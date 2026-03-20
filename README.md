# Project 2 Docker
# Authors: Alvin Ngo, Jason Tran

# How to test for Task 1 (anycast)

TCP Dump to capture traffic (in separate terminal)
docker exec -it anycast-server1-1 apt-get update && docker exec -it anycast-server1-1 apt-get install -y tcpdump
docker exec -it anycast-server1-1 tcpdump -i eth0 port 5000

From the /anycast folder run the client multiple times in another terminal to show connections with anycast with:
docker compose run client1 

# How to test for Task 2 (multicast)

From the /multicast folder, build and start all containers:
docker compose up

tcpdump in a separate terminal:
docker exec -it multicast-multicast_receiver1-1 tcpdump -i eth0 udp port 5007
RUN RIGHT AFTER docker compose up runs on first terminal

Receivers join multicast group 224.1.1.1:5007 for 15 seconds.
sender1 sends temp data, sender2 sends humidity data (JSON + binary). Both receivers print all messages.