from TcpClient import TcpClient
from UdpClient import UdpClient
import threading

class GameServer:
    def __init__(self, host: str, tcp_port: int, is_leader: bool):
        self.tcp_port = tcp_port
        self.host = host
        self.is_leader = is_leader
        self.shared_bool = threading.Event() #ob Gameserver frei ist oder belegt
        self.tcp_server = TcpClient("", self.tcp_port, self.shared_bool)
        self.udp_server = UdpClient(is_leader, self.shared_bool, self.tcp_port)

    def run(self):
        # Mulitcast
        udp = threading.Thread(target=self.udp_server.run)
        # Server auf dem die Spiele laufen
        tcp = threading.Thread(target=self.tcp_server.listen)

        udp.start()
        tcp.start()
