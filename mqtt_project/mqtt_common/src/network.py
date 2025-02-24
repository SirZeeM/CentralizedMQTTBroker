from abc import ABC, abstractmethod
from typing import Callable, Awaitable, Optional
from ..models.message import Message

class NetworkInterface(ABC):
    """Interface for network operations in MQTT broker"""
    
    @abstractmethod
    async def start(self, host: str, port: int) -> None:
        """
        Start the network server
        
        Args:
            host: The host address to bind to
            port: The port number to listen on
        """
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Stop the network server and clean up resources"""
        pass

    @abstractmethod
    async def send_message(self, client_id: str, message: Message) -> None:
        """
        Send a message to a specific client
        
        Args:
            client_id: The unique identifier of the client
            message: The Message object to send
        """
        pass

    @abstractmethod
    def get_client_count(self) -> int:
        """Return the current number of connected clients"""
        pass

    @abstractmethod
    def is_client_connected(self, client_id: str) -> bool:
        """
        Check if a client is currently connected
        
        Args:
            client_id: The unique identifier of the client
        """
        pass