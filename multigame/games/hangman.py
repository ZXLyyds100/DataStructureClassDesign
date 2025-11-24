import tkinter as tk
import random
from ui_utils import ModernButton, THEME, ResourceManager

# 单词与对应图片的映射
WORD_DATA = [
    ('apple', 'fruit_apple.png'),
    ('banana', 'fruit_banana.png'),
    ('cherry', 'fruit_cherry.png'),
    ('grape', 'fruit_grape.png'),
    ('lemon', 'fruit_lemon.png'),
    ('orange', 'fruit_orange.png'),
    ('pear', 'fruit_pear.png'),
    ('strawberry', 'fruit_strawberry.png'),
    ('watermelon', 'fruit_watermelon.png'),
    ('pineapple', 'fruit_pineapple.png'),
]

class HangmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title('猜单词')
        self.root.geometry('700x650')
        self.root.config(bg=THEME['bg'])
        self.max_wrong = 7
        self._new_game()
        self._build()

    def _new_game(self):
        self.word, self.image_file = random.choice(WORD_DATA)
        self.guessed = set()
        self.wrong = 0
        self.game_over = False

    def _build(self):
        main_frame = tk.Frame(self.root, bg=THEME['bg'])
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        title = tk.Label(main_frame, text='📝 看图猜单词', font=("Helvetica", 24, "bold"), fg=THEME['fg'], bg=THEME['bg'])
        title.pack(pady=(0, 15))

        # 游戏区域：左边是图片，右边是 Hangman
        game_area = tk.Frame(main_frame, bg=THEME['bg'])
        game_area.pack(pady=10)

        # 左侧：单词图片
        self.img_label = tk.Label(game_area, bg=THEME['surface'], width=200, height=200)
        self.img_label.pack(side=tk.LEFT, padx=20)
        self._update_image()

        # 右侧：Hangman 画布
        self.canvas = tk.Canvas(game_area, width=200, height=250, bg=THEME['surface'], highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, padx=20)
        self.draw_hangman()

        # 单词显示
        self.word_var = tk.StringVar()
        word_label = tk.Label(main_frame, textvariable=self.word_var, font=("Courier", 32, "bold"), fg=THEME['yellow'], bg=THEME['bg'])
        word_label.pack(pady=20)
        self._update_word()

        self.status = tk.Label(main_frame, text=f'❤️ 剩余机会: {self.max_wrong - self.wrong}', font=("Helvetica", 16), fg=THEME['subtext'], bg=THEME['bg'])
        self.status.pack(pady=5)

        # 输入区域
        entry_frame = tk.Frame(main_frame, bg=THEME['bg'])
        entry_frame.pack(pady=15)

        self.entry = tk.Entry(entry_frame, font=("Helvetica", 18), width=5, justify="center", 
                                bg=THEME['surface'], fg=THEME['fg'], insertbackground=THEME['fg'], bd=0, relief=tk.FLAT)
        self.entry.pack(side=tk.LEFT, padx=10, ipady=5)
        self.entry.focus_set()
        self.entry.bind('<Return>', lambda e: self.guess_letter())

        ModernButton(entry_frame, text='猜', command=self.guess_letter, bg_color=THEME['green']).pack(side=tk.LEFT, padx=10)

        ModernButton(main_frame, text='🔄 新游戏', command=self.reset, bg_color=THEME['orange']).pack(pady=10)

    def _update_image(self):
        img = ResourceManager.get_image(self.image_file, (180, 180))
        if img:
            self.img_label.config(image=img, width=200, height=200)
            self.img_label.image = img
        else:
            self.img_label.config(text="图片加载失败", fg=THEME['red'])

    def _update_word(self):
        s = ' '.join(c.upper() if c in self.guessed else '_' for c in self.word)
        self.word_var.set(s)

    def guess_letter(self):
        if self.game_over:
            return
            
        v = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)

        if not v or len(v) != 1 or not v.isalpha():
            self.status.config(text='⚠️ 请输入单个字母', fg=THEME['red'])
            return
        if v in self.guessed:
            self.status.config(text=f'❌ "{v.upper()}" 已经猜过了', fg=THEME['yellow'])
            return
            
        self.guessed.add(v)
        
        if v in self.word:
            self.status.config(text='✅ 正确！', fg=THEME['green'])
            self._update_word()
            if all(c in self.guessed for c in self.word):
                self.status.config(text='🎉 恭喜你，赢了！', fg=THEME['green'])
                self.end_game()
        else:
            self.wrong += 1
            self.status.config(text=f'❌ 错误！剩余: {self.max_wrong - self.wrong}', fg=THEME['red'])
            self.draw_hangman()
            if self.wrong >= self.max_wrong:
                self.word_var.set(self.word.upper())
                self.status.config(text=f'😢 游戏结束，单词: {self.word.upper()}', fg=THEME['red'])
                self.end_game()

    def draw_hangman(self):
        self.canvas.delete("all")
        # 绘制更精致的绞刑架
        self.canvas.create_line(40, 230, 160, 230, fill=THEME['fg'], width=4, capstyle=tk.ROUND) # Base
        self.canvas.create_line(100, 230, 100, 40, fill=THEME['fg'], width=4, capstyle=tk.ROUND) # Pole
        self.canvas.create_line(100, 40, 150, 40, fill=THEME['fg'], width=4, capstyle=tk.ROUND) # Beam
        self.canvas.create_line(150, 40, 150, 70, fill=THEME['fg'], width=3) # Rope

        # 绘制火柴人 (根据错误次数)
        if self.wrong > 0: # Head
            self.canvas.create_oval(135, 70, 165, 100, outline=THEME['yellow'], width=3)
        if self.wrong > 1: # Body
            self.canvas.create_line(150, 100, 150, 160, fill=THEME['yellow'], width=3)
        if self.wrong > 2: # Left Arm
            self.canvas.create_line(150, 110, 120, 140, fill=THEME['yellow'], width=3, capstyle=tk.ROUND)
        if self.wrong > 3: # Right Arm
            self.canvas.create_line(150, 110, 180, 140, fill=THEME['yellow'], width=3, capstyle=tk.ROUND)
        if self.wrong > 4: # Left Leg
            self.canvas.create_line(150, 160, 120, 200, fill=THEME['yellow'], width=3, capstyle=tk.ROUND)
        if self.wrong > 5: # Right Leg
            self.canvas.create_line(150, 160, 180, 200, fill=THEME['yellow'], width=3, capstyle=tk.ROUND)
        if self.wrong > 6: # Dead Eyes
            self.canvas.create_line(143, 80, 148, 85, fill=THEME['red'], width=2)
            self.canvas.create_line(148, 80, 143, 85, fill=THEME['red'], width=2)
            self.canvas.create_line(153, 80, 158, 85, fill=THEME['red'], width=2)
            self.canvas.create_line(158, 80, 153, 85, fill=THEME['red'], width=2)

    def end_game(self):
        self.game_over = True
        self.entry.config(state=tk.DISABLED)

    def reset(self):
        self._new_game()
        self._update_image()
        self._update_word()
        self.entry.config(state=tk.NORMAL)
        self.entry.delete(0, tk.END)
        self.status.config(text=f'❤️ 剩余机会: {self.max_wrong - self.wrong}', fg=THEME['subtext'])
        self.draw_hangman()
