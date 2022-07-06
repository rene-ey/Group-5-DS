import socket
import struct
import threading

class UdpClient:
    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5007

    def __init__(self, is_leader: bool, event: threading.Event, tcp_port: int):
        self.leader = is_leader
        self.tcp_port = tcp_port
        self.is_free = True
        self.shared_bool = event
        self.searching = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        self.socket.bind(("", self.MCAST_PORT))

        mreq = struct.pack("4sl", socket.inet_aton(self.MCAST_GRP), socket.INADDR_ANY)

        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


    def run(self):
        print("Start listening udp")
        while True:
            data, address = self.socket.recvfrom(10240)
            if data.decode() == "searching" and self.leader is True:
                print("Mach ich")
                print("Client:", address)
                self.searching.append(address)
            elif data.decode() == "searching" and self.leader is False:
                send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                send_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
                if not self.shared_bool.is_set():
                    print("Sendign free message")
                    msg = f"BIN FREI {self.tcp_port}"
                    send_socket.sendto(bytes(msg, encoding="utf-8"), (self.MCAST_GRP, self.MCAST_PORT))
                send_socket.close()
            if data.decode().startswith("BIN FREI") and self.leader is True:
                port = data.decode().split(" ")[-1]
                for i in self.searching:
                    self.socket.sendto(bytes(port, encoding="utf-8"), i)
                self.searching = []


    def set_leader(self):
        self.leader = True