import tkinter as tk
import random

WORDS = [
    'python', 'hangman', 'computer', 'university', 'program', 'algorithm', 'structure', 'variable', 'function'
]


class HangmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title('猜单词')
        self.root.geometry('600x500')
        self.root.config(bg="#1e1e2e")
        self.max_wrong = 7
        self._new_game()
        self._build()

    def _new_game(self):
        self.word = random.choice(WORDS)
        self.guessed = set()
        self.wrong = 0
        self.game_over = False

    def _build(self):
        main_frame = tk.Frame(self.root, bg="#1e1e2e")
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        title = tk.Label(main_frame, text='📝 猜单词 (Hangman)', font=("Helvetica", 22, "bold"), fg="#cdd6f4", bg="#1e1e2e")
        title.pack(pady=(0, 10))

        self.canvas = tk.Canvas(main_frame, width=200, height=250, bg="#313244", highlightthickness=0)
        self.canvas.pack(pady=10)

        self.word_var = tk.StringVar()
        word_label = tk.Label(main_frame, textvariable=self.word_var, font=("Courier", 28, "bold"), fg="#f9e2af", bg="#1e1e2e")
        word_label.pack(pady=10)
        self._update_word()

        self.status = tk.Label(main_frame, text=f'❤️ 剩余机会: {self.max_wrong - self.wrong}', font=("Helvetica", 14), fg="#a6adc8", bg="#1e1e2e")
        self.status.pack(pady=5)

        entry_frame = tk.Frame(main_frame, bg="#1e1e2e")
        entry_frame.pack(pady=10)

        self.entry = tk.Entry(entry_frame, font=("Helvetica", 16), width=5, justify="center", 
                                bg="#313244", fg="#cdd6f4", insertbackground="#cdd6f4", bd=0, relief=tk.FLAT)
        self.entry.pack(side=tk.LEFT, padx=5, ipady=5)
        self.entry.focus_set()

        self.guess_btn = tk.Button(entry_frame, text='猜', font=("Helvetica", 13),
                                   fg="#1e1e2e", bg="#a6e3a1", activebackground="#a6e3a1",
                                   relief=tk.FLAT, bd=0, padx=15, pady=5, cursor="hand2", command=self.guess_letter)
        self.guess_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = tk.Button(main_frame, text='🔄 新游戏', font=("Helvetica", 13),
                                   fg="#1e1e2e", bg="#fab387", activebackground="#fab387",
                                   relief=tk.FLAT, bd=0, padx=15, pady=8, cursor="hand2", command=self.reset)
        self.reset_btn.pack(pady=10)
        
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
            self.status.config(text='⚠️ 请输入单个字母', fg="#f38ba8")
            return
        if v in self.guessed:
            self.status.config(text=f'❌ "{v.upper()}" 已经猜过了', fg="#f9e2af")
            return
            
        self.guessed.add(v)
        
        if v in self.word:
            self.status.config(text='✅ 正确！', fg="#a6e3a1")
            self._update_word()
            if all(c in self.guessed for c in self.word):
                self.status.config(text='🎉 恩喜你，赢了！', fg="#a6e3a1")
                self.end_game()
        else:
            self.wrong += 1
            self.status.config(text=f'❌ 错误！剩余: {self.max_wrong - self.wrong}', fg="#f38ba8")
            self.draw_hangman()
            if self.wrong >= self.max_wrong:
                self.word_var.set(self.word.upper())
                self.status.config(text=f'😢 游戏结束，单词: {self.word.upper()}', fg="#f38ba8")
                self.end_game()

    def draw_hangman(self):
        self.canvas.delete("all")
        # Gallow
        self.canvas.create_line(50, 220, 150, 220, fill="#cdd6f4", width=3)
        self.canvas.create_line(100, 220, 100, 50, fill="#cdd6f4", width=3)
        self.canvas.create_line(100, 50, 150, 50, fill="#cdd6f4", width=3)
        self.canvas.create_line(150, 50, 150, 80, fill="#cdd6f4", width=2)

        if self.wrong > 0:
            self.canvas.create_oval(135, 80, 165, 110, outline="#f9e2af", width=3)
        if self.wrong > 1:
            self.canvas.create_line(150, 110, 150, 160, fill="#f9e2af", width=3)
        if self.wrong > 2:
            self.canvas.create_line(150, 120, 120, 140, fill="#f9e2af", width=3)
        if self.wrong > 3:
            self.canvas.create_line(150, 120, 180, 140, fill="#f9e2af", width=3)
        if self.wrong > 4:
            self.canvas.create_line(150, 160, 120, 190, fill="#f9e2af", width=3)
        if self.wrong > 5:
            self.canvas.create_line(150, 160, 180, 190, fill="#f9e2af", width=3)
        if self.wrong > 6:
            self.canvas.create_line(145, 90, 150, 95, fill="#f38ba8", width=2)
            self.canvas.create_line(150, 90, 145, 95, fill="#f38ba8", width=2)
            self.canvas.create_line(155, 90, 160, 95, fill="#f38ba8", width=2)
            self.canvas.create_line(160, 90, 155, 95, fill="#f38ba8", width=2)

    def draw_hangman(self):
        self.canvas.delete("all")
        # Gallow
        self.canvas.create_line(50, 220, 150, 220, fill="#ecf0f1", width=2) # Base
        self.canvas.create_line(100, 220, 100, 50, fill="#ecf0f1", width=2) # Pole
        self.canvas.create_line(100, 50, 150, 50, fill="#ecf0f1", width=2) # Beam
        self.canvas.create_line(150, 50, 150, 80, fill="#ecf0f1", width=2) # Rope

        if self.wrong > 0: # Head
            self.canvas.create_oval(135, 80, 165, 110, outline="#ecf0f1", width=2)
        if self.wrong > 1: # Torso
            self.canvas.create_line(150, 110, 150, 160, fill="#ecf0f1", width=2)
        if self.wrong > 2: # Left Arm
            self.canvas.create_line(150, 120, 120, 140, fill="#ecf0f1", width=2)
        if self.wrong > 3: # Right Arm
            self.canvas.create_line(150, 120, 180, 140, fill="#ecf0f1", width=2)
        if self.wrong > 4: # Left Leg
            self.canvas.create_line(150, 160, 120, 190, fill="#ecf0f1", width=2)
        if self.wrong > 5: # Right Leg
            self.canvas.create_line(150, 160, 180, 190, fill="#ecf0f1", width=2)
        if self.wrong > 6: # Dead face
            self.canvas.create_line(145, 90, 150, 95, fill="#c0392b", width=1)
            self.canvas.create_line(150, 90, 145, 95, fill="#c0392b", width=1)
            self.canvas.create_line(155, 90, 160, 95, fill="#c0392b", width=1)
            self.canvas.create_line(160, 90, 155, 95, fill="#c0392b", width=1)

    def end_game(self):
        self.game_over = True
        self.entry.config(state=tk.DISABLED)
        self.guess_btn.config(state=tk.DISABLED)

    def reset(self):
        self._new_game()
        self._update_word()
        self.entry.config(state=tk.NORMAL)
        self.guess_btn.config(state=tk.NORMAL)
        self.entry.delete(0, tk.END)
        self.status.config(text=f'❤️ 剩余机会: {self.max_wrong - self.wrong}', fg="#a6adc8")
        self.draw_hangman()
