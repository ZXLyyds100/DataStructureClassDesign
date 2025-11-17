import tkinter as tk
from tkinter import messagebox
import sys
import os

from games import tictactoe, guess_number, hangman, blackjack, memory, minesweeper, snake

APP_TITLE = "多游戏集合"


class Launcher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("700x600")
        self.config(bg="#1e1e2e")
        self._build_ui()

    def _build_ui(self):
        # Main container
        main_frame = tk.Frame(self, bg="#1e1e2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Title
        title = tk.Label(main_frame, text=APP_TITLE, font=("Helvetica", 36, "bold"), 
                        fg="#cdd6f4", bg="#1e1e2e")
        title.pack(pady=(10, 5))

        # Subtitle
        desc = tk.Label(main_frame, text="选择下面的游戏开始", font=("Helvetica", 14), 
                       fg="#a6adc8", bg="#1e1e2e")
        desc.pack(pady=(0, 30))

        # Buttons container
        btn_frame = tk.Frame(main_frame, bg="#1e1e2e")
        btn_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights for centering
        for i in range(4):
            btn_frame.grid_rowconfigure(i, weight=1)
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

        buttons = [
            ("🎮 井字棋", self.launch_tictactoe, "#f38ba8"),
            ("🔢 猜数字", self.launch_guess, "#fab387"),
            ("📝 猜单词", self.launch_hangman, "#f9e2af"),
            ("🃏 二十一点", self.launch_blackjack, "#a6e3a1"),
            ("🎴 记忆翻牌", self.launch_memory, "#89dceb"),
            ("💣 扫雷", self.launch_minesweeper, "#89b4fa"),
            ("🐍 贪吃蛇", self.launch_snake, "#cba6f7"),
        ]

        for i, (label, cmd, color) in enumerate(buttons):
            b = tk.Button(btn_frame, text=label, font=("Helvetica", 13, "bold"), 
                          fg="#1e1e2e", bg=color, activebackground=color, 
                          activeforeground="#11111b", relief=tk.FLAT, bd=0,
                          width=18, height=2, cursor="hand2", command=cmd)
            b.grid(row=i // 2, column=i % 2, padx=12, pady=10, sticky="ew")
            
            # Hover effects
            def on_enter(e, btn=b, clr=color):
                btn.config(bg=self._lighten_color(clr))
            def on_leave(e, btn=b, clr=color):
                btn.config(bg=clr)
            
            b.bind("<Enter>", on_enter)
            b.bind("<Leave>", on_leave)

        # Footer info
        info = tk.Label(main_frame, text="提示：点击游戏按钮即可开始 | 关闭子窗口不会退出主程序", 
                       font=("Helvetica", 10), fg="#6c7086", bg="#1e1e2e")
        info.pack(pady=(20, 10))

    def _lighten_color(self, hex_color):
        """让颜色变亮一点用于悬停效果"""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = min(255, int(r * 1.15))
        g = min(255, int(g * 1.15))
        b = min(255, int(b * 1.15))
        return f"#{r:02x}{g:02x}{b:02x}"

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
