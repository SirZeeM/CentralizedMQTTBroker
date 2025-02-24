from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from ..models.message import Message

class SessionInterface(ABC):
    """Interface for client session management"""
    
    @abstractmethod
    async def create_session(self, client_id: str, clean_session: bool) -> None:
        """
        Create a new client session
        
        Args:
            client_id: The unique identifier of the client
            clean_session: Whether to start with a clean session
        """
        pass

    @abstractmethod
    async def end_session(self, client_id: str) -> None:
        """
        End a client session
        
        Args:
            client_id: The unique identifier of the client
        """
        pass

    @abstractmethod
    async def store_will_message(self, client_id: str, message: Message) -> None:
        """
        Store a client's will message
        
        Args:
            client_id: The unique identifier of the client
            message: The will Message to store
        """
        pass

    @abstractmethod
    async def get_session_data(self, client_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve session data for a client
        
        Args:
            client_id: The unique identifier of the client
        
        Returns:
            Optional[Dict[str, Any]]: Session data if exists, None otherwise
        """
        pass67