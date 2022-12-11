import random
import socket
import tkFont
import ttk
import os
from tkinter import *
import time
import pickle

IP = "0.0.0.0"
PORT = 8000

S_IP = "127.0.0.1"
S_PORT = 5000

SOS = 5
ICON = "E:\\FinalProj\\icon.ico"
FONT = "TkDefaultFont"

QUIZZES_FOLDER = r"E:\\FinalProj\\Quizzes\\"

pins = []

started = False
ROUND_LEN = 15
WAIT_BEFORE = 5


def main():
    global window
    # Create the opening window
    window = Tk()
    window.title("Kahoot+")
    window.geometry("970x630")
    window.iconbitmap(ICON)
    window.resizable(0, 0)

    home_screen()

    window.mainloop()


def home_screen():
    for widget in window.winfo_children():
        widget.destroy()

    logo_var = StringVar()
    logo_var.set("Kahoot+")
    label = Label(window, textvariable=logo_var, font=('Helvetica', 75), fg="Purple")
    label.place(x=265, y=200)

    editor_btn = Button(window, text="Create A New Quiz", font=FONT, command=get_quiz_name, height=3, width=27)
    editor_btn.place(x=210, y=410)
    game_btn = Button(window, text="Start Playing", font=FONT, height=3, command=quiz_choosing, width=27)
    game_btn.place(x=480, y=410)


def quiz_choosing():
    for widget in window.winfo_children():
        widget.destroy()

    client_socket = socket.socket()
    client_socket.connect((S_IP, S_PORT))
    send_msg(client_socket, ["GQUIZZES"])

    size = client_socket.recv(SOS)
    data = handle_msg(client_socket, size)
    quizzes = data[1:]
    client_socket.close()

    for i in range(len(quizzes)):
        quizzes[i] = " ".join(quizzes[i].split("_"))

    quizzes_scroll = ttk.Scrollbar(window, orient=VERTICAL)
    quizzes_scroll.pack(side=RIGHT, fill=Y)

    my_list = Listbox(window, yscrollcommand=quizzes_scroll.set)
    for line in quizzes:
        my_list.insert(END, line)
    my_list.pack(side=LEFT, fill=BOTH)
    quizzes_scroll.config(command=my_list.yview)

    game_btn = Button(window, text="Choose quiz", font=FONT, height=3,
                      command=lambda: gather_players(quizzes[my_list.curselection()[0]]), width=27)
    game_btn.place(x=480, y=410)


def gather_players(quiz):
    global started
    for widget in window.winfo_children():
        widget.destroy()

    client_socket = socket.socket()
    client_socket.connect((S_IP, S_PORT))
    send_msg(client_socket, ["START"])

    size = client_socket.recv(SOS)
    data = handle_msg(client_socket, size)
    pin = data[1]

    server_socket = socket.socket()
    server_socket.bind((IP, PORT))
    server_socket.listen(10)
    server_socket.settimeout(0.001)

    pin_var = StringVar()
    pin_var.set("Game PIN: " + pin)
    label = Label(window, textvariable=pin_var, font=('Helvetica', 50), fg="purple")
    label.place(x=40, y=15)

    quiz_var = StringVar()
    quiz_var.set("Game Subject: " + quiz)
    label = Label(window, textvariable=quiz_var, font=('Helvetica', 30))
    label.place(x=40, y=95)

    name_var = StringVar()
    name_var.set("Players in:")
    label = Label(window, textvariable=name_var, font=('Helvetica', 20))
    label.place(x=40, y=155)

    players = {}
    game_btn = Button(window, text="Start Game", font=FONT, height=3, width=27,
                      command=lambda: start_game(client_socket, players))
    game_btn.place(x=700, y=60)

    y = 0
    while not started:
        window.update()
        try:
            phone_socket, phone_address = server_socket.accept()
            time.sleep(0.01)
            size = phone_socket.recv(SOS)
            if size != "":
                data = handle_msg(phone_socket, size)
                print data
                if data[0] == "NEW":
                    y += 50
                    players[data[1]] = [phone_socket, 0]
                    label = Label(window, text=data[1], font=('Helvetica', 25), fg="Purple")
                    label.place(x=40, y=200 + y)
        except socket.error:
            pass
    started = False
    # at this point when start game was pressed the players names and socket are in players{} and quiz name is in quiz
    client_socket = socket.socket()
    client_socket.connect((S_IP, S_PORT))
    send_msg(client_socket, ["GQUIZ", "_".join(quiz.split())])

    size = client_socket.recv(SOS)
    data = handle_msg(client_socket, size)
    quiz = data[1]
    quiz = pickle.loads(quiz)
    client_socket.close()

    print players
    game(players, quiz)


def game(players, quiz):
    """
    main game loop
    players = {player1:socket, player2:socket}
    quiz = {Q1:[A,WA1,WA2,WA3,WA4], Q2:[A,WA1,WA2,WA3,WA4]}
    """
    client_socket = socket.socket()
    client_socket.connect((S_IP, S_PORT))
    for q in quiz:
        for widget in window.winfo_children():
            widget.destroy()
        # shuffle the answers list
        answers = quiz[q]
        ra = answers[0]
        random.shuffle(answers)

        # remember the position of the right answer
        true_pos = int(answers.index(ra))

        # put the question on screen
        q_var = StringVar()
        q_var.set(q)
        label = Label(window, textvariable=q_var, font=('Helvetica', 35))
        label.place(x=5, y=15)

        # the label that wil be the timer
        timer_var = StringVar()
        timer_var.set(ROUND_LEN)
        label = Label(window, textvariable=timer_var, font=('Helvetica', 100), fg="Purple")
        label.place(x=750, y=100)

        my_font = tkFont.Font(family='Helvetica', size=15, weight=tkFont.BOLD)

        # put the possible answers on screen
        button1 = Button(window, text=answers[0], font=my_font, height=8, width=25, bg="Green")
        button1.place(x=50, y=200)

        button2 = Button(window, text=answers[1], font=my_font, height=8, width=25, bg="Red")
        button2.place(x=50, y=410)

        button3 = Button(window, text=answers[2], font=my_font, height=8, width=25, bg="Yellow")
        button3.place(x=360, y=200)

        button4 = Button(window, text=answers[3], font=my_font, height=8, width=25, bg="Blue")
        button4.place(x=360, y=410)

        #  will save the answer the player sent and the time he sent it
        cur_an = {}
        for player in players.keys():
            cur_an[player] = [4, 0]  # default values for if a players sends nothing (answer number 4 doesnt exist)

        broadcast(players, ["GO"])

        # round started, for ROUND_LEN seconds
        start = time.time()
        printed = ROUND_LEN + 1
        run = True
        while run:
            window.update()
            for player in players.keys():
                try:
                    size = players[player][0].recv(SOS)
                    if size != "":
                        data = handle_msg(players[player][0], size)
                        if data[0] == "AN":
                            cur_an[player][0] = int(data[1])  # save the player's answer
                            cur_an[player][1] = printed  # save the time that was left when he sent
                except socket.error:
                    pass

            seconds = int(time.time() - start)
            if printed != ROUND_LEN - seconds:  # handle the timer and show on screen the time that is left
                printed = ROUND_LEN - seconds
                timer_var.set(str(printed))
            elif printed == 0:
                run = False

        # round ended, tell players if they were right or not and add points
        for player in cur_an.keys():
            if int(cur_an[player][0]) == int(true_pos):
                send_msg(players[player][0], ["CORRECT"])
                players[player][1] += 50 + 2 * cur_an[player][1]
            else:
                send_msg(players[player][0], ["WRONG"])
        print players

        # 5 seconds for the players to see if they were right, the correct answer and top 3
        for widget in window.winfo_children():
            widget.destroy()
        top3 = []
        for player in players.keys():
            score = players[player][1]
            if len(top3) < 3:
                top3.append((player, score))
            else:
                min, a = min_top3(top3)
                if score > min:
                    top3[a] = (player, score)

        top3.sort(key=lambda x: x[1], reverse=True)

        cor = "Correct Answer Was: " + ra
        label = Label(window, text=cor, font=('Helvetica', 30), fg="Purple")
        label.place(x=10, y=10)

        label = Label(window, text="Top Players", font=('Helvetica', 40), fg="Blue")
        label.place(x=190, y=120)

        y = 0
        for i in range(len(top3)):
            cur = str(i + 1) + ".  " + top3[i][0] + " - " + str(top3[i][1]) + " points"
            label = Label(window, text=cur, font=('Helvetica', 40), fg="Red")
            label.place(x=190, y=220 + y)
            y += 100

        timer_var = StringVar()
        timer_var.set(WAIT_BEFORE)
        label = Label(window, textvariable=timer_var, font=('Helvetica', 85), fg="Purple")
        label.place(x=850, y=30)

        wait = True
        start = time.time()
        printed = WAIT_BEFORE + 1
        while wait:
            window.update()
            seconds = int(time.time() - start)
            if printed != WAIT_BEFORE - seconds:  # handle the timer and show on screen the time that is left
                printed = WAIT_BEFORE - seconds
                timer_var.set(str(printed))
            elif printed == 0:
                wait = False

    print "game over"

    # add the points for each player, tell them game is done and how much points they had, close their sockets
    for player in players.keys():
        points = str(players[player][1])
        try:
            send_msg(players[player][0], ["FIN", player, points])
            send_msg(client_socket, ["ADDPTO", player, points])
            players[player][0].close()
        except socket.error:
            pass

    client_socket.close()
    home_screen()


def broadcast(players, data):
    for un in players:
        send_msg(players[un][0], data)


def start_game(client_socket, players):
    global started
    if len(players.keys()) > -1:
        print "starting game"
        send_msg(client_socket, ["STOP"])
        client_socket.close()
        started = True


def editor(name):
    if len(name) > 0:
        for widget in window.winfo_children():
            widget.destroy()

        # connect to the server to add quizzes
        client_socket = socket.socket()
        client_socket.connect((S_IP, S_PORT))
        send_msg(client_socket, ["CREATE", name])

        next_question(client_socket)


def next_question(client_socket):
    # Create the screen to enter a new quiz, question by question
    q_var = StringVar()
    q_var.set("Enter A Question:")
    label = Label(window, textvariable=q_var, font=(FONT, 20))
    label.place(x=65, y=30)

    question_entry = Entry(window, font=(FONT, 20))
    question_entry.place(x=290, y=30)

    ra_var = StringVar()
    ra_var.set("Enter The Right Answer:")
    label = Label(window, textvariable=ra_var, font=(FONT, 20))
    label.place(x=65, y=130)

    ra_entry = Entry(window, font=(FONT, 20))
    ra_entry.place(x=390, y=130)

    wa_var = StringVar()
    wa_var.set("Enter 3 Wrong Answers:")
    label = Label(window, textvariable=wa_var, font=(FONT, 20))
    label.place(x=335, y=230)

    wa1_entry = Entry(window, font=(FONT, 20))
    wa1_entry.place(x=10, y=300)

    wa2_entry = Entry(window, font=(FONT, 20))
    wa2_entry.place(x=335, y=300)

    wa3_entry = Entry(window, font=(FONT, 20))
    wa3_entry.place(x=660, y=300)

    next_btn = Button(window, text="Add Question", font=FONT, command=lambda: new_question(client_socket,
                                                                                           question_entry.get(),
                                                                                           ra_entry.get(),
                                                                                           wa1_entry.get(),
                                                                                           wa2_entry.get(),
                                                                                           wa3_entry.get()),
                      height=3, width=27)
    next_btn.place(x=210, y=440)

    finish_btn = Button(window, text="Finish The Quiz", font=FONT, command=lambda: finish_editing(client_socket),
                        height=3, width=27)
    finish_btn.place(x=480, y=440)


def finish_editing(client_socket):
    client_socket.close()
    home_screen()


def new_question(client_socket, question, RAnswer, WAnswer1, WAnswer2, WAnswer3):
    send_msg(client_socket, ["ADD", question, RAnswer, WAnswer1, WAnswer2, WAnswer3])

    for widget in window.winfo_children():
        widget.destroy()

    next_question(client_socket)


def get_quiz_name():
    for widget in window.winfo_children():
        widget.destroy()

    var = StringVar()
    var.set("Enter A Name For Your Quiz:")
    label = Label(window, textvariable=var, font=(FONT, 22))
    label.place(x=200, y=180)

    name_entry = Entry(window, font=(FONT, 20))
    name_entry.place(x=210, y=240)

    submit_name_btn = Button(window, text="Submit", font=FONT, command=lambda: editor(name_entry.get()),
                             height=3, width=20)
    submit_name_btn.place(x=210, y=330)


def min_top3(top3):
    a = 0
    min = top3[0][1]
    for i in top3:
        if i[1] < min:
            a = i
            min = i[1]
    return min, a


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
