import pytest
from datetime import datetime
from mqtt_common.models.message import Message

def test_valid_message_creation():
    """Test creating a valid message"""
    msg = Message(
        topic="test/topic",
        payload=b"test payload",
        qos=0,
        retain=False
    )
    assert msg.topic == "test/topic"
    assert msg.payload == b"test payload"
    assert msg.qos == 0
    assert msg.retain is False
    assert isinstance(msg.timestamp, datetime)
    assert msg.properties == {}

def test_message_with_properties():
    """Test message with custom properties"""
    props = {"user_property": "test"}
    msg = Message(
        topic="test/topic",
        payload=b"test",
        qos=0,
        retain=False,
        properties=props
    )
    assert msg.properties == props

def test_invalid_qos():
    """Test message creation with invalid QoS"""
    with pytest.raises(ValueError, match="QoS must be 0, 1, or 2"):
        Message(
            topic="test/topic",
            payload=b"test",
            qos=3,
            retain=False
        )

def test_qos_without_message_id():
    """Test QoS > 0 message without message_id"""
    with pytest.raises(ValueError, match="Message ID is required for QoS > 0"):
        Message(
            topic="test/topic",
            payload=b"test",
            qos=1,
            retain=False
        )

def test_invalid_topic_type():
    """Test message creation with invalid topic type"""
    with pytest.raises(ValueError, match="Topic must be a string"):
        Message(
            topic=123,  # type: ignore
            payload=b"test",
            qos=0,
            retain=False
        )

def test_invalid_payload_type():
    """Test message creation with invalid payload type"""
    with pytest.raises(ValueError, match="Payload must be bytes"):
        Message(
            topic="test/topic",
            payload="test",  # type: ignore
            qos=0,
            retain=False
        )