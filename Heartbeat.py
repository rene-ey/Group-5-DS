import socket
import time
import subprocess

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
MULTICAST_TTL = 2

def leader_election(ports):
    lowest_port = None
    for port in ports:
        int_port = int(port)
        if lowest_port is None:
            lowest_port = int_port
        elif int_port < lowest_port:
            lowest_port = int_port
    return lowest_port



def main():
    servers = {}
    leader = set()
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
    udp_sock.settimeout(15)
    tries = 0


    while True:
        udp_sock.sendto(b"heartbeat", (MCAST_GRP, MCAST_PORT))
        try:
            msg = udp_sock.recv(2048).decode().split(" ")
            now = time.time()
            if msg[1] == "True":
                leader.add(msg[0])
            elif msg[1] == "False" and msg[0] in leader:
                leader.discard(msg[0])
            servers[msg[0]] = now
            for server in list(servers):
                if now - servers[server] > 10:
                    print(f"{server} down")
                    servers.pop(server)
                    if server in leader:
                        leader.clear()
            if len(leader) == 0 or len(leader) > 1:
                print("Start Leader Election")
                new_leader = leader_election(list(servers))
                print("This is the new leader ",new_leader)
                leader_msg = f"leader {new_leader}"
                udp_sock.sendto(bytes(leader_msg, encoding="utf-8"), (MCAST_GRP, MCAST_PORT))
            if len(servers) == 1 and tries > 10:
                port = int(list(servers)[0]) + 2
                '''if port > 9001:
                    port = 9000'''
                try:
                    cmd = f"python server1.py localhost {port} false"
                    subprocess.Popen(cmd.split(),stdout=subprocess.PIPE)
                except OSError:
                    pass


        except socket.timeout:
            print("All servers are down - - New servers are being started")
            servers = {}
            leader.clear()
            cmd = "python server1.py localhost 9000 true"
            subprocess.Popen(cmd.split(),stdout=subprocess.PIPE)
            cmd = "python server1.py localhost 9001 false"
            subprocess.Popen(cmd.split(),stdout=subprocess.PIPE)
            pass
        time.sleep(2)
        tries += 1
        print(servers)
        print(leader)


if __name__ == '__main__':
    main()