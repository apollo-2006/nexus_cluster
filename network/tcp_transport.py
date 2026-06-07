import asyncio
import json
from typing import Callable, Awaitable, Optional, Dict, Any


class TCPTransport:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server = None

    async def start_listening(self, rpc_handler: Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]]):
        """Boots the asynchronous TCP server to listen for incoming Raft RPCs."""

        async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
            try:
                # Read the incoming payload (max 4KB for prototype)
                data = await reader.read(4096)
                if not data:
                    return

                # Decode the JSON RPC
                request = json.loads(data.decode('utf-8'))

                # Pass to the Node's logical handler and await the response
                response_dict = await rpc_handler(request)

                # Encode and send the response back over the wire
                writer.write(json.dumps(response_dict).encode('utf-8'))
                await writer.drain()
            except Exception as e:
                print(f"[Transport Error] Failed handling client: {e}")
            finally:
                writer.close()
                await writer.wait_closed()

        self.server = await asyncio.start_server(handle_client, self.host, self.port)
        print(f"[Transport] Node binding to {self.host}:{self.port}...")

    async def send_rpc(self, target_host: str, target_port: int, payload: str) -> Optional[Dict[str, Any]]:
        """Opens a TCP socket, transmits the RPC payload, and awaits the response."""
        try:
            # Attempt to connect to the peer
            reader, writer = await asyncio.open_connection(target_host, target_port)

            # Fire the payload
            writer.write(payload.encode('utf-8'))
            await writer.drain()

            # Await the peer's response
            data = await reader.read(4096)

            writer.close()
            await writer.wait_closed()

            return json.loads(data.decode('utf-8'))

        except ConnectionRefusedError:
            # The target node is dead or partitioned.
            # We return None so the Raft logic can handle the timeout.
            return None
        except asyncio.TimeoutError:
            # Network latency is too high
            return None