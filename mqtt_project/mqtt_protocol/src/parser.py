from typing import Tuple
from mqtt_common.models.constants import PacketType, QualityOfService, MQTTProtocol
from mqtt_common.models.errors import ProtocolError
from .packet import MQTTPacket, ConnectPacket, ConnAckPacket, PublishPacket

async def decode_packet(data: bytes) -> 'MQTTPacket':
    """Decodes raw bytes into an MQTT packet object."""
    if len(data) < 2:  # 2 bytes are the minimum length of an MQTT packet
        raise ProtocolError("Packet too short")
    
    packet_type, flags, remaining_length = await PacketParser.parse_fixed_header(data)
    return MQTTPacket(packet_type=packet_type, flags=flags, remaining_length=remaining_length)

@staticmethod
async def decode(data: bytes) -> 'MQTTPacket':
    """Static method for packet decoding."""
    return await decode_packet(data)

class PacketParser:
    """Handles parsing of MQTT packets from raw bytes into structured packet objects."""
    @staticmethod
    async def parse_packet(data: bytes) -> MQTTPacket:
        """Parses a complete MQTT packet from bytes and returns the appropriate packet object based on type."""
        if len(data) < MQTTProtocol.MIN_PACKET_LENGTH:
            raise ProtocolError("Packet too short")
            
        packet_type, flags, remaining_length = await PacketParser.parse_fixed_header(data)
        
        header_length = PacketParser._get_header_length(data)
        total_length = header_length + remaining_length
        
        if len(data) < total_length:
            raise ProtocolError("Incomplete packet")
            
        packet_data = data[header_length:total_length]
        
        if packet_type == PacketType.CONNECT:
            return await PacketParser._parse_connect(packet_data)
        elif packet_type == PacketType.PUBLISH:
            return await PacketParser._parse_publish(packet_data, flags)
        
        return MQTTPacket(packet_type=packet_type, flags=flags, remaining_length=remaining_length)

    @staticmethod
    async def parse_fixed_header(data: bytes) -> Tuple[PacketType, int, int]:
        """Parses the fixed header of an MQTT packet, extracting packet type, flags, and remaining length."""
        if not data:
            raise ProtocolError("Empty packet")
            
        byte1 = data[0]
        packet_type = PacketType(byte1 >> MQTTProtocol.PACKET_TYPE_SHIFT) 
        flags = byte1 & MQTTProtocol.FLAGS_MASK
        
        multiplier = 1 
        remaining_length = 0
        index = MQTTProtocol.MIN_HEADER_LENGTH
        
        while True:
            if index >= len(data):
                raise ProtocolError("Incomplete packet")
            if index > MQTTProtocol.MAX_LENGTH_BYTES:
                raise ProtocolError("Remaining length field too long")
                
            byte = data[index]
            remaining_length += (byte & MQTTProtocol.LENGTH_MASK) * multiplier
            
            if remaining_length > MQTTProtocol.MAX_PACKET_SIZE:
                raise ProtocolError("Packet too large")
                
            if byte & MQTTProtocol.CONTINUATION_BIT == 0:
                break
                
            multiplier *= 128
            index += 1
            
        return packet_type, flags, remaining_length

    @staticmethod
    async def _parse_connect(data: bytes) -> ConnectPacket:
        """Parses a CONNECT packet, extracting protocol information, client details, and optional will message settings."""
        offset = 0
        protocol_name, offset = await PacketParser.parse_string(data, offset)
        
        if offset + MQTTProtocol.KEEP_ALIVE_SIZE >= len(data):
            raise ProtocolError("Invalid CONNECT packet")
            
        protocol_version = data[offset]
        connect_flags = data[offset + 1]
        keep_alive = int.from_bytes(
            data[offset + 2:offset + 2 + MQTTProtocol.KEEP_ALIVE_SIZE], 
            MQTTProtocol.BYTE_ORDER
        )
        offset += 2 + MQTTProtocol.KEEP_ALIVE_SIZE
        
        client_id, offset = await PacketParser.parse_string(data, offset)
        
        will_topic = None
        will_message = None
        if connect_flags & MQTTProtocol.CONNECT_WILL_FLAG:
            will_topic, offset = await PacketParser.parse_string(data, offset)
            will_message, offset = await PacketParser.parse_bytes(data, offset)
            
        username = None
        if connect_flags & MQTTProtocol.CONNECT_USERNAME_FLAG:
            username, offset = await PacketParser.parse_string(data, offset)
            
        password = None
        if connect_flags & MQTTProtocol.CONNECT_PASSWORD_FLAG:
            password, offset = await PacketParser.parse_bytes(data, offset)
            
        return ConnectPacket(
            protocol_name=protocol_name,
            protocol_version=protocol_version,
            clean_session=bool(connect_flags & MQTTProtocol.CONNECT_CLEAN_SESSION_FLAG),
            keep_alive=keep_alive,
            client_id=client_id,
            will_topic=will_topic,
            will_message=will_message,
            will_qos=QualityOfService(
                (connect_flags & MQTTProtocol.CONNECT_WILL_QOS_MASK) 
                >> MQTTProtocol.CONNECT_WILL_QOS_SHIFT
            ),
            will_retain=bool(connect_flags & MQTTProtocol.CONNECT_WILL_RETAIN_FLAG),
            username=username,
            password=password
        )

    @staticmethod
    async def parse_string(data: bytes, offset: int) -> Tuple[str, int]:
        """Parses a length-prefixed UTF-8 string from the packet data and returns the string and new offset."""
        if offset + MQTTProtocol.LENGTH_FIELD_SIZE > len(data):
            raise ProtocolError("Incomplete string length")
            
        length = int.from_bytes(
            data[offset:offset + MQTTProtocol.LENGTH_FIELD_SIZE], 
            MQTTProtocol.BYTE_ORDER
        )
        
        if length > MQTTProtocol.MAX_TOPIC_LENGTH:
            raise ProtocolError("String too long")
            
        string_end = offset + MQTTProtocol.LENGTH_FIELD_SIZE + length
        if string_end > len(data):
            raise ProtocolError("Incomplete string data")
            
        string = data[
            offset + MQTTProtocol.LENGTH_FIELD_SIZE:string_end
        ].decode(MQTTProtocol.STRING_ENCODING)
        
        return string, string_end
    
    @staticmethod
    async def _parse_publish(data: bytes, flags: int) -> PublishPacket:
        """Parses a PUBLISH packet, extracting topic, payload, and message delivery settings including QoS level."""
        offset = 0
        topic, offset = await PacketParser.parse_string(data, offset)
        
        # Parse packet ID for QoS > 0
        qos = (flags & MQTTProtocol.PUBLISH_QOS_MASK) >> MQTTProtocol.PUBLISH_QOS_SHIFT
        packet_id = None
        if qos > QualityOfService.AT_MOST_ONCE.value:
            if offset + MQTTProtocol.PACKET_ID_SIZE > len(data):
                raise ProtocolError("Invalid PUBLISH packet")
            packet_id = int.from_bytes(
                data[offset:offset + MQTTProtocol.PACKET_ID_SIZE], 
                MQTTProtocol.BYTE_ORDER
            )
            offset += MQTTProtocol.PACKET_ID_SIZE
            
        payload = data[offset:]
        
        return PublishPacket(
            topic=topic,
            payload=payload,
            packet_id=packet_id,
            qos=QualityOfService(qos),
            retain=bool(flags & MQTTProtocol.PUBLISH_RETAIN_FLAG),
            dup=bool(flags & MQTTProtocol.PUBLISH_DUP_FLAG)
        )
    
    @staticmethod
    async def parse_bytes(data: bytes, offset: int) -> Tuple[bytes, int]:
        """Parses a length-prefixed byte array from the packet data and returns the bytes and new offset."""
        if offset + MQTTProtocol.LENGTH_FIELD_SIZE > len(data):
            raise ProtocolError("Incomplete bytes length")
            
        length = int.from_bytes(
            data[offset:offset + MQTTProtocol.LENGTH_FIELD_SIZE], 
            MQTTProtocol.BYTE_ORDER
        )
        
        bytes_end = offset + MQTTProtocol.LENGTH_FIELD_SIZE + length
        if bytes_end > len(data):
            raise ProtocolError("Incomplete bytes data")
            
        return (
            data[offset + MQTTProtocol.LENGTH_FIELD_SIZE:bytes_end], 
            bytes_end
        )