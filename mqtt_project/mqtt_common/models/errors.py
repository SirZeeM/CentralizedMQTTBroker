class MQTTError(Exception):
    """Base exception for all MQTT-related errors"""
    pass

class ProtocolError(MQTTError):
    """Raised when there's an MQTT protocol violation"""
    pass

class ConnectError(MQTTError):
    """Raised for network connection issues"""
    pass

class AuthenticationError(MQTTError):
    """Raised when authentication fails"""
    pass

class AuthorizationError(MQTTError):
    """Raised when a client is not authorized for an operation"""
    pass

class StorageError(MQTTError):
    """Raised when storage operations fail"""
    pass

class ValidationError(MQTTError):
    """Raised when data validation fails"""
    pass