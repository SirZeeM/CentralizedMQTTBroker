from enum import IntEnum, auto

# MQTT Protocol Constants
class MQTTProtocol:
    """MQTT Protocol Constants"""
    VERSION_3_1_1 = 4  # MQTT Version 3.1.1
    VERSION_5_0 = 5    # MQTT Version 5.0
    DEFAULT_PORT = 1883
    DEFAULT_TLS_PORT = 8883
    
    # Default values
    DEFAULT_KEEP_ALIVE = 60  # seconds
    DEFAULT_FLAGS = 0
    
    # Size limits
    MAX_PACKET_SIZE = 268435455  # 256MB (per MQTT spec)
    MAX_TOPIC_LENGTH = 65535     # bytes
    MAX_CLIENT_ID_LENGTH = 23    # characters
    
    # Header constants
    PROTOCOL_NAME_3_1_1 = "MQTT" # Protocol name for MQTT 3.1.1
    PROTOCOL_NAME_3_1 = "MQIsdp" # Protocol name for MQTT 3.1

    # Bit masks and shifts
    PACKET_TYPE_MASK = 0xF0
    PACKET_TYPE_SHIFT = 4
    FLAGS_MASK = 0x0F
    
    # Variable length encoding
    CONTINUATION_BIT = 0x80
    LENGTH_MASK = 0x7F
    MAX_LENGTH_BYTES = 4
    
    # Connect flags
    CONNECT_WILL_FLAG = 0x04
    CONNECT_CLEAN_SESSION_FLAG = 0x02 
    CONNECT_USERNAME_FLAG = 0x80
    CONNECT_PASSWORD_FLAG = 0x40
    CONNECT_WILL_RETAIN_FLAG = 0x20
    CONNECT_WILL_QOS_MASK = 0x18
    CONNECT_WILL_QOS_SHIFT = 3
    
    # Minimum packet sizes
    MIN_PACKET_LENGTH = 2
    MIN_HEADER_LENGTH = 1
    
    # Field sizes
    LENGTH_FIELD_SIZE = 2  # Size of length fields for strings and binary data
    KEEP_ALIVE_SIZE = 2    # Size of keep alive field in CONNECT
    
    # Encoding
    STRING_ENCODING = 'utf-8'
    BYTE_ORDER = 'big'

    # PUBLISH flags
    PUBLISH_DUP_FLAG = 0x08 # Duplicate delivery flag   
    PUBLISH_QOS_MASK = 0x06 # QoS level mask
    PUBLISH_QOS_SHIFT = 1 # QoS level shift
    PUBLISH_RETAIN_FLAG = 0x01 # Retain flag
    
    # Field sizes
    PACKET_ID_SIZE = 2 # Size of packet ID field    

class QualityOfService(IntEnum):
    """MQTT Quality of Service levels"""
    AT_MOST_ONCE = 0 # At most once delivery
    AT_LEAST_ONCE = 1 # At least once delivery
    EXACTLY_ONCE = 2 # Exactly once delivery

class PacketType(IntEnum):
    """MQTT Control Packet Types"""
    CONNECT = 1 # Sent by client to initiate a connection to the broker
    CONNACK = 2 # Sent by broker to acknowledge the connection request
    PUBLISH = 3 # Sent by client or broker to publish a message
    PUBACK = 4 # Sent by broker to acknowledge a published message
    PUBREC = 5 # Sent by broker to acknowledge a published message
    PUBREL = 6 # Sent by client to release a message
    PUBCOMP = 7 # Sent by broker to acknowledge a published message
    SUBSCRIBE = 8 # Sent by client to subscribe to a topic      
    SUBACK = 9 # Sent by broker to acknowledge a subscription request
    UNSUBSCRIBE = 10 # Sent by client to unsubscribe from a topic
    UNSUBACK = 11 # Sent by broker to acknowledge an unsubscribe request
    PINGREQ = 12 # Sent by client to check the connection
    PINGRESP = 13 # Sent by broker to respond to a ping request
    DISCONNECT = 14 # Sent by client to disconnect from the broker

class ConnectReturnCode(IntEnum):
    """Connection return codes for CONNACK packets"""
    ACCEPTED = 0 # Client can proceed with MQTT operations
    UNACCEPTABLE_PROTOCOL_VERSION = 1 # Client should reconnect with a supported version
    IDENTIFIER_REJECTED = 2 # Client ID is already in use
    SERVER_UNAVAILABLE = 3 # Server is temporarily unavailable
    BAD_USERNAME_PASSWORD = 4 # Username or password is incorrect
    NOT_AUTHORIZED = 5 # Client is not authorized to connect