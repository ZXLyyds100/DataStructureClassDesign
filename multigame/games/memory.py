import tkinter as tk
import random
import os
from ui_utils import ModernButton, THEME, ResourceManager

class MemoryApp:
    # 使用新的水果图片
    IMAGE_FILES = [
        'fruit_apple.png', 'fruit_banana.png', 'fruit_cherry.png', 'fruit_grape.png',
        'fruit_lemon.png', 'fruit_orange.png', 'fruit_pear.png', 'fruit_strawberry.png'
    ]
    CARD_BACK_IMAGE = 'card_back.png'

    COLORS = ['#f38ba8', '#fab387', '#f9e2af', '#a6e3a1', '#89dceb', '#89b4fa', '#cba6f7', '#f5c2e7']

    def __init__(self, root, rows=4, cols=4):
        self.root = root
        self.root.title('记忆翻牌')
        self.root.config(bg=THEME['bg'])
        self.rows = rows
        self.cols = cols
        
        self._load_images()
        self._build()
        self.reset()

    def _load_images(self):
        self.card_images = []
        self.use_images = False
        
        # 尝试加载卡背
        self.card_back = ResourceManager.get_image(self.CARD_BACK_IMAGE, (64, 64))
        
        if self.card_back:
            # 尝试加载所有卡片图片
            loaded_images = []
            for img_file in self.IMAGE_FILES:
                img = ResourceManager.get_image(img_file, (64, 64))
                if img:
                    loaded_images.append(img)
            
            if len(loaded_images) == len(self.IMAGE_FILES):
                self.card_images = loaded_images
                self.use_images = True

    def _build(self):
        f = tk.Frame(self.root, bg=THEME['bg'])
        f.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        tk.Label(f, text='🎴 记忆翻牌', font=("Helvetica", 22, "bold"), fg=THEME['fg'], bg=THEME['bg']).pack(pady=(0, 10))
        
        self.board_frame = tk.Frame(f, bg=THEME['bg'])
        self.board_frame.pack(pady=10)
        
        self.buttons = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                b = tk.Button(self.board_frame, text='', width=8, height=4, font=("Helvetica", 20, "bold"),
                              bg=THEME['surface'], activebackground=THEME['surface2'], relief=tk.FLAT, bd=2,
                              highlightbackground=THEME['overlay'], cursor="hand2",
                              command=lambda r=r, c=c: self.on_click(r, c))
                b.grid(row=r, column=c, padx=5, pady=5)
                row.append(b)
            self.buttons.append(row)
            
        ctrl = tk.Frame(f, bg=THEME['bg'])
        ctrl.pack(pady=10)
        
        self.status = tk.Label(ctrl, text='', font=("Helvetica", 14), fg=THEME['subtext'], bg=THEME['bg'])
        self.status.pack(side=tk.LEFT, padx=10)
        
        ModernButton(ctrl, text='🔄 重置', command=self.reset, bg_color=THEME['orange']).pack()

    def reset(self):
        n = self.rows * self.cols
        if n // 2 > len(self.COLORS) or (self.use_images and n // 2 > len(self.card_images)):
            raise ValueError("Not enough colors or images for the grid size")
            
        pairs = list(range(n // 2)) * 2
        random.shuffle(pairs)
        self.values = [pairs[i * self.cols:(i + 1) * self.cols] for i in range(self.rows)]
        self.revealed = [[False] * self.cols for _ in range(self.rows)]
        self.first = None
        self.locked = False
        self.matches = 0
        self.status['text'] = '翻开两张卡片进行配对'
        self._update_buttons()

    def _update_buttons(self):
        for r in range(self.rows):
            for c in range(self.cols):
                btn = self.buttons[r][c]
                if self.revealed[r][c]:
                    val = self.values[r][c]
                    if self.use_images:
                        btn.config(image=self.card_images[val], text="", state=tk.DISABLED)
                    else:
                        btn.config(bg=self.COLORS[val], text=str(val), state=tk.DISABLED, disabledforeground=THEME['bg'])
                else:
                    if self.use_images:
                        btn.config(image=self.card_back, text="", state=tk.NORMAL)
                    else:
                        btn.config(bg=THEME['surface'], text="", state=tk.NORMAL)

    def on_click(self, r, c):
        if self.locked or self.revealed[r][c]:
            return
            
        self.revealed[r][c] = True
        self._update_buttons()
        
        if self.first is None:
            self.first = (r, c)
            return
            
        r0, c0 = self.first
        if self.values[r0][c0] == self.values[r][c]:
            self.matches += 1
            if self.matches == (self.rows * self.cols) // 2:
                self.status.config(text='🎉 恩喜，全部配对成功！', fg=THEME['green'])
            self.first = None
        else:
            self.locked = True
            self.root.after(800, self._hide_pair, r0, c0, r, c)

    def _hide_pair(self, r0, c0, r1, c1):
        self.revealed[r0][c0] = False
        self.revealed[r1][c1] = False
        self.first = None
        self.locked = False
        self._update_buttons()
