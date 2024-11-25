# src/player_interactions/humanGUI_player.py

import tkinter as tk

class HumanGUI:
    def __init__(self, name):
        self.name = name
        self.root = tk.Tk()
        self.root.title(f"Ходы игрока: {self.name}")
        self.move_entry = tk.Entry(self.root)
        self.move_entry.pack()
        self.move_button = tk.Button(self.root, text="Сделать ход", command=self.submit_move)
        self.move_button.pack()
        self.move = None

    def submit_move(self):
        self.move = self.move_entry.get()
        self.root.quit()  # Закрываем GUI после ввода

    def make_move(self, game_state):
        self.root.mainloop()  # Ожидаем ввода от пользователя
        return self.move

    def __str__(self):
        return self.name
