import asyncio
from typing import Dict, Optional
from mqtt_common.src.network import NetworkInterface
from mqtt_common.models.message import Message

class CentralizedNetwork(NetworkInterface):
    def __init__(self):
        self.server: Optional[asyncio.Server] = None # Server object for handling client connections    
        self.clients: Dict[str, asyncio.StreamWriter] = {} # Dictionary of connected clients
        self.running: bool = False # Flag to indicate if the server is running

    async def start(self, host: str, port: int) -> None:
        """Start the TCP server and listen for connections"""
        self.running = True
        self.server = await asyncio.start_server( 
            self.handle_client_connection, host, port
        )
        
        async with self.server:
            await self.server.serve_forever()

    async def stop(self) -> None:
        """Stop the server and close all client connections"""
        self.running = False
        if self.server: 
            self.server.close()
            await self.server.wait_closed()
            
        # Close all client connections
        for writer in self.clients.values():
            writer.close()
            await writer.wait_closed()
        self.clients.clear()

    async def send_message(self, client_id: str, message: Message) -> None:
        """Send a message to a specific client"""
        if client_id not in self.clients: 
            raise ValueError(f"Client {client_id} not connected")
            
        writer = self.clients[client_id]
        try:
            # Convert message to bytes and send
            message_bytes = message.to_bytes()
            writer.write(message_bytes)
            await writer.drain() 
        except Exception as e:
            # Handle connection errors
            await self._remove_client(client_id)
            raise ConnectionError(f"Failed to send message to client {client_id}: {str(e)}")

    def get_client_count(self) -> int:
        """Return the current number of connected clients"""
        return len(self.clients)

    def is_client_connected(self, client_id: str) -> bool:
        """Check if a client is currently connected"""
        return client_id in self.clients

    async def handle_client_connection(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        """Handle new client connections"""
        # Wait for CONNECT packet to get client_id
        try:
            connect_packet = await self._read_connect_packet(reader)
            client_id = connect_packet.client_id
            
            # Store client connection
            self.clients[client_id] = writer
            
            # Handle incoming messages until connection closes
            while self.running:
                try:
                    message = await self._read_message(reader)
                    if message is None:  # Connection closed
                        break
                    # Process message (implement message handling logic)
                    await self._handle_message(client_id, message)
                except ConnectionError:
                    break
                
        finally:
            await self._remove_client(client_id)

    async def _remove_client(self, client_id: str) -> None:
        """Remove a client and clean up their connection"""
        if client_id in self.clients:
            writer = self.clients[client_id]
            writer.close()
            await writer.wait_closed()
            del self.clients[client_id]

    async def _read_connect_packet(self, reader: asyncio.StreamReader) -> Message:
        """Read and parse the initial CONNECT packet"""
        # Implement MQTT CONNECT packet parsing
        pass

    async def _read_message(self, reader: asyncio.StreamReader) -> Optional[Message]:
        """Read and parse an MQTT message"""
        # Implement MQTT message parsing
        pass

    async def _handle_message(self, client_id: str, message: Message) -> None:
        """Process received messages"""
        # Implement message handling logic
        pass
