import os
import socket
import threading
from QuizzesSQL import *
from PlayersSQL import *
import random
import pickle

IP = "0.0.0.0"
PORT = 5000
CHUNK = 1024
SOS = 5

games = {}


def main():
    server_socket = socket.socket()
    server_socket.bind((IP, PORT))
    server_socket.listen(1)
    while True:
        client_socket, client_address = server_socket.accept()
        t = threading.Thread(target=handle_client, args=(client_socket, client_address[0],))
        t.start()


def handle_client(client_socket, ip):
    client_socket.settimeout(0.01)

    players_db = PlayersORM()
    quizzes_db = ""
    while True:
        try:
            size = client_socket.recv(SOS)

            # Check if the player closed his socket
            if size == "":
                connected = False
                print "Client disconnected"
                break

            # Receives the message from client by the size and returns a list [action, parameters:]
            data = handle_msg(client_socket, size)
            print data
            # Messages from the game editor
            if data[0] == "CREATE" and quizzes_db == "":
                quizzes_db = QuizzesORM(data[1])
                quizzes_db.open_DB()

            elif data[0] == "ADD" and quizzes_db != "":
                quizzes_db.add_question(data[1], data[2], data[3], data[4], data[5])

            elif data[0] == "START":
                while True:
                    cur_pin = random.randint(100000, 999999)
                    if cur_pin not in games.keys():
                        cur_pin = str(cur_pin)
                        games[cur_pin] = ip
                        send_msg(client_socket, ["PIN", cur_pin])
                        print games
                        break

            elif data[0] == "STOP":
                for key in games.keys():
                    if games[key] == ip:
                        del games[key]
                        print games

            elif data[0] == "GQUIZZES":
                quiz_db = QuizzesORM("")
                quizzes = quiz_db.get_quizzes()
                quizzes_send = ["QUIZZES"]
                for q in quizzes:
                    quizzes_send.append(q)
                print quizzes_send
                send_msg(client_socket, quizzes_send)

            elif data[0] == "GQUIZ":
                quiz_db = QuizzesORM(data[1])
                quiz = quiz_db.get_quiz()
                s = pickle.dumps(quiz)
                send_msg(client_socket, ["QUIZ", s])

            elif data[0] == "ADDPTO":
                db = PlayersORM()
                db.update_points(data[1], int(data[2]))

            # Messages from the android player
            elif data[0] == "LOG":
                if data[1] not in players_db.get_all_usernames():
                    send_msg(client_socket, ["WRNG"])
                else:
                    logged = players_db.check_log(data[1], data[2])
                    if not logged:
                        send_msg(client_socket, ["WRNG"])
                    else:
                        send_msg(client_socket, ["IN"])

            elif data[0] == "REG":
                if data[1] in players_db.get_all_usernames():
                    send_msg(client_socket, ["TKN"])
                else:
                    players_db.add_player(data[1], data[2])
                    send_msg(client_socket, ["IN"])

            elif data[0] == "GPOINTS":
                points = players_db.get_points(data[1])
                send_msg(client_socket, ["POINTS", points])

            elif data[0] == "PIN":
                if data[1] in games.keys():
                    send_msg(client_socket, ["CONNECT", games[data[1]]])
                else:
                    send_msg(client_socket, ["WRNG"])

        except socket.error:
            pass


def handle_msg(client_socket, size):
    data = client_socket.recv(int(size))[1:]
    data = data.split("#")
    return data


def send_msg(client_socket, msg):
    data = "#" + "#".join(msg)
    data = str(len(data)).zfill(5) + data
    client_socket.send(data)


if __name__ == '__main__':
    main()
