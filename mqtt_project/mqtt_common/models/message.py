from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class Message:
    """
    MQTT Message representation
    
    Attributes:
        topic: The topic this message is published to
        payload: The message content as bytes
        qos: Quality of Service level (0, 1, or 2)
        retain: Whether this is a retained message
        message_id: Optional message identifier (required for QoS > 0)
        properties: Optional MQTT 5.0 properties
        timestamp: When the message was created
    """
    topic: str
    payload: bytes
    qos: int
    retain: bool
    message_id: Optional[int] = None
    properties: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        """Validate message attributes after initialization"""
        if not isinstance(self.topic, str):
            raise ValueError("Topic must be a string")
        if not isinstance(self.payload, bytes):
            raise ValueError("Payload must be bytes")
        if self.qos not in (0, 1, 2):
            raise ValueError("QoS must be 0, 1, or 2")
        if not isinstance(self.retain, bool):
            raise ValueError("Retain must be a boolean")
        if self.qos > 0 and self.message_id is None:
            raise ValueError("Message ID is required for QoS > 0")