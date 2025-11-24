import tkinter as tk
import random
from ui_utils import ModernButton, THEME

def launch_console_window(parent):
    w = tk.Toplevel(parent)
    w.title('猜数字')
    w.geometry('450x350')
    w.config(bg=THEME['bg'])
    GuessNumberApp(w)


class GuessNumberApp:
    def __init__(self, root):
        self.root = root
        self.low = 1
        self.high = 100
        self.target = random.randint(self.low, self.high)
        self.tries = 0
        self._build()

    def _build(self):
        f = tk.Frame(self.root, bg=THEME['bg'])
        f.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        tk.Label(f, text=f'🎯 猜数字游戏', font=("Helvetica", 24, "bold"), fg=THEME['fg'], bg=THEME['bg']).pack(pady=(0,10))
        tk.Label(f, text=f'我想了一个 {self.low} 到 {self.high} 的数字', font=("Helvetica", 16), fg=THEME['subtext'], bg=THEME['bg']).pack(pady=(0,5))
        tk.Label(f, text='你能猜到吗？', font=("Helvetica", 14), fg=THEME['subtext'], bg=THEME['bg']).pack(pady=(0,20))

        entry = tk.Entry(f, font=("Helvetica", 18), width=12, justify="center", 
                         bg=THEME['surface'], fg=THEME['fg'], insertbackground=THEME['fg'], bd=0, relief=tk.FLAT)
        entry.pack(pady=6, ipady=8)
        self.entry = entry
        self.entry.bind('<Return>', lambda e: self.guess())
        
        self.status = tk.Label(f, text='', font=("Helvetica", 14, "bold"), fg=THEME['yellow'], bg=THEME['bg'])
        self.status.pack(pady=15)

        btn_frame = tk.Frame(f, bg=THEME['bg'])
        btn_frame.pack(pady=10)

        ModernButton(btn_frame, text='🎲 猜！', command=self.guess, bg_color=THEME['green']).pack(side=tk.LEFT, padx=5)
        ModernButton(btn_frame, text='🔄 重置', command=self.reset, bg_color=THEME['orange']).pack(side=tk.LEFT, padx=5)

    def guess(self):
        try:
            val = int(self.entry.get())
        except Exception:
            self.status.config(text='⚠️ 请输入有效的整数', fg=THEME['red'])
            return
            
        self.tries += 1
        if val == self.target:
            self.status.config(text=f'🎉 正确！你用了 {self.tries} 次', fg=THEME['green'])
            self.entry.config(state=tk.DISABLED)
        elif val < self.target:
            self.status.config(text='📉 太小了，再试试！', fg=THEME['blue'])
        else:
            self.status.config(text='📈 太大了，再试试！', fg=THEME['orange'])
        
        self.entry.delete(0, tk.END)

    def reset(self):
        self.target = random.randint(self.low, self.high)
        self.tries = 0
        self.entry.config(state=tk.NORMAL)
        self.entry.delete(0, tk.END)
        self.status.config(text='', fg=THEME['yellow'])
