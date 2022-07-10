import socket
import json
import time

if __name__ == "__main__":

    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5007
    MULTICAST_TTL = 2

    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

    udp_sock.sendto(b"searching", (MCAST_GRP, MCAST_PORT))
    print("Your multicast message has been sent to the group {}:{}".format(MCAST_GRP,MCAST_PORT))

    msg, address = udp_sock.recvfrom(2048)

    name = input("You have been assigned to the server with the port {}. What is your Name? ".format(msg.decode()))

    # TCP Connection with the GameServer
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((address[0], int(msg.decode())))
        #sock.connect((address[0], int(msg.decode())))
        print("Connected with Server {}:{}".format(address[0],int(msg.decode())))
        data = json.dumps({"method": "join", "name": name})
        sock.send(bytes(data,encoding="utf-8"))
        while True:
            rev_data = sock.recv(2048).decode()
            if rev_data == "Wait for opponent":
                print("You are in the lobby, please wait for opponent...")
                time.sleep(5)
                sock.send(bytes(data,encoding="utf-8"))            
            elif rev_data == "GO":
                selection = input("Choose: rock or paper or scissors???   ")
                data_turn = json.dumps({"method": "turn", "selection": selection})
                print(f'Your selection has been sent and was: {selection}')
                sock.sendall(bytes(data_turn,encoding="utf-8"))
            elif rev_data == "WIN":
                print("Congratulations! You have won :)")
            elif rev_data == "LOSE":
                print("Too bad you lost :(")
            elif rev_data == "DRAW":
                print("You played a draw!")

    except KeyboardInterrupt:
        sock.sendall(b"quit")
        sock.close()


