from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class AuthCredentials:
    """Authentication credentials container"""
    username: Optional[str] = None
    password: Optional[bytes] = None
    client_id: str = ""
    certificate: Optional[bytes] = None
    custom_auth_data: Optional[Dict[str, Any]] = None

class AuthInterface(ABC):
    """Interface for authentication and authorization"""
    
    @abstractmethod
    async def authenticate(self, credentials: AuthCredentials) -> bool:
        """
        Authenticate a client
        
        Args:
            credentials: The AuthCredentials object containing auth data
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        pass

    @abstractmethod
    async def authorize_publish(self, client_id: str, topic: str) -> bool:
        """
        Check if client can publish to topic
        
        Args:
            client_id: The unique identifier of the client
            topic: The topic to publish to
        
        Returns:
            bool: True if authorized, False otherwise
        """
        pass

    @abstractmethod
    async def authorize_subscribe(self, client_id: str, topic: str) -> bool:
        """
        Check if client can subscribe to topic
        
        Args:
            client_id: The unique identifier of the client
            topic: The topic to subscribe to
        
        Returns:
            bool: True if authorized, False otherwise
        """
        pass