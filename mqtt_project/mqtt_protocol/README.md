# MQTT Protocol Module

The MQTT Protocol module handles all MQTT packet encoding, decoding, and validation according to the MQTT 3.1.1 specification. This module is designed to be protocol-version agnostic and extensible for future MQTT versions.

## Directory Structure

```
mqtt_protocol/
├── src/
│   ├── __init__.py
│   ├── encoder.py      # Handles packet encoding to bytes
│   ├── parser.py       # Handles packet parsing from bytes
│   └── packet.py       # Packet class definitions
├── tests/
│   ├── __init__.py
│   ├── test_basic_packet_operations.py
│   ├── test_encode_and_decode.py
│   ├── test_error_handling.py
│   └── test_qos_levels.py
└── README.md
```

## Core Components

### Packet Classes (`packet.py`)
- `MQTTPacket`: Base class for all MQTT packets
- `ConnectPacket`: Handles client connection requests
- `ConnAckPacket`: Represents broker connection responses
- `PublishPacket`: Manages message publication

### Packet Encoder (`encoder.py`)
- Converts packet objects to byte sequences
- Handles fixed headers, variable headers, and payloads
- Supports all MQTT packet types
- Includes validation and error checking

### Packet Parser (`parser.py`)
- Converts byte sequences to packet objects
- Implements asynchronous parsing
- Handles packet type detection
- Performs protocol compliance validation and error handling

## Features

- Full MQTT 3.1.1 protocol support
- Asynchronous operation
- Comprehensive error handling
- QoS level support (0, 1, 2)
- Retain message handling
- Will message support
- Clean session management
- Username/password authentication
- Keep-alive monitoring






## Testing the protocol:
The test suite covers:

### Unit Tests for Basic Packet Operations:
Test packet creation and validation.
- CONNECT packets: Ensure client identification and authentication fields are handled correctly
- PUBLISH packets: Verify topic, payload, and QoS fields are properly set
- Other packet types: Test basic packet structure and flags

### Encoding/Decoding Tests:
Test round-trip conversions. Must verify all packet types can be encoded to bytes and decoded back to the original packet object correctly. 
- Packet to bytes conversion: Ensure packets are correctly serialized
- Bytes to packet conversion: Verify proper deserialization
- Edge cases: Test maximum lengths, special characters, empty fields

### QoS Level Tests:
Test different quality of service scenarios, must verify all delivery guarantee levels work correctly.
- QoS 0: At most once delivery (fire and forget)
- QoS 1: At least once delivery (with PUBACK)
- QoS 2: Exactly once delivery (with PUBREC, PUBREL, PUBCOMP) 

### Error Handling Tests:
Test protocol error conditions, must verify all error handling mechanisms work correctly. Robust error handling is essential for maintaining protocol stability and security.
- `ProtocolError`: For MQTT protocol violations
- `ValidationError`: For invalid packet content
- `EncodingError`: For encoding-related issues

## Run tests using:
```bash
pytest mqtt_protocol/tests/test_name.py
```

## Dependencies

- Python 3.11+
- `mqtt_common` module for shared constants and models