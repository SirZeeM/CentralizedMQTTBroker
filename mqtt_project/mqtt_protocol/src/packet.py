from dataclasses import dataclass
from typing import Optional
from mqtt_common.models.constants import (
    PacketType, QualityOfService, ConnectReturnCode, MQTTProtocol
)
from mqtt_common.models.errors import ValidationError, ProtocolError


@dataclass
class MQTTPacket:
    """Base class representing an MQTT packet with common fields for all packet types."""
    packet_type: PacketType
    flags: int = MQTTProtocol.DEFAULT_FLAGS
    remaining_length: int = 0 

@dataclass
class ConnectPacket(MQTTPacket):
    """Represents an MQTT CONNECT packet used by clients to establish a connection with the broker."""
    protocol_name: str = MQTTProtocol.PROTOCOL_NAME_3_1_1
    protocol_version: int = MQTTProtocol.VERSION_3_1_1
    clean_session: bool = True
    keep_alive: int = MQTTProtocol.DEFAULT_KEEP_ALIVE
    client_id: str = ""
    will_topic: Optional[str] = None
    will_message: Optional[bytes] = None
    will_qos: QualityOfService = QualityOfService.AT_MOST_ONCE
    will_retain: bool = False
    username: Optional[str] = None
    password: Optional[bytes] = None

    def validate(self) -> None:
        """Validates the CONNECT packet fields according to MQTT protocol rules, checking client ID, QoS, and will message settings."""
        if not self.client_id and not self.clean_session:
            raise ValidationError("Client ID is required for non-clean sessions")
        if self.will_qos not in QualityOfService:
            raise ValidationError(f"Invalid QoS level: {self.will_qos}")
        if bool(self.will_topic) != bool(self.will_message):
            raise ValidationError("Will topic and message must both be present or absent")

@dataclass
class ConnAckPacket(MQTTPacket):
    """Represents an MQTT CONNACK packet sent by the broker in response to a client's CONNECT request."""
    session_present: bool = False
    return_code: ConnectReturnCode = ConnectReturnCode.ACCEPTED

@dataclass
class PublishPacket(MQTTPacket):
    """Represents an MQTT PUBLISH packet used to distribute messages between clients through the broker."""
    topic: str
    payload: bytes
    packet_id: Optional[int] = None
    qos: QualityOfService = QualityOfService.AT_MOST_ONCE
    retain: bool = False
    dup: bool = False
    packet_type: PacketType = PacketType.PUBLISH

    def validate(self) -> None:
        """Validates the PUBLISH packet fields, ensuring topic is present, QoS is valid, and packet ID is included when required."""
        if not self.topic:
            raise ValidationError("Topic cannot be empty")
        if self.qos not in QualityOfService:
            raise ValidationError(f"Invalid QoS level: {self.qos}")
        if self.qos > QualityOfService.AT_MOST_ONCE and self.packet_id is None:
            raise ValidationError("Packet ID is required for QoS > 0")