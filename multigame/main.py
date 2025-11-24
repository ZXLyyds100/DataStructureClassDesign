import tkinter as tk
from tkinter import messagebox
import sys
import os

from games import tictactoe, guess_number, hangman, blackjack, memory, minesweeper, snake
from ui_utils import ModernButton, GameCard, THEME, center_window, ResourceManager

APP_TITLE = "多游戏集合"


class Launcher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("900x700")
        self.config(bg=THEME["bg"])
        center_window(self, 900, 700)
        self._build_ui()

    def _build_ui(self):
        # Main container
        main_frame = tk.Frame(self, bg=THEME["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        # Header Section
        header_frame = tk.Frame(main_frame, bg=THEME["bg"])
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Try to load icon
        icon_img = ResourceManager.get_image("game_controller.png", (80, 80))
        if icon_img:
            icon_lbl = tk.Label(header_frame, image=icon_img, bg=THEME["bg"])
            icon_lbl.image = icon_img # Keep reference
            icon_lbl.pack(side=tk.LEFT, padx=(0, 20))

        title_frame = tk.Frame(header_frame, bg=THEME["bg"])
        title_frame.pack(side=tk.LEFT, fill=tk.Y, expand=True)

        title = tk.Label(title_frame, text=APP_TITLE, font=("Helvetica", 36, "bold"), 
                        fg=THEME["fg"], bg=THEME["bg"], anchor="w")
        title.pack(fill=tk.X)

        desc = tk.Label(title_frame, text="选择下面的游戏开始您的挑战", font=("Helvetica", 16), 
                       fg=THEME["subtext"], bg=THEME["bg"], anchor="w")
        desc.pack(fill=tk.X, pady=(5, 0))

        # Games Grid container
        grid_frame = tk.Frame(main_frame, bg=THEME["bg"])
        grid_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        for i in range(3):
            grid_frame.grid_columnconfigure(i, weight=1)

        games = [
            ("井字棋", self.launch_tictactoe, "tictactoe.png"),
            ("猜数字", self.launch_guess, "guess_number.png"),
            ("猜单词", self.launch_hangman, "hangman.png"),
            ("二十一点", self.launch_blackjack, "blackjack.png"),
            ("记忆翻牌", self.launch_memory, "memory.png"),
            ("扫雷", self.launch_minesweeper, "mine.png"),
            ("贪吃蛇", self.launch_snake, "snake_head.png"),
        ]

        for i, (label, cmd, icon) in enumerate(games):
            card = GameCard(grid_frame, title=label, icon_name=icon, command=cmd)
            card.grid(row=i // 3, column=i % 3, padx=15, pady=15, sticky="nsew")

        # Footer info
        info = tk.Label(main_frame, text="提示：点击卡片即可开始 | 关闭子窗口不会退出主程序", 
                       font=("Helvetica", 12), fg=THEME["subtext"], bg=THEME["bg"])
        info.pack(side=tk.BOTTOM, pady=(20, 0))

    def launch_tictactoe(self):
        tictactoe.TicTacToeApp(tk.Toplevel(self))

    def launch_guess(self):
        guess_number.launch_console_window(self)

    def launch_hangman(self):
        hangman.HangmanApp(tk.Toplevel(self))

    def launch_blackjack(self):
        blackjack.BlackjackApp(tk.Toplevel(self))

    def launch_memory(self):
        memory.MemoryApp(tk.Toplevel(self))

    def launch_minesweeper(self):
        minesweeper.MinesweeperApp(tk.Toplevel(self))

    def launch_snake(self):
        snake.SnakeApp(tk.Toplevel(self))


def main():
    root = Launcher()
    root.mainloop()


if __name__ == '__main__':
    main()
