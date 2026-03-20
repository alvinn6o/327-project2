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
docker compose up --build

TCP Dump to capture traffic (in separate terminal while containers are running)
docker exec -it receiver1 tcpdump -i eth0 udp port 5007

Receivers will automatically join the multicast group 224.1.1.1 and listen for 30 seconds.
sender1 sends money data, sender2 sends cash data (JSON with type/value), both receivers print all messages.
Containers exit automatically after 30 seconds.