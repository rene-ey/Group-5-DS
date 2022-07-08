import sys
from GameServer import GameServer

def main(host: str, tcp_port: int, is_leader: bool):
    GameServer(host, tcp_port, is_leader).run()
    #GameServer("", 9000, 9002, False).run()


if __name__ == '__main__':
    host = ""
    tcp_port = int(sys.argv[2])
    is_leader = sys.argv[3].lower() == 'true'
    print( tcp_port, is_leader)
    main(host, tcp_port, is_leader)
