# UDP multicast receiver

import socket
import struct
import argparse
import json
import time

# Multicast group address and port (must match sender)
MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

# Parse --duration: leave group after N seconds
parser = argparse.ArgumentParser()
parser.add_argument('--duration', type=int, default=None)
args, _ = parser.parse_known_args()

# Create UDP socket and allow multiple receivers on same port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))

# Join multicast group
mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print('Joined multicast group')
start = time.time()

try:
    while True:
        # Exit after --duration seconds if set
        if args.duration and (time.time() - start) >= args.duration:
            break
        sock.settimeout(1.0)  # Allow periodic duration check
        try:
            data, addr = sock.recvfrom(65535)
        except socket.timeout:
            continue
        # Handle message types: JSON, plain text, or binary
        try:
            text = data.decode('utf-8')
            try:
                json.loads(text)
                print(f'Received: {text}')
            except json.JSONDecodeError:
                print(f'Received: {text} from {addr}')
        except UnicodeDecodeError:
            print(f'Received: <binary {len(data)} bytes> from {addr}')
except KeyboardInterrupt:
    pass
finally:
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
    sock.close()
    print('Leaving multicast group')
