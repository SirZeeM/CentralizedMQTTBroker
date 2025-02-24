# MQTT Common Module

The MQTT Common module serves as the foundation for the entire MQTT broker project, providing core interfaces, models, and utilities that are shared across all other modules.

## Directory Structure

```
mqtt_common/
├── src/
│ ├── init.py
│ ├── network.py # Network-related interfaces
│ ├── storage.py # Storage-related interfaces
│ ├── auth.py # Authentication interfaces
│ └── session.py # Session-related interfaces
├── models/
│ ├── init.py
│ ├── message.py # MQTT message models
│ ├── constants.py # Constants for MQTT
│ └── errors.py # Custom exceptions
├── tests/
│ ├── interfaces/
│ ├── models/
│ └── utils/
├── pyproject.toml
└── README.md
```

## Core Components

### Interfaces (`src/`)

#### Authentication (`auth.py`)
- `AuthInterface`: Abstract base class for authentication providers
- `AuthCredentials`: Data class for authentication information
- Supports username/password and certificate-based auth
- Handles both authentication and authorization

#### Network (`network.py`)
- `NetworkInterface`: Abstract base class for network operations
- Manages client connections
- Handles message delivery
- Tracks connection states

#### Session (`session.py`)
- `SessionInterface`: Abstract base class for session management
- Handles client session persistence
- Manages will messages
- Stores session state

#### Storage (`storage.py`)
- `StorageInterface`: Abstract base class for storage operations
- Manages message persistence
- Handles subscription storage
- Supports various backend implementations

### Models (`models/`)

#### Message (`message.py`)
```python
from mqtt_common.models import Message

# Create a new message
message = Message(
    topic="sensors/temperature",
    payload=b"23.5",
    qos=1,
    retain=False,
    message_id=12345
)
```

#### Constants (`constants.py`)
- `MQTTProtocol`: Protocol-specific constants
- `QualityOfService`: QoS level definitions
- `PacketType`: MQTT packet type enumerations
- `ConnectReturnCode`: Connection response codes

#### Errors (`errors.py`)
- `MQTTError`: Base exception class
- `ProtocolError`: Protocol violation errors
- `ConnectError`: Connection-related errors
- `AuthenticationError`: Authentication failures
- `AuthorizationError`: Permission-related errors
- `StorageError`: Storage operation failures
- `ValidationError`: Data validation errors

## Testing

The test suite covers:

- Interface contracts
- Model validation
- Error handling
- Utility functions

Run tests using:
```bash
pytest mqtt_common/tests/test_name.py
```

## Dependencies

- Python 3.11+
- No external dependencies (core module)

## Best Practices

When implementing interfaces:

1. Inherit from the appropriate interface class
2. Implement all abstract methods
3. Follow the type hints
4. Handle all defined exceptions
5. Add unit tests in the test suite