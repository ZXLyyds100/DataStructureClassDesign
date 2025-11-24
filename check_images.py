import tkinter as tk
import os

root = tk.Tk()
base_path = os.path.join(os.getcwd(), 'multigame', 'images')
files = ['card_0.png', 'card_1.png', 'card_2.png', 'card_3.png', 'card_4.png', 'card_5.png', 'card_6.png', 'card_7.png']

print(f"Checking images in {base_path}...")

for f in files:
    p = os.path.join(base_path, f)
    if not os.path.exists(p):
        print(f"MISSING: {f}")
        continue
    
    try:
        img = tk.PhotoImage(file=p)
        print(f"OK: {f} ({img.width()}x{img.height()})")
    except Exception as e:
        print(f"ERROR: {f} - {e}")

root.destroy()
