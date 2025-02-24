from typing import List
from mqtt_common.models.constants import PacketType, QualityOfService, MQTTProtocol
from mqtt_common.models.errors import ProtocolError
from .packet import MQTTPacket, ConnectPacket, PublishPacket

def encode_packet(packet: 'MQTTPacket') -> bytes:
    """Encodes the MQTT packet into its byte representation."""
    return PacketEncoder.encode_fixed_header(
        packet.packet_type, packet.flags, packet.remaining_length
    )

@staticmethod
def encode(packet: 'MQTTPacket') -> bytes:
    """Static method for packet encoding."""
    return encode_packet(packet)

class PacketEncoder:
    """Handles encoding of MQTT packets from objects to bytes."""
    
    @staticmethod
    def encode_packet(packet: MQTTPacket) -> bytes:
        """Encodes an MQTT packet object into its byte representation according to the MQTT protocol."""
        if isinstance(packet, ConnectPacket):
            return PacketEncoder._encode_connect(packet)
        elif isinstance(packet, PublishPacket):
            return PacketEncoder._encode_publish(packet)
        else:
            # Basic packet encoding for other types
            return PacketEncoder.encode_fixed_header(
                packet.packet_type,
                packet.flags,
                packet.remaining_length
            )

    @staticmethod
    def encode_fixed_header(packet_type: PacketType, flags: int, remaining_length: int) -> bytes:
        """Encodes the fixed header of an MQTT packet, including packet type, flags, and remaining length."""
        if remaining_length > MQTTProtocol.MAX_PACKET_SIZE:
            raise ProtocolError("Packet too large")
            
        # First byte: packet type and flags
        byte1 = (packet_type << MQTTProtocol.PACKET_TYPE_SHIFT) | (flags & MQTTProtocol.FLAGS_MASK)
        
        # Encode remaining length
        remaining_bytes = []
        while remaining_length > 0 or not remaining_bytes:
            byte = remaining_length % 128
            remaining_length = remaining_length // 128
            if remaining_length > 0:
                byte |= MQTTProtocol.CONTINUATION_BIT
            remaining_bytes.append(byte)
            
            if len(remaining_bytes) > MQTTProtocol.MAX_LENGTH_BYTES:
                raise ProtocolError("Remaining length too large")
                
        return bytes([byte1] + remaining_bytes)

    @staticmethod
    def _encode_connect(packet: ConnectPacket) -> bytes:
        """Encodes a CONNECT packet with client identification, protocol version, and optional authentication."""
        # Variable header
        variable_header = []
        
        # Protocol name
        variable_header.extend(PacketEncoder.encode_string(packet.protocol_name))
        
        # Protocol version
        variable_header.append(packet.protocol_version)
        
        # Connect flags
        connect_flags = 0
        if packet.clean_session:
            connect_flags |= MQTTProtocol.CONNECT_CLEAN_SESSION_FLAG
        if packet.will_topic is not None:
            connect_flags |= MQTTProtocol.CONNECT_WILL_FLAG
            connect_flags |= (packet.will_qos.value << MQTTProtocol.CONNECT_WILL_QOS_SHIFT)
            if packet.will_retain:
                connect_flags |= MQTTProtocol.CONNECT_WILL_RETAIN_FLAG
        if packet.username is not None:
            connect_flags |= MQTTProtocol.CONNECT_USERNAME_FLAG
        if packet.password is not None:
            connect_flags |= MQTTProtocol.CONNECT_PASSWORD_FLAG
        variable_header.append(connect_flags)
        
        # Keep alive
        variable_header.extend(
            packet.keep_alive.to_bytes(MQTTProtocol.KEEP_ALIVE_SIZE, MQTTProtocol.BYTE_ORDER)
        )
        
        # Payload
        payload = []
        payload.extend(PacketEncoder.encode_string(packet.client_id))
        
        if packet.will_topic is not None:
            payload.extend(PacketEncoder.encode_string(packet.will_topic))
            payload.extend(PacketEncoder.encode_bytes(packet.will_message))
            
        if packet.username is not None:
            payload.extend(PacketEncoder.encode_string(packet.username))
            
        if packet.password is not None:
            payload.extend(PacketEncoder.encode_bytes(packet.password))
            
        # Combine all parts
        variable_header_and_payload = bytes(variable_header + payload)
        fixed_header = PacketEncoder.encode_fixed_header(
            PacketType.CONNECT,
            0,
            len(variable_header_and_payload)
        )
        
        return fixed_header + variable_header_and_payload

    @staticmethod
    def _encode_publish(packet: PublishPacket) -> bytes:
        """Encodes a PUBLISH packet containing the topic, payload, and quality of service settings."""
        # Calculate flags
        flags = 0
        if packet.dup: # Duplicate delivery flag
            flags |= MQTTProtocol.PUBLISH_DUP_FLAG
        flags |= (packet.qos.value << MQTTProtocol.PUBLISH_QOS_SHIFT)
        if packet.retain:
            flags |= MQTTProtocol.PUBLISH_RETAIN_FLAG
            
        # Variable header
        variable_header = []
        variable_header.extend(PacketEncoder.encode_string(packet.topic)) # Encodes the topic string    
        
        if packet.qos > QualityOfService.AT_MOST_ONCE:
            if packet.packet_id is None: # Packet ID required for QoS > 0
                raise ProtocolError("Packet ID required for QoS > 0")
            variable_header.extend(
                packet.packet_id.to_bytes(MQTTProtocol.PACKET_ID_SIZE, MQTTProtocol.BYTE_ORDER)
            )
            
        # Combine all parts
        variable_header_and_payload = bytes(variable_header) + packet.payload
        fixed_header = PacketEncoder.encode_fixed_header( 
            PacketType.PUBLISH,
            flags,
            len(variable_header_and_payload)
        )
        
        return fixed_header + variable_header_and_payload

    @staticmethod
    def encode_string(string: str) -> bytes:
        """Encodes a string into MQTT format with a 2-byte length prefix followed by UTF-8 encoded string data."""
        encoded = string.encode(MQTTProtocol.STRING_ENCODING)
        length = len(encoded)
        
        if length > MQTTProtocol.MAX_TOPIC_LENGTH:
            raise ProtocolError("String too long")
            
        return length.to_bytes(MQTTProtocol.LENGTH_FIELD_SIZE, MQTTProtocol.BYTE_ORDER) + encoded

    @staticmethod
    def encode_bytes(data: bytes) -> bytes:
        """Encodes a byte array into MQTT format with a 2-byte length prefix followed by the raw data."""
        length = len(data)
        return length.to_bytes(MQTTProtocol.LENGTH_FIELD_SIZE, MQTTProtocol.BYTE_ORDER) + data