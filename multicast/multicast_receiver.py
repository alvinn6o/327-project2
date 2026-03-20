#Joins a UDP multicast group and receives text, JSON, and binary messages.

import socket
import struct
import json
import time
import argparse
import signal
import sys

# Multicast config
MULTICAST_GROUP = "224.1.1.1"
PORT            = 5007
BUFFER_SIZE     = 4096

# 4-byte magic header used by the sender to mark binary frames
BINARY_MAGIC    = b"\xDE\xAD\xBE\xEF"


def build_socket() -> socket.socket:
    """Create a UDP socket and join the multicast group."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Allow multiple processes on the same host to bind the same port
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", PORT))

    # Tell the kernel to join the multicast group on all interfaces
    group = socket.inet_aton(MULTICAST_GROUP)
    mreq  = struct.pack("4sL", group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    return sock


def leave_group(sock: socket.socket) -> None:
    """Drop membership from the multicast group and close the socket."""
    group = socket.inet_aton(MULTICAST_GROUP)
    mreq  = struct.pack("4sL", group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
    sock.close()
    print("Leaving multicast group")


def handle_message(data: bytes, addr: tuple) -> None:
    """Detect message type and pretty-print the received payload."""
    # Binary frame 
    if data[:4] == BINARY_MAGIC:
        head_hex = data[:4].hex()
        print(f"Received binary from {addr[0]}:{addr[1]}: "
              f"[binary] {len(data)} bytes, head={head_hex}")
        return

    # Try to decode as UTF-8 text
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        # Unknown binary format — show raw length
        print(f"Received unknown binary from {addr[0]}:{addr[1]}: {len(data)} bytes")
        return

    # JSON payload
    try:
        payload = json.loads(text)
        print(f"Received json from {addr[0]}:{addr[1]}: {payload}")
        return
    except json.JSONDecodeError:
        pass

    # Plain text
    print(f"Received text from {addr[0]}:{addr[1]}: {text}")


def main() -> None:
    parser = argparse.ArgumentParser(description="UDP Multicast Receiver")
    parser.add_argument(
        "--duration", type=int, default=30,
        help="How many seconds to listen before leaving the group (default: 30)"
    )
    args = parser.parse_args()

    sock = build_socket()
    sock.settimeout(1.0)          # non-blocking 1-second timeout so we can check the clock

    print(f"Joined multicast group {MULTICAST_GROUP}:{PORT} "
          f"(listening for {args.duration}s)")

    # Allow Ctrl-C to exit cleanly
    def _sigint_handler(sig, frame):
        leave_group(sock)
        sys.exit(0)

    signal.signal(signal.SIGINT, _sigint_handler)

    deadline = time.time() + args.duration

    try:
        while time.time() < deadline:
            try:
                data, addr = sock.recvfrom(BUFFER_SIZE)
                handle_message(data, addr)
            except socket.timeout:
                # No packet arrived in this 1-second window — just loop again
                continue
    finally:
        leave_group(sock)


if __name__ == "__main__":
    main()