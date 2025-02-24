# MQTT Project

A modular, high-performance MQTT broker implementation in Python with Docker support and web-based monitoring.

## Project Structure
```
mqtt_project/
├── docker/ # Docker configuration files
│ ├── Dockerfile.broker # Main broker Dockerfile
│ └── docker-compose.yml # Docker compose configuration
├── mqtt_broker/ # Main broker implementation
│ ├── src/ # Source code
│ ├── tests/ # Unit tests
│ └── pyproject.toml # Package configuration
├── mqtt_network/ # Network handling module
├── mqtt_protocol/ # MQTT protocol implementation
├── mqtt_storage/ # Storage implementations
├── mqtt_auth/ # Authentication and authorization
├── mqtt_common/ # Shared utilities and interfaces
└── mqtt_monitor/ # Web-based monitoring interface
```

## Submodules

### mqtt_common
Core interfaces and shared utilities used across all modules. Defines the contract for:
- Message handling
- Network operations
- Storage operations
- Authentication/Authorization

### mqtt_network
Handles all network-related operations:
- TCP connection management
- Connection pooling
- Async I/O operations
- Session management

### mqtt_protocol
MQTT protocol implementation:
- MQTT 3.1.1 and 5.0 support
- Packet encoding/decoding
- QoS handling
- Topic matching
- Retain message handling

### mqtt_storage
Pluggable storage implementations:
- In-memory storage (default)
- File-based persistence
- Database backend

### mqtt_auth
Authentication and authorization:
- Username/password authentication
- Certificate-based auth
- Access Control Lists (ACL)
- Custom auth providers

### mqtt_broker
Main broker implementation that combines all modules:
- Module orchestration
- Configuration management
- Metrics collection
- Logging

### mqtt_monitor
Web-based monitoring interface:
- Real-time connection statistics
- Message flow visualization
- System metrics
- Log viewing
- Configuration management

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.11+

### Installation
1. Clone the repository:
   ```bash
   git clone 
   cd mqtt_project
   ```

2. Build the project:
   ```bash
   docker compose build
   ```

3. Start the broker:
   ```bash
   docker compose up -d
   ```

4. Access the web monitor:
   ```bash
   open http://localhost:8080
   ```

Features:
- Dashboard with key metrics
- Active connections view
- Topic explorer
- Message flow visualization
- System logs  

### Configuration

The broker can be configured through:
- Environment variables
- Configuration file (config.yaml)
- Web interface

### Start everything (broker + monitoring)
docker-compose up
### Start only the broker
docker-compose up mqtt-broker