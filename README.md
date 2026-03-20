# Project 2 Docker
# Authors: Alvin Ngo, Jason Tran

# How to test for Task 1 (anycast)

TCP Dump to capture traffic (in separate terminal)
docker exec -it anycast-server1-1 apt-get update && docker exec -it anycast-server1-1 apt-get install -y tcpdump
docker exec -it anycast-server1-1 tcpdump -i eth0 port 5000

From the /anycast folder run the client multiple times in another terminal to show connections with anycast with:
docker compose run client1 

