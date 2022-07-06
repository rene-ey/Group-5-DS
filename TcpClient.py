import socket
import threading
import json

"""
    body: {
        player_name: "Rene",
    }
"""

class TcpClient:
    def __init__(self,host: str, port: int, event: threading.Event):
        self.host = host
        self.port = port
        self.shared_bool = event
        self.is_free = True
        self.player = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))


    def listen(self):
        print("Start listening tcp")
        self.socket.listen(2)
        while True:
            if len(self.player) < 2:
                client, address = self.socket.accept()
                threading.Thread(target=self.get_data, args=(client, address)).start()




    def get_data(self, client: socket.socket, address):
        while True:
            data = client.recv(2048).decode()
            if not data:
                self.player.pop(address, None)
                # Reset Spielstand, weil der Gegner ragequited ist
                self.shared_bool.clear()
                client.close()
                break
            try:
                json_data = json.loads(data)
                if json_data["method"] == "join":
                    self.player[address] = {
                        "name": "Rene",
                        "selection": ""
                    }
                    if len(self.player) == 2:
                        self.shared_bool.set()
                        client.sendall(b"GO")
                    else:
                        client.sendall(b"Bisch in der Lobby, warte du pisser")
                # json_data["method"] == "turn", dann schauen was der andere gespielt hat und in self.player oder so speichern
            except json.JSONDecodeError:
                client.sendall(b"Schick mal gut Daten, du Hund")

