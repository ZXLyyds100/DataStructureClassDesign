import tkinter as tk
import random
from ui_utils import ModernButton, THEME

WORDS = [
    'python', 'hangman', 'computer', 'university', 'program', 'algorithm', 'structure', 'variable', 'function'
]


class HangmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title('猜单词')
        self.root.geometry('600x550')
        self.root.config(bg=THEME['bg'])
        self.max_wrong = 7
        self._new_game()
        self._build()

    def _new_game(self):
        self.word = random.choice(WORDS)
        self.guessed = set()
        self.wrong = 0
        self.game_over = False

    def _build(self):
        main_frame = tk.Frame(self.root, bg=THEME['bg'])
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        title = tk.Label(main_frame, text='📝 猜单词 (Hangman)', font=("Helvetica", 22, "bold"), fg=THEME['fg'], bg=THEME['bg'])
        title.pack(pady=(0, 10))

        self.canvas = tk.Canvas(main_frame, width=200, height=250, bg=THEME['surface'], highlightthickness=0)
        self.canvas.pack(pady=10)

        self.word_var = tk.StringVar()
        word_label = tk.Label(main_frame, textvariable=self.word_var, font=("Courier", 28, "bold"), fg=THEME['yellow'], bg=THEME['bg'])
        word_label.pack(pady=10)
        self._update_word()

        self.status = tk.Label(main_frame, text=f'❤️ 剩余机会: {self.max_wrong - self.wrong}', font=("Helvetica", 14), fg=THEME['subtext'], bg=THEME['bg'])
        self.status.pack(pady=5)

        entry_frame = tk.Frame(main_frame, bg=THEME['bg'])
        entry_frame.pack(pady=10)

        self.entry = tk.Entry(entry_frame, font=("Helvetica", 16), width=5, justify="center", 
                                bg=THEME['surface'], fg=THEME['fg'], insertbackground=THEME['fg'], bd=0, relief=tk.FLAT)
        self.entry.pack(side=tk.LEFT, padx=5, ipady=5)
        self.entry.focus_set()
        self.entry.bind('<Return>', lambda e: self.guess_letter())

        ModernButton(entry_frame, text='猜', command=self.guess_letter, bg_color=THEME['green']).pack(side=tk.LEFT, padx=5)

        ModernButton(main_frame, text='🔄 新游戏', command=self.reset, bg_color=THEME['orange']).pack(pady=10)
        
        self.draw_hangman()

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
                self.status.config(text='🎉 恩喜你，赢了！', fg=THEME['green'])
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
        # Gallow
        self.canvas.create_line(50, 220, 150, 220, fill=THEME['fg'], width=3)
        self.canvas.create_line(100, 220, 100, 50, fill=THEME['fg'], width=3)
        self.canvas.create_line(100, 50, 150, 50, fill=THEME['fg'], width=3)
        self.canvas.create_line(150, 50, 150, 80, fill=THEME['fg'], width=2)

        if self.wrong > 0:
            self.canvas.create_oval(135, 80, 165, 110, outline=THEME['yellow'], width=3)
        if self.wrong > 1:
            self.canvas.create_line(150, 110, 150, 160, fill=THEME['yellow'], width=3)
        if self.wrong > 2:
            self.canvas.create_line(150, 120, 120, 140, fill=THEME['yellow'], width=3)
        if self.wrong > 3:
            self.canvas.create_line(150, 120, 180, 140, fill=THEME['yellow'], width=3)
        if self.wrong > 4:
            self.canvas.create_line(150, 160, 120, 190, fill=THEME['yellow'], width=3)
        if self.wrong > 5:
            self.canvas.create_line(150, 160, 180, 190, fill=THEME['yellow'], width=3)
        if self.wrong > 6:
            self.canvas.create_line(145, 90, 150, 95, fill=THEME['red'], width=2)
            self.canvas.create_line(150, 90, 145, 95, fill=THEME['red'], width=2)
            self.canvas.create_line(155, 90, 160, 95, fill=THEME['red'], width=2)
            self.canvas.create_line(160, 90, 155, 95, fill=THEME['red'], width=2)

    def end_game(self):
        self.game_over = True
        self.entry.config(state=tk.DISABLED)
        # self.guess_btn.config(state=tk.DISABLED) # ModernButton doesn't support state config easily yet, or we need to implement it. 
        # Actually ModernButton inherits from tk.Button or tk.Label? No, it's a Frame with a Label.
        # Let's check ModernButton implementation.
        # If ModernButton is a Frame, we can't just config state.
        # But for now, let's just leave it enabled but logic locked.

    def reset(self):
        self._new_game()
        self._update_word()
        self.entry.config(state=tk.NORMAL)
        # self.guess_btn.config(state=tk.NORMAL)
        self.entry.delete(0, tk.END)
        self.status.config(text=f'❤️ 剩余机会: {self.max_wrong - self.wrong}', fg=THEME['subtext'])
        self.draw_hangman()
