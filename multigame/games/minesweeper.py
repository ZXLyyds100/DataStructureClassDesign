import tkinter as tk
import random


class MinesweeperApp:
    FLAG_ICON = None 
    MINE_ICON = None

    NUMBER_COLORS = {
        1: "#89b4fa", 2: "#a6e3a1", 3: "#f38ba8", 4: "#cba6f7",
        5: "#f9e2af", 6: "#89dceb", 7: "#fab387", 8: "#bac2de"
    }

    def __init__(self, root, rows=10, cols=10, mines=15):
        self.root = root
        self.root.title('扫雷')
        self.root.config(bg="#1e1e2e")
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.game_over_flag = False
        self._build()
        self.reset()

    def _build(self):
        f = tk.Frame(self.root, bg="#1e1e2e")
        f.pack(padx=10, pady=10)
        
        header = tk.Frame(f, bg="#1e1e2e")
        header.pack(pady=5)
        
        tk.Label(header, text="💣 扫雷", font=("Helvetica", 22, "bold"), fg="#cdd6f4", bg="#1e1e2e").pack()
        
        self.status = tk.Label(header, text="开始游戏", font=("Helvetica", 14), fg="#a6adc8", bg="#1e1e2e")
        self.status.pack(pady=5)
        
        tk.Button(header, text='🔄 重置', font=("Helvetica", 12), command=self.reset,
                  fg="#1e1e2e", bg="#fab387", activebackground="#fab387", 
                  relief=tk.FLAT, bd=0, padx=15, pady=5, cursor="hand2").pack(pady=5)

        self.board = tk.Frame(f, bg="#313244")
        self.board.pack(pady=10)
        
        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                b = tk.Button(self.board, width=2, height=1, font=("Helvetica", 10, "bold"),
                              bg="#45475a", activebackground="#f9e2af",
                              relief=tk.RAISED, bd=2, cursor="hand2",
                              command=lambda r=r, c=c: self.open_cell(r, c))
                b.bind('<Button-3>', lambda e, r=r, c=c: self.toggle_flag(r, c))
                b.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[r][c] = b

    def reset(self):
        self.game_over_flag = False
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flagged = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        
        coords = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        mine_locs = random.sample(coords, self.mines)
        
        for r, c in mine_locs:
            self.grid[r][c] = -1
            
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == -1: continue
                count = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        rr, cc = r + dr, c + dc
                        if 0 <= rr < self.rows and 0 <= cc < self.cols and self.grid[rr][cc] == -1:
                            count += 1
                self.grid[r][c] = count

        for r in range(self.rows):
            for c in range(self.cols):
                self.buttons[r][c].config(text='', state=tk.NORMAL, bg="#45475a", fg="#cdd6f4", relief=tk.RAISED)
        
        self.status.config(text='右键插旗，左键排雷', fg="#a6adc8")

    def toggle_flag(self, r, c):
        if self.game_over_flag or self.revealed[r][c]:
            return
        self.flagged[r][c] = not self.flagged[r][c]
        self.buttons[r][c].config(text='🚩' if self.flagged[r][c] else '', fg="#f38ba8")

    def open_cell(self, r, c):
        if self.game_over_flag or self.flagged[r][c] or self.revealed[r][c]:
            return
            
        self.revealed[r][c] = True
        self.buttons[r][c].config(relief=tk.SUNKEN, bg="#313244")

        if self.grid[r][c] == -1:
            self.buttons[r][c].config(text='💣', bg='#f38ba8', fg="#1e1e2e")
            self.game_over(False)
            return
            
        val = self.grid[r][c]
        if val > 0:
            self.buttons[r][c].config(text=str(val), fg=self.NUMBER_COLORS.get(val, "#cdd6f4"))
        else:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < self.rows and 0 <= cc < self.cols:
                        self.open_cell(rr, cc)
        
        if self._check_win():
            self.game_over(True)

    def _check_win(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] != -1 and not self.revealed[r][c]:
                    return False
        return True

    def game_over(self, won):
        self.game_over_flag = True
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == -1:
                    self.buttons[r][c].config(text='💣', bg='#585b70' if won else '#f38ba8')
        
        if won:
            self.status.config(text='🎉 恩喜你，全部清除！', fg="#a6e3a1")
        else:
            self.status.config(text='💥 游戏结束，踩到地雷了', fg="#f38ba8")

    def toggle_flag(self, r, c):
        if self.game_over_flag or self.revealed[r][c]:
            return
        self.flagged[r][c] = not self.flagged[r][c]
        self.buttons[r][c].config(text='🚩' if self.flagged[r][c] else '', fg="red")

    def open_cell(self, r, c):
        if self.game_over_flag or self.flagged[r][c] or self.revealed[r][c]:
            return
            
        self.revealed[r][c] = True
        self.buttons[r][c].config(relief=tk.SUNKEN, bg="#bdc3c7")

        if self.grid[r][c] == -1:
            self.buttons[r][c].config(text='💣', bg='red')
            self.game_over(False)
            return
            
        val = self.grid[r][c]
        if val > 0:
            self.buttons[r][c].config(text=str(val), fg=self.NUMBER_COLORS.get(val, "black"))
        else: # val is 0, open neighbors
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < self.rows and 0 <= cc < self.cols:
                        self.open_cell(rr, cc)
        
        if self._check_win():
            self.game_over(True)

    def _check_win(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] != -1 and not self.revealed[r][c]:
                    return False
        return True

    def game_over(self, won):
        self.game_over_flag = True
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == -1:
                    self.buttons[r][c].config(text='💣', bg='red' if not won else 'gray')
        
        if won:
            self.status.config(text='恭喜你，全部清除！', fg="#27ae60")
        else:
            self.status.config(text='游戏结束，踩到地雷了。', fg="#c0392b")
