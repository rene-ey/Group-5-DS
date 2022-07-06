import socket
import json

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
    print(msg.decode())

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(("", int(msg.decode())))
        data = json.dumps({"method": "join"})
        sock.sendall(bytes(data,encoding="utf-8"))
        while True:
            data = sock.recv(2048).decode()
            if data == "Bisch in der Lobby, warte du pisser":
                print("Lobby warten auf Gegner...")
            elif data == "GO":
                input("St, Sc, Pa?")
                # Als Json verschicken, mit Method: turn oder so und selection: rock
                sock.sendall(b"Stein")
            elif data == "WIN":
                print("Du hast gewonnen")
            elif data == "LOSE":
                print("Du hast verloren")

    except KeyboardInterrupt:
        sock.sendall(b"quit")
        sock.close()


