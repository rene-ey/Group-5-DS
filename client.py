import socket
import json
import time

"""MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
# regarding socket.IP_MULTICAST_TTL
# ---------------------------------
# for all packets sent, after two hops on the network the packet will not
# be re-sent/broadcast (see https://www.tldp.org/HOWTO/Multicast-HOWTO-6.html)
MULTICAST_TTL = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

sock.sendto(b"searching", (MCAST_GRP, MCAST_PORT))

msg = sock.recvfrom(2048)
print(msg)"""

if __name__ == "__main__":

    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5007
    # regarding socket.IP_MULTICAST_TTL
    # ---------------------------------
    # for all packets sent, after two hops on the network the packet will not
    # be re-sent/broadcast (see https://www.tldp.org/HOWTO/Multicast-HOWTO-6.html)
    MULTICAST_TTL = 2

    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

    udp_sock.sendto(b"searching", (MCAST_GRP, MCAST_PORT))

    msg, address = udp_sock.recvfrom(2048)
    name = input("You are playing on Port {}. What is your Name? ".format(msg.decode()))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(("", int(msg.decode())))
        data = json.dumps({"method": "join", "name": name})
        sock.send(bytes(data,encoding="utf-8"))
        while True:
            rev_data = sock.recv(2048).decode()
            if rev_data == "Wait for oppenent":
                print("You are in the lobby, please wait for opponents...")
                time.sleep(5)
                sock.send(bytes(data,encoding="utf-8"))
                
            elif rev_data == "GO":
                selection = input("Choose: rock or paper or scissors???   ")
                data_turn = json.dumps({"method": "turn", "selection": selection})
                print(f'Your selection was: {data_turn}')
                sock.sendall(bytes(data_turn,encoding="utf-8"))
                print('Daten wurden gesendet')
                # Als Json verschicken, mit Method: turn oder so und selection: rock
                #sock.sendall(b"Stein")
            elif rev_data == "WIN":
                print("Du hast gewonnen")
            elif rev_data == "LOSE":
                print("Du hast verloren")
            elif rev_data == "DRAW":
                print("Unentschieden")

    except KeyboardInterrupt:
        sock.sendall(b"quit")
        sock.close()


