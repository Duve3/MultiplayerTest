import socket
from _thread import *
from player import Player
import pickle
import random
import pygame

encoding = "utf-8"
DisconnectMSG = "!!!Disconnect"
DisconnectRES = "Disconnected"
HitMSG = "HIT:"
HitRES = "Player Hit"

server = "127.0.0.1"
port = 5556
header = 2048

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)
    print(e)

s.listen()
print("Waiting for a connection, Server Started")


playerList = {}


def threaded_client(conn, pid):
    if pid in playerList:
        conn.send(pickle.dumps(playerList[pid]))
    else:
        newPlayer = Player(0, 0, 50, 50, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), pid)
        conn.send(pickle.dumps(newPlayer))
        playerList[pid] = newPlayer

    while True:
        try:
            data = conn.recv(header)

            if data == DisconnectMSG.encode(encoding):
                print("Disconnected")
                conn.send(DisconnectRES.encode(encoding))
                break
            else:
                reply = [x for i, x in enumerate(playerList.values()) if i != pid and x is not None]

            DataPickled = pickle.loads(data)

            print("Received: ", data)
            print("Sending : ", reply)

            # game logic
            collisionList = [pygame.Rect(plr.rect) for plr in reply]
            collision = pygame.Rect.collidelist(pygame.Rect(playerList[pid].rect), collisionList)
            if collision != -1:
                print(f"{collision = }")
                print(f"{collisionList = }")
                print(f"{[playerList.keys()] = }")
                collideID = [key for key in playerList.keys()].index(reply[collision].id)  # we are doing key for key ... because we are trying to avoid getting a dict_keys object from the playerList.keys()
                print(f"{collideID = }")
                playerList[collideID].health -= 5

            for plr in playerList.values():
                plr.width = plr.health // 2
                plr.height = plr.health // 2

            playerList[pid].x = DataPickled[0]  # x
            playerList[pid].y = DataPickled[1]  # y

            # refresh reply
            reply = [x for i, x in enumerate(playerList.values()) if i != pid and x is not None]

            print(playerList[pid].__repr__())

            conn.sendall(pickle.dumps(reply))
            conn.sendall(pickle.dumps(playerList[pid]))

        except Exception as err:
            print(f"{err = }")
            break

    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
