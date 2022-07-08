from re import T
import socket
import threading
import json

"""
    body: {
        player_name: "Rene",
    }
"""

def get_result(player1, player2):
    result = ""
    rock = "rock"
    paper = "paper"
    scissors = "scissors"
    print("Player 1:", player1)
    print("Player 2:", player2)

    if player1 == player2:
        result = "DRAW"
    elif player1 == rock:
        if player2 == paper:
            result = "LOSE"
        else:
            result = "WIN"
    elif player1 == scissors:
        if player2 == rock:
            result = "LOSE"
        else:
            result = "WIN"
    elif player1 == paper:
        if player2 == scissors:
            result = "LOSE"
        else:
            result = "WIN"
    return result


class TcpClient:
    def __init__(self,host: str, port: int, event: threading.Event):
        self.host = host
        self.port = port
        self.shared_bool = event
        self.is_free = True
        self.player = {} #"Name": [], "address":[], "selection":[]
        self.score = {}

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))


    def listen(self):
        print("Start listening tcp on {}:{}".format(self.host,self.port))
        self.socket.listen(2)
        while True:
            if len(self.player) < 2:
                client, address = self.socket.accept()
                if len(self.player) < 2:
                    self.player[address] = {
                        "name": "Rene",
                        "selection": None,
                        "client": client
                    }
                threading.Thread(target=self.get_data, args=(client, address)).start()




    def get_data(self, client: socket.socket, address):
        while True:
            try:
                data = client.recv(2048).decode()
            except ConnectionResetError:
                self.player.pop(address, None)
                # Reset Spielstand, weil der Gegner ragequited ist
                self.shared_bool.clear()
                client.close()
                if len(self.player) > 0:
                    for key in self.player:
                        self.player[key]["client"].sendall(b"Wait for oppenent")
                break
            if not data:
                self.player.pop(address, None)
                # Reset Spielstand, weil der Gegner ragequited ist
                self.shared_bool.clear()
                client.close()
                if len(self.player) > 0:
                    for key in self.player:
                        self.player[key]["client"].sendall(b"Wait for oppenent")
                break
            try:
                json_data = json.loads(data)
                print("Client sendet request:{}".format(json_data["method"]))
                if json_data["method"] == "join":
                    if len(self.player) == 2:
                        self.shared_bool.set()
                        client.sendall(b"GO")
                    else:
                        client.sendall(b"Wait for oppenent")
                
                elif json_data["method"] == "turn":
                    print(json_data["selection"])
                    if len(self.player) < 2:
                        client.sendall(b"Wait for oppenent")

                    # Checken ob es die Auswahl überhaupt gibt

                    self.player[address]["selection"] = json_data["selection"]

                    for key in self.player:
                        if key != address and  self.player[key]["selection"] is not None:
                            game_status = get_result(self.player[address]["selection"], self.player[key]["selection"])
                            if game_status == "WIN":
                                client.sendall(b"WIN")
                                self.player[key]["client"].sendall(b"LOSE")
                            elif game_status == "DRAW":
                                client.sendall(b"DRAW")
                                self.player[key]["client"].sendall(b"DRAW")
                            elif game_status == "LOSE":
                                client.sendall(b"LOSE")
                                self.player[key]["client"].sendall(b"WIN")

                            self.player[address]["selection"] = None
                            self.player[key]["selection"] = None
                            
                            client.sendall(b"GO")
                            self.player[key]["client"].sendall(b"GO")

                        else:
                            client.sendall(b"Warte auf Gegnerischenzug")
                    
                    # Daten im Scoreboard speichern
                    
                   
                elif json_data["method"] == "scoreboard":
                    client.sendall(self.score)
            except json.JSONDecodeError:
                client.sendall(b"Please send valid data")
