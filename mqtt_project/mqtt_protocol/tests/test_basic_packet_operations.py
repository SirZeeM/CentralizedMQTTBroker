import pytest
from mqtt_common.models.constants import PacketType, QualityOfService, MQTTProtocol
from mqtt_common.models.errors import ValidationError
from mqtt_protocol.src.packet import ConnectPacket, PublishPacket, ConnAckPacket
from mqtt_protocol.src.encoder import PacketEncoder
from mqtt_protocol.src.parser import PacketParser

class TestConnectPacket:
    """Tests for CONNECT packet creation and validation."""
    
    @pytest.mark.asyncio
    async def test_create_minimal_connect_packet(self):
        """Tests creation of a CONNECT packet with minimal required fields."""
        packet = ConnectPacket(
            packet_type=PacketType.CONNECT,
            client_id="test-client"
        )
        assert packet.protocol_name == MQTTProtocol.PROTOCOL_NAME_3_1_1
        assert packet.protocol_version == MQTTProtocol.VERSION_3_1_1
        assert packet.clean_session is True
        assert packet.keep_alive == MQTTProtocol.DEFAULT_KEEP_ALIVE

        encoded = PacketEncoder.encode(packet)
        decoded = await PacketParser.decode(encoded)
        assert isinstance(decoded, ConnectPacket)
        assert decoded.client_id == packet.client_id


    @pytest.mark.asyncio
    async def test_create_full_connect_packet(self):
        """Tests creation of a CONNECT packet with all optional fields."""
        packet = ConnectPacket(
            packet_type=PacketType.CONNECT,
            client_id="test-client",
            clean_session=False,
            keep_alive=30,
            username="user",
            password=b"pass",
            will_topic="will/topic",
            will_message=b"offline",
            will_qos=QualityOfService.AT_LEAST_ONCE,
            will_retain=True
        )
        assert packet.username == "user"
        assert packet.password == b"pass"
        assert packet.will_topic == "will/topic"
        assert packet.will_message == b"offline"
        assert packet.will_qos == QualityOfService.AT_LEAST_ONCE
        assert packet.will_retain is True

        encoded = PacketEncoder.encode(packet)
        decoded = await PacketParser.decode(encoded)
        assert isinstance(decoded, ConnectPacket)
        assert decoded.username == packet.username
        assert decoded.will_topic == packet.will_topic

    def test_connect_validation_no_client_id(self):
        """Tests that CONNECT validation fails when client_id is missing with clean_session False."""
        packet = ConnectPacket(
            packet_type=PacketType.CONNECT,
            clean_session=False
        )
        with pytest.raises(ValidationError, match="Client ID is required"):
            packet.validate()

    def test_connect_will_validation(self):
        """Tests that CONNECT validation fails when will fields are inconsistent."""
        packet = ConnectPacket(
            packet_type=PacketType.CONNECT,
            client_id="test-client",
            will_topic="topic",  # Message missing
        )
        with pytest.raises(ValidationError, match="Will topic and message must both be present"):
            packet.validate()

class TestPublishPacket:
    """Tests for PUBLISH packet creation and validation."""
    
    @pytest.mark.asyncio
    async def test_create_minimal_publish_packet(self):
        """Tests creation of a PUBLISH packet with QoS 0."""
        packet = PublishPacket(
            topic="test/topic",
            payload=b"test message"
        )
        assert packet.topic == "test/topic"
        assert packet.payload == b"test message"
        assert packet.qos == QualityOfService.AT_MOST_ONCE
        assert packet.packet_id is None
        assert packet.retain is False
        assert packet.dup is False

        encoded = PacketEncoder.encode(packet)
        decoded = await PacketParser.decode(encoded)
        assert isinstance(decoded, PublishPacket)
        assert decoded.topic == packet.topic
        assert decoded.payload == packet.payload

    def test_create_qos1_publish_packet(self):
        """Tests creation of a PUBLISH packet with QoS 1."""
        packet = PublishPacket(
            topic="test/topic",
            payload=b"test message",
            qos=QualityOfService.AT_LEAST_ONCE,
            packet_id=1
        )
        assert packet.qos == QualityOfService.AT_LEAST_ONCE
        assert packet.packet_id == 1

    def test_publish_validation_empty_topic(self):
        """Tests that PUBLISH validation fails when topic is empty."""
        packet = PublishPacket(
            topic="",
            payload=b"test"
        )
        with pytest.raises(ValidationError, match="Topic cannot be empty"):
            packet.validate()

    def test_publish_validation_qos_packet_id(self):
        """Tests that PUBLISH validation fails when packet_id is missing for QoS > 0."""
        packet = PublishPacket(
            topic="test/topic",
            payload=b"test",
            qos=QualityOfService.AT_LEAST_ONCE
        )
        with pytest.raises(ValidationError, match="Packet ID is required"):
            packet.validate()

class TestConnAckPacket:
    """Tests for CONNACK packet creation."""
    
    def test_create_connack_packet(self):
        """Tests creation of a CONNACK packet."""
        packet = ConnAckPacket(
            packet_type=PacketType.CONNACK,
            session_present=True
        )
        assert packet.session_present is True
        assert packet.return_code == 0  # ACCEPTED