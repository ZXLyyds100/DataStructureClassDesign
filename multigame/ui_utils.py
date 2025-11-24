import tkinter as tk
from tkinter import font
import os

# -----------------------------------------------------------------------------
# 颜色主题配置
# -----------------------------------------------------------------------------
THEME = {
    # 兼容旧键名 (main.py 使用)
    "bg_primary": "#1e1e2e",      # 深色背景
    "bg_secondary": "#313244",    # 次级背景
    "accent": "#89b4fa",          # 强调色 (蓝)
    "accent_hover": "#b4befe",    # 强调色悬停
    "text_primary": "#cdd6f4",    # 主要文字
    "text_secondary": "#a6adc8",  # 次要文字
    "success": "#a6e3a1",         # 成功 (绿)
    "warning": "#f9e2af",         # 警告 (黄)
    "danger": "#f38ba8",          # 危险 (红)
    "card_bg": "#cdd6f4",         # 卡片背景

    # 新键名 (游戏文件使用 - Catppuccin Mocha 风格)
    "bg": "#1e1e2e",
    "fg": "#cdd6f4",
    "surface": "#313244",
    "surface2": "#45475a",
    "overlay": "#585b70",
    "subtext": "#a6adc8",
    "red": "#f38ba8",
    "green": "#a6e3a1",
    "yellow": "#f9e2af",
    "blue": "#89b4fa",
    "orange": "#fab387",
    "purple": "#cba6f7",
}

# -----------------------------------------------------------------------------
# 资源管理
# -----------------------------------------------------------------------------
class ResourceManager:
    _images = {}
    
    @classmethod
    def get_image(cls, filename, size=None):
        """
        获取并缓存图片，支持自动缩放
        :param filename: 图片文件名 (在 images/ 目录下)
        :param size: (width, height) 元组，如果提供则缩放图片
        :return: tk.PhotoImage 对象 或 None
        """
        key = (filename, size)
        if key in cls._images:
            return cls._images[key]
            
        base_path = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(base_path, 'images', filename)
        
        if not os.path.exists(img_path):
            return None
            
        try:
            img = tk.PhotoImage(file=img_path)
            
            if size:
                # 简单的缩放算法 (subsample)
                # 注意: PhotoImage 的缩放比较基础，只能整数倍缩小
                # 如果需要高质量缩放，通常需要 PIL (Pillow)，但为了保持无依赖，这里用基础方法
                w, h = img.width(), img.height()
                target_w, target_h = size
                
                scale_w = max(1, w // target_w)
                scale_h = max(1, h // target_h)
                scale = min(scale_w, scale_h)
                
                if scale > 1:
                    img = img.subsample(scale, scale)
            
            cls._images[key] = img
            return img
        except Exception as e:
            print(f"Error loading image {filename}: {e}")
            return None

# -----------------------------------------------------------------------------
# UI 组件封装
# -----------------------------------------------------------------------------
class ModernButton(tk.Button):
    """现代风格按钮，支持悬停效果"""
    def __init__(self, master, text, command=None, type="primary", bg_color=None, **kwargs):
        
        if bg_color:
            final_bg = bg_color
            final_hover = bg_color # 简化处理，或者可以稍微变亮/变暗
            final_fg = THEME["bg"] # 假设彩色按钮用深色文字，或者根据颜色亮度判断
            if bg_color in [THEME['bg'], THEME['surface'], THEME['surface2']]:
                final_fg = THEME['fg']
        else:
            final_bg = THEME["accent"]
            final_fg = THEME["bg"]
            final_hover = THEME["accent_hover"]
            
            if type == "danger":
                final_bg = THEME["danger"]
                final_hover = "#eba0ac"
            elif type == "success":
                final_bg = THEME["success"]
                final_hover = "#94e2d5"
            elif type == "warning":
                final_bg = THEME["warning"]
                final_hover = "#f2cdcd"
            elif type == "secondary":
                final_bg = THEME["surface2"]
                final_fg = THEME["fg"]
                final_hover = THEME["overlay"]

        super().__init__(master, text=text, command=command,
                         font=("Helvetica", 12, "bold"),
                         bg=final_bg, fg=final_fg,
                         activebackground=final_hover, activeforeground=final_fg,
                         relief=tk.FLAT, bd=0, cursor="hand2",
                         padx=20, pady=10, **kwargs)
        
        self.bg_normal = final_bg
        self.bg_hover = final_hover
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
    def _on_enter(self, e):
        if self['state'] != tk.DISABLED:
            self.config(bg=self.bg_hover)
            
    def _on_leave(self, e):
        if self['state'] != tk.DISABLED:
            self.config(bg=self.bg_normal)

class GameCard(tk.Frame):
    """
    一个类似卡片的游戏入口组件
    包含: 图标, 标题, 点击事件
    """
    def __init__(self, master, title, icon_name, command, bg_color=THEME['surface']):
        super().__init__(master, bg=bg_color, cursor="hand2", padx=10, pady=10)
        self.command = command
        self.bg_normal = bg_color
        self.bg_hover = THEME['surface2']
        
        # 尝试加载图标
        self.icon_img = ResourceManager.get_image(icon_name, (64, 64))
        
        # 布局
        if self.icon_img:
            self.icon_lbl = tk.Label(self, image=self.icon_img, bg=bg_color, cursor="hand2")
            self.icon_lbl.pack(pady=(10, 5))
            self.icon_lbl.bind("<Button-1>", lambda e: command())
            
        self.title_lbl = tk.Label(self, text=title, font=("Helvetica", 14, "bold"), 
                                  fg=THEME['fg'], bg=bg_color, cursor="hand2")
        self.title_lbl.pack(pady=(0, 10))
        self.title_lbl.bind("<Button-1>", lambda e: command())
        
        # 绑定事件
        self.bind("<Button-1>", lambda e: command())
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
        # 绑定子组件事件到父组件
        for child in self.winfo_children():
            child.bind("<Enter>", self._on_enter)
            child.bind("<Leave>", self._on_leave)

    def _on_enter(self, e):
        self.config(bg=self.bg_hover)
        for child in self.winfo_children():
            child.config(bg=self.bg_hover)

    def _on_leave(self, e):
        self.config(bg=self.bg_normal)
        for child in self.winfo_children():
            child.config(bg=self.bg_normal)

class GameWindow(tk.Toplevel):
    """统一的游戏窗口基类"""
    def __init__(self, parent, title, width=600, height=500):
        super().__init__(parent)
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.config(bg=THEME["bg_primary"])
        
        # 居中窗口
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"+{x}+{y}")
        
        # 标题栏
        self.header = tk.Frame(self, bg=THEME["bg_secondary"], height=60)
        self.header.pack(fill=tk.X, side=tk.TOP)
        self.header.pack_propagate(False) # 禁止自动收缩
        
        self.title_label = tk.Label(self.header, text=title, 
                                    font=("Helvetica", 20, "bold"),
                                    bg=THEME["bg_secondary"], fg=THEME["text_primary"])
        self.title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # 内容区域
        self.content = tk.Frame(self, bg=THEME["bg_primary"])
        self.content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def add_status_bar(self):
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(self, textvariable=self.status_var,
                                   bg=THEME["bg_secondary"], fg=THEME["text_secondary"],
                                   font=("Helvetica", 10), anchor="w", padx=10)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, ipady=5)
        return self.status_var

def center_window(root, width=800, height=600):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")
