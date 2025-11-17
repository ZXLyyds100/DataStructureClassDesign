import tkinter as tk
import random


def launch_console_window(parent):
    w = tk.Toplevel(parent)
    w.title('猜数字')
    w.geometry('450x300')
    w.config(bg="#1e1e2e")
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
        f = tk.Frame(self.root, bg="#1e1e2e")
        f.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        tk.Label(f, text=f'🎯 猜数字游戏', font=("Helvetica", 24, "bold"), fg="#cdd6f4", bg="#1e1e2e").pack(pady=(0,10))
        tk.Label(f, text=f'我想了一个 {self.low} 到 {self.high} 的数字', font=("Helvetica", 16), fg="#a6adc8", bg="#1e1e2e").pack(pady=(0,5))
        tk.Label(f, text='你能猜到吗？', font=("Helvetica", 14), fg="#a6adc8", bg="#1e1e2e").pack(pady=(0,20))

        entry = tk.Entry(f, font=("Helvetica", 18), width=12, justify="center", 
                         bg="#313244", fg="#cdd6f4", insertbackground="#cdd6f4", bd=0, relief=tk.FLAT)
        entry.pack(pady=6, ipady=8)
        self.entry = entry
        
        self.status = tk.Label(f, text='', font=("Helvetica", 14, "bold"), fg="#f9e2af", bg="#1e1e2e")
        self.status.pack(pady=15)

        btn_frame = tk.Frame(f, bg="#1e1e2e")
        btn_frame.pack(pady=10)

        guess_btn = tk.Button(btn_frame, text='🎲 猜！', font=("Helvetica", 13),
                              fg="#1e1e2e", bg="#a6e3a1", activebackground="#a6e3a1",
                              relief=tk.FLAT, bd=0, padx=15, pady=8, cursor="hand2", command=self.guess)
        guess_btn.pack(side=tk.LEFT, padx=5)

        reset_btn = tk.Button(btn_frame, text='🔄 重置', font=("Helvetica", 13),
                              fg="#1e1e2e", bg="#fab387", activebackground="#fab387",
                              relief=tk.FLAT, bd=0, padx=15, pady=8, cursor="hand2", command=self.reset)
        reset_btn.pack(side=tk.LEFT, padx=5)

    def guess(self):
        try:
            val = int(self.entry.get())
        except Exception:
            self.status.config(text='⚠️ 请输入有效的整数', fg="#f38ba8")
            return
            
        self.tries += 1
        if val == self.target:
            self.status.config(text=f'🎉 正确！你用了 {self.tries} 次', fg="#a6e3a1")
            self.entry.config(state=tk.DISABLED)
        elif val < self.target:
            self.status.config(text='📉 太小了，再试试！', fg="#89b4fa")
        else:
            self.status.config(text='📈 太大了，再试试！', fg="#fab387")

    def reset(self):
        self.target = random.randint(self.low, self.high)
        self.tries = 0
        self.entry.config(state=tk.NORMAL)
        self.entry.delete(0, tk.END)
        self.status.config(text='', fg="#f9e2af")
