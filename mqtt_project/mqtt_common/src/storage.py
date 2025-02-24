from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from ..models.message import Message

class StorageInterface(ABC):
    """Interface for message and subscription storage"""
    
    @abstractmethod
    async def store_message(self, message: Message) -> None:
        """
        Store a message
        
        Args:
            message: The Message object to store
        """
        pass

    @abstractmethod
    async def get_message(self, message_id: int) -> Optional[Message]:
        """
        Retrieve a message by ID
        
        Args:
            message_id: The unique identifier of the message
        """
        pass

    @abstractmethod
    async def store_subscription(self, client_id: str, topic: str, qos: int) -> None:
        """
        Store a client's subscription
        
        Args:
            client_id: The unique identifier of the client
            topic: The topic pattern subscribed to
            qos: Quality of Service level
        """
        pass

    @abstractmethod
    async def remove_subscription(self, client_id: str, topic: str) -> None:
        """
        Remove a client's subscription
        
        Args:
            client_id: The unique identifier of the client
            topic: The topic pattern to unsubscribe from
        """
        pass

    @abstractmethod
    async def get_subscriptions(self, topic: str) -> List[Tuple[str, int]]:
        """
        Get all subscriptions matching a topic
        
        Args:
            topic: The topic to match against
        
        Returns:
            List of tuples containing (client_id, qos)
        """
        pass 