#Sends text, JSON, and binary data to a UDP multicast group.

import socket
import struct
import time
import json
import os
import random
import argparse

#Multicast config
MULTICAST_GROUP = "224.1.1.1"
PORT            = 5007
TTL             = 2          # how many router hops the packet can cross


def build_socket() -> socket.socket:
    """Create and configure a UDP socket for multicast sending."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Set the Time-To-Live for multicast packets
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack("b", TTL))
    return sock


def send_text(sock: socket.socket, sender_name: str) -> None:
    """Send a plain-text greeting message to the multicast group."""
    message = f"Hello from {sender_name}"
    sock.sendto(message.encode(), (MULTICAST_GROUP, PORT))
    print(f"Sent text: {message}")


def send_json(sock: socket.socket, sender_name: str, data_type: str, value: float) -> None:
    """Send a JSON-encoded data (money/cash) to the multicast group."""
    payload = {
        "type":   data_type,
        "value":  value,
        "sender": sender_name,
        "ts":     time.time(),
    }
    data = json.dumps(payload)
    sock.sendto(data.encode(), (MULTICAST_GROUP, PORT))
    print(f"Sent JSON: {data}")


def send_binary(sock: socket.socket) -> None:
    """Send 32 random bytes (prefixed with a 4-byte header) to the multicast group."""
    # 4-byte magic header so receivers can identify binary frames
    header  = b"\xDE\xAD\xBE\xEF"
    payload = header + os.urandom(28)          # total = 32 bytes
    sock.sendto(payload, (MULTICAST_GROUP, PORT))
    print(f"Sent binary: {len(payload)} bytes")


def main() -> None:
    parser = argparse.ArgumentParser(description="UDP Multicast Sender")
    parser.add_argument("--name",   default="sender1",  help="Sender identifier")
    parser.add_argument("--type",   dest="data_type", default="money",
                        help="Data type (e.g. money, cash)")
    parser.add_argument("--value",  type=float,
                        default=None, help="Amount value (random if omitted)")
    args = parser.parse_args()

    # Use a provided value or generate a random amount (e.g. dollars)
    amount = args.value if args.value is not None else round(random.uniform(10.0, 500.0), 2)

    sock = build_socket()

    try:
        # 1. Plain text greeting
        send_text(sock, args.name)
        time.sleep(0.5)

        # 2. JSON data (money/cash)
        send_json(sock, args.name, args.data_type, amount)
        time.sleep(0.5)

        # 3. Binary payload
        send_binary(sock)

    finally:
        sock.close()


if __name__ == "__main__":
    main()