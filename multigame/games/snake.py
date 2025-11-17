import tkinter as tk
import os


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
        
        # 尝试加载图片资源
        self.images = {}
        self._load_images()
        
        self._build()
        self.reset()
    
    def _load_images(self):
        """加载蛇头图片"""
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        image_path = os.path.join(base_path, 'images')
        
        # 只加载蛇头图片
        snake_img_path = os.path.join(image_path, '贪吃蛇.png')
        
        if os.path.exists(snake_img_path):
            try:
                # 加载原始图片
                original_img = tk.PhotoImage(file=snake_img_path)
                
                # 获取原始图片尺寸
                width = original_img.width()
                height = original_img.height()
                
                # 计算缩放比例以适应格子大小
                scale_x = max(1, width // self.cell)
                scale_y = max(1, height // self.cell)
                scale = max(scale_x, scale_y)
                
                # 缩放图片
                if scale > 1:
                    scaled_img = original_img.subsample(scale, scale)
                else:
                    scaled_img = original_img
                
                # 只用于蛇头
                self.images['snake_head'] = scaled_img
                
                print(f"✓ 成功加载蛇头图片: 贪吃蛇.png (缩放比例: 1/{scale})")
            except Exception as e:
                print(f"✗ 加载图片失败: {e}")
                self.images['snake_head'] = None
        else:
            print(f"✗ 未找到图片文件: 贪吃蛇.png")
            self.images['snake_head'] = None

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
            
            # 蛇头使用图片
            if i == 0 and self.images.get('snake_head'):
                self.canvas.create_image(x0 + self.cell//2, y0 + self.cell//2, 
                                        image=self.images['snake_head'])
            # 蛇头没有图片时用绿色方块
            elif i == 0:
                self.canvas.create_rectangle(x0, y0, x0 + self.cell, y0 + self.cell, 
                                            fill="#4ade80", outline="#1e1e2e", width=2)
            # 蛇身全部用纯绿色方块
            else:
                self.canvas.create_rectangle(x0, y0, x0 + self.cell, y0 + self.cell, 
                                            fill="#22c55e", outline="#1e1e2e", width=2)
            
        # Draw food - 使用苹果表情符号
        fx, fy = self.food
        x0, y0 = fx * self.cell, fy * self.cell
        self.canvas.create_text(x0 + self.cell//2, y0 + self.cell//2, 
                               text="🍎", font=("Arial", self.cell-2))
