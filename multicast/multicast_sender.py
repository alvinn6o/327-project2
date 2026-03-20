# UDP multicast sender - sends JSON and binary to 224.1.1.1:5007

import socket
import json
import os
import time
import random

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

sensor_type = os.environ.get('SENSOR_TYPE', 'temp')
time.sleep(2)  # let receivers join

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

# 1. Text
msg = 'Multicast message'
sock.sendto(msg.encode('utf-8'), (MCAST_GRP, MCAST_PORT))
print(f'Sent: {msg}')

# 2. JSON
json_msg = {'sensor': sensor_type, 'value': round(random.uniform(20, 30), 1)}
json_str = json.dumps(json_msg)
sock.sendto(json_str.encode('utf-8'), (MCAST_GRP, MCAST_PORT))
print(f'Sent: {json_str}')

# 3. Binary
sock.sendto(bytes(random.getrandbits(8) for _ in range(32)), (MCAST_GRP, MCAST_PORT))
print('Sent: <binary 32 bytes>')

sock.close()
