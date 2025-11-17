import tkinter as tk


class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title('井字棋')
        self.root.geometry('450x520')
        self.root.config(bg="#1e1e2e")
        self.current = 'X'
        self.board = [None] * 9
        self.buttons = []
        self.winner_line = None
        self._build()

    def _build(self):
        top = tk.Frame(self.root, bg="#1e1e2e")
        top.pack(pady=(20, 10))
        label = tk.Label(top, text='井字棋 - 两人对战', font=("Helvetica", 20, "bold"), fg="#cdd6f4", bg="#1e1e2e")
        label.pack()

        grid = tk.Frame(self.root, bg="#1e1e2e")
        grid.pack(pady=10)

        for i in range(9):
            b = tk.Button(grid, text='', font=("Helvetica", 32, "bold"), width=4, height=2,
                          bg="#313244", fg="#cdd6f4", activebackground="#45475a",
                          relief=tk.FLAT, bd=2, highlightbackground="#585b70",
                          cursor="hand2", command=lambda i=i: self._on_click(i))
            b.grid(row=i // 3, column=i % 3, padx=3, pady=3)
            self.buttons.append(b)

        ctrl = tk.Frame(self.root, bg="#1e1e2e")
        ctrl.pack(pady=20)
        self.status = tk.Label(ctrl, text='当前: X', font=("Helvetica", 16), fg="#a6adc8", bg="#1e1e2e")
        self.status.pack(side=tk.LEFT, padx=15)
        
        reset_btn = tk.Button(ctrl, text='重置游戏', font=("Helvetica", 13), 
                              fg="#1e1e2e", bg="#f38ba8", activebackground="#f38ba8",
                              relief=tk.FLAT, bd=0, padx=15, pady=8, cursor="hand2", command=self.reset)
        reset_btn.pack(side=tk.LEFT, padx=10)

    def _on_click(self, idx):
        if self.board[idx] is not None or self.winner_line:
            return
            
        self.board[idx] = self.current
        self.buttons[idx].config(text=self.current, fg="#f38ba8" if self.current == 'X' else "#89b4fa")
        
        winner_info = self.check_winner()
        if winner_info:
            winner, line = winner_info
            self.status.config(text=f'🏆 胜利者: {winner}!', fg="#a6e3a1")
            self.highlight_winner(line)
            self.disable_all()
            return

        if all(v is not None for v in self.board):
            self.status.config(text='⚖️ 平局', fg="#f9e2af")
            return
            
        self.current = 'O' if self.current == 'X' else 'X'
        self.status.config(text=f'当前: {self.current}', fg="#a6adc8")

    def check_winner(self):
        lines = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6),
        ]
        for line in lines:
            a, b, c = line
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a], line
        return None

    def highlight_winner(self, line):
        self.winner_line = line
        for idx in line:
            self.buttons[idx].config(bg="#a6e3a1")

    def disable_all(self):
        self.winner_line = True
        for b in self.buttons:
            b.config(state=tk.DISABLED)

    def reset(self):
        self.current = 'X'
        self.board = [None] * 9
        self.winner_line = None
        for b in self.buttons:
            b.config(text='', state=tk.NORMAL, bg="#313244", fg="#cdd6f4")
        self.status.config(text='当前: X', fg="#a6adc8")
