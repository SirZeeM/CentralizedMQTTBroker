import pytest
from typing import List, Optional, Tuple
from mqtt_common.interfaces.storage import StorageInterface
from mqtt_common.models.message import Message

class MockStorage(StorageInterface):
    """Mock implementation of StorageInterface for testing"""
    
    def __init__(self):
        self.messages = {}
        self.subscriptions = {}

    async def store_message(self, message: Message) -> None:
        if message.message_id:
            self.messages[message.message_id] = message

    async def get_message(self, message_id: int) -> Optional[Message]:
        return self.messages.get(message_id)

    async def store_subscription(self, client_id: str, topic: str, qos: int) -> None:
        if client_id not in self.subscriptions:
            self.subscriptions[client_id] = []
        self.subscriptions[client_id].append((topic, qos))

    async def remove_subscription(self, client_id: str, topic: str) -> None:
        if client_id in self.subscriptions:
            self.subscriptions[client_id] = [
                (t, q) for t, q in self.subscriptions[client_id] 
                if t != topic
            ]

    async def get_subscriptions(self, topic: str) -> List[Tuple[str, int]]:
        result = []
        for client_id, subs in self.subscriptions.items():
            for sub_topic, qos in subs:
                if sub_topic == topic:  # Simple matching for testing
                    result.append((client_id, qos))
        return result


@pytest.mark.asyncio
class TestStorageInterface:
    """Test suite for StorageInterface"""

    @pytest.fixture
    async def storage(self):
        """Provide a mock storage implementation"""
        return MockStorage()

    async def test_store_and_get_message(self, storage):
        """Test storing and retrieving a message"""
        # Create test message
        message = Message(
            topic="test/topic",
            payload=b"test payload",
            qos=1,
            retain=False,
            message_id=1
        )

        # Store message
        await storage.store_message(message)

        # Retrieve message
        retrieved = await storage.get_message(1)
        assert retrieved is not None
        assert retrieved.topic == "test/topic"
        assert retrieved.payload == b"test payload"
        assert retrieved.qos == 1
        assert retrieved.retain is False

    async def test_get_nonexistent_message(self, storage):
        """Test retrieving a message that doesn't exist"""
        message = await storage.get_message(999)
        assert message is None

    async def test_subscription_management(self, storage):
        """Test subscription storage operations"""
        # Store subscription
        await storage.store_subscription("client1", "test/topic", 1)
        await storage.store_subscription("client2", "test/topic", 0)

        # Get subscriptions
        subs = await storage.get_subscriptions("test/topic")
        assert len(subs) == 2
        assert ("client1", 1) in subs
        assert ("client2", 0) in subs

    async def test_remove_subscription(self, storage):
        """Test removing a subscription"""
        # Store and then remove subscription
        await storage.store_subscription("client1", "test/topic", 1)
        await storage.remove_subscription("client1", "test/topic")

        # Verify removal
        subs = await storage.get_subscriptions("test/topic")
        assert len(subs) == 0

    async def test_multiple_subscriptions_per_client(self, storage):
        """Test handling multiple subscriptions for a single client"""
        # Store multiple subscriptions
        await storage.store_subscription("client1", "test/topic1", 1)
        await storage.store_subscription("client1", "test/topic2", 2)

        # Verify first topic
        subs1 = await storage.get_subscriptions("test/topic1")
        assert ("client1", 1) in subs1

        # Verify second topic
        subs2 = await storage.get_subscriptions("test/topic2")
        assert ("client1", 2) in subs2

        # Remove one subscription
        await storage.remove_subscription("client1", "test/topic1")

        # Verify removal of first topic only
        subs1 = await storage.get_subscriptions("test/topic1")
        assert len(subs1) == 0
        subs2 = await storage.get_subscriptions("test/topic2")
        assert len(subs2) == 1