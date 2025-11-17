import tkinter as tk


class SnakeApp:
    def __init__(self, root, width=500, height=500, cell=25):
        self.root = root
        self.root.title('贪吃蛇')
        self.root.config(bg="#1e1e2e")
        self.width = width
        self.height = height
        self.cell = cell
        self.cols = width // cell
        self.rows = height // cell
        self._build()
        self.reset()

    def _build(self):
        f = tk.Frame(self.root, bg="#1e1e2e")
        f.pack(padx=10, pady=10)

        tk.Label(f, text="🐍 贪吃蛇", font=("Helvetica", 24, "bold"), fg="#cdd6f4", bg="#1e1e2e").pack(pady=(0, 5))

        header = tk.Frame(f, bg="#1e1e2e")
        header.pack(pady=5, fill=tk.X)
        self.score_var = tk.StringVar()
        tk.Label(header, textvariable=self.score_var, font=("Helvetica", 16, "bold"), fg="#a6e3a1", bg="#1e1e2e").pack()
        
        self.canvas = tk.Canvas(f, width=self.width, height=self.height, bg='#313244', highlightthickness=0)
        self.canvas.pack(pady=10)
        
        self.status_var = tk.StringVar()
        tk.Label(f, textvariable=self.status_var, font=("Helvetica", 14), fg="#a6adc8", bg="#1e1e2e").pack(pady=5)

        tk.Button(f, text='🔄 开始 / 重置', font=("Helvetica", 13), command=self.reset,
                  fg="#1e1e2e", bg="#89b4fa", activebackground="#89b4fa", relief=tk.FLAT, bd=0, padx=15, pady=8, cursor="hand2").pack(pady=10)

        self.root.bind('<Up>', lambda e: self.change_dir((0, -1)))
        self.root.bind('<Down>', lambda e: self.change_dir((0, 1)))
        self.root.bind('<Left>', lambda e: self.change_dir((-1, 0)))
        self.root.bind('<Right>', lambda e: self.change_dir((1, 0)))
        self.root.focus_set()

    def reset(self):
        self.direction = (1, 0)
        self.snake = [(self.cols // 4, self.rows // 2)]
        self.spawn_food()
        self.running = True
        self.score = 0
        self.update_score()
        self.status_var.set("⌨️ 使用方向键移动")
        if hasattr(self, '_loop_id'):
            self.root.after_cancel(self._loop_id)
        self._loop()

    def spawn_food(self):
        import random
        while True:
            p = (random.randint(0, self.cols - 1), random.randint(0, self.rows - 1))
            if p not in self.snake:
                self.food = p
                return

    def change_dir(self, d):
        if not self.running: return
        if len(self.snake) > 1 and (d[0] == -self.direction[0] and d[1] == -self.direction[1]):
            return
        self.direction = d

    def _loop(self):
        if not self.running:
            return
            
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        if not (0 <= new_head[0] < self.cols and 0 <= new_head[1] < self.rows):
            self.game_over()
            return
        
        if new_head in self.snake:
            self.game_over()
            return
            
        self.snake.insert(0, new_head)
        
        if new_head == self.food:
            self.score += 1
            self.update_score()
            self.spawn_food()
        else:
            self.snake.pop()
            
        self._draw()
        self._loop_id = self.root.after(100, self._loop)

    def game_over(self):
        self.running = False
        self.status_var.set(f'💀 游戏结束！最终得分: {self.score}')
        self.canvas.create_text(self.width/2, self.height/2, text="GAME OVER",
                                font=("Helvetica", 36, "bold"), fill="#f38ba8")

    def update_score(self):
        self.score_var.set(f'🏆 得分: {self.score}')

    def _draw(self):
        self.canvas.delete('all')
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            x0, y0 = x * self.cell, y * self.cell
            color = "#a6e3a1" if i == 0 else "#89b4fa"
            self.canvas.create_rectangle(x0, y0, x0 + self.cell, y0 + self.cell, fill=color, outline="#1e1e2e", width=2)
            
        # Draw food
        fx, fy = self.food
        x0, y0 = fx * self.cell, fy * self.cell
        self.canvas.create_oval(x0+2, y0+2, x0 + self.cell-2, y0 + self.cell-2, fill='#f38ba8', outline="#f38ba8")
