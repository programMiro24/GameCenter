import tkinter as tk
import angry_birds
import snake_game
import os
# import webbrowser # open website in browser

players = []
def write(player):
    filename = f"{player['name']}.txt"
    with open(filename, "w") as file:
        file.write(f"{player['score']}\n")

def read(name):
    filename = f"{name}.txt"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            score = int(file.readline().strip())
    else:
        score = 0
        with open(filename, "w") as file:
            file.write("0\n")
    return score

def player_info() -> dict:
    player_name = entry_name.get().strip()
    if player_name == '':
        player_name = "Player"
    if player_name not in players:
        players.append(player_name)
    player_score = read(player_name)
    return {'name': player_name, 'score': player_score}

def start_snake(level, window):
    player = player_info()
    if level == 'Easy':
        clock_fps = 5
    elif level == 'Medium':
        clock_fps = 10
    else:
        clock_fps = 15
    window.destroy()
    points = snake_game.run(player, clock_fps)
    if points > player['score']:
        player['score'] = points
    text = f"{player['name']}'s high score: {player['score']}"
    score_name.config(text = text)
    write(player)

def start_angry_birds():
    player = player_info()
    points = angry_birds.run(player)
    if points > player['score']:
        player['score'] = points
    text = f"{player['name']}'s high score: {player['score']}"
    score_name.config(text = text)
    write(player)

def leaderboard():
    srt = []
    for pl in players:
        srt.append({'name': pl, 'score': read(pl)})
    srt.sort(key=lambda x: x['score'], reverse=True)
    lb_window = tk.Toplevel(root)
    lb_window.title("Leaderboard")
    lb_window.geometry("300x400")
    number = 1
    for pl_dat in srt:
        name = pl_dat['name']
        score = pl_dat['score']
        tk.Label(lb_window, text=f"{number}. {name} - {score} points", font=("Arial", 14)).pack(pady=2)
        number += 1

def tutorial_snake(window):
    tutorial_window = tk.Toplevel(window)
    tutorial_window.title("Tutorial: Snake")
    username = player_info()['name']
    lbl_user = tk.Label(tutorial_window, text=f'Welcome, {username} to Snake!', font=("Arial", 15))
    lbl_user.pack(pady=5)
    lbl_green = tk.Label(tutorial_window, text="Green Apple(")

def hard():
    sl_window = tk.Toplevel(root)
    sl_window.title("Choose Level: Snake")
    sl_window.geometry("300x400")
    btn_easy = tk.Button(sl_window, text="Easy", width=20, command=lambda: start_snake("Easy", sl_window))
    btn_easy.pack(pady=5)
    btn_medium = tk.Button(sl_window, text="Medium", width=20, command=lambda: start_snake("Medium", sl_window))
    btn_medium.pack(pady=5)
    btn_hard = tk.Button(sl_window, text="Hard", width=20, command=lambda: start_snake("Hard", sl_window))
    btn_hard.pack(pady=5)
    btn_tutorial = tk.Button(sl_window, text="Tutorial", width=20, command=lambda: tutorial_snake(sl_window))
    btn_tutorial.pack()
    sl_window.mainloop()


root = tk.Tk()
root.title("Game Center")
root.geometry("420x420")

label_name = tk.Label(root, text="Enter your name: ", font=("Arial", 20))
label_name.pack()
entry_name = tk.Entry(root)
entry_name.pack(pady=5)

title = tk.Label(root, text="Choose game", fg="black", bg="white")
title.pack(pady=20)

snake = tk.PhotoImage(file="assets/assets_snake/assets/snake.png").zoom(4,4)
btn_snake = tk.Button(root, text="Snake", compound="top", command=hard, image=snake)
btn_snake.pack(pady=5)

angrys = tk.PhotoImage(file="assets/assets_angry_birds/angry-birds.png")
btn_angrys = tk.Button(root, text="Angry Birds", image=angrys, compound="top", command=start_angry_birds)
btn_angrys.image = angrys  # keep reference
btn_angrys.pack(pady=5)

btn_leaderboard = tk.Button(root, text="Leaderboard", command=leaderboard, width=20)
btn_leaderboard.pack(pady=5)

btn_exit = tk.Button(root, text="Exit", width = 20, command=root.quit)
btn_exit.pack(pady=5)

score_name = tk.Label(root, text=f"Welcome to the Game Center!", font=("Arial", 15))
score_name.pack()

root.mainloop()
