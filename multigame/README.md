# Python Multigame Collection

一个基于 Python Tkinter 的现代化多游戏集合应用。包含贪吃蛇、俄罗斯方块、看图猜词（Hangman变体）和记忆翻牌等经典游戏。

## ✨ 特性

- **现代化 UI 设计**: 采用深色主题 (Dark Theme)，卡片式布局，圆角按钮和流畅的交互体验。
- **资源管理**: 自动下载和管理游戏所需的图片资源。
- **模块化架构**: 游戏逻辑与界面分离，易于扩展和维护。

## 🎮 包含的游戏

1. **贪吃蛇 (Snake)**
   - 经典的贪吃蛇玩法，控制蛇吃食物变长，避免撞墙或撞到自己。
   
2. **俄罗斯方块 (Tetris)**
   - 经典的方块消除游戏，支持旋转、加速下落。

3. **看图猜词 (Picture Guessing)**
   - 这是一个基于 Hangman 的变体。
   - 玩家需要根据显示的**水果图片**猜出对应的英文单词。
   - 猜错会扣除生命值，猜对显示完整单词。

4. **记忆翻牌 (Memory Game)**
   - 考验记忆力的游戏。
   - 翻开两张相同的卡片即可消除，直到消除所有卡片。

## 🛠️ 安装与运行

### 1. 环境要求

- Python 3.x
- `requests` 库 (用于下载资源)
- `Pillow` 库 (用于图像处理)

### 2. 安装依赖

```bash
pip install requests Pillow
```

### 3. 下载资源

首次运行前，请运行资源下载脚本以获取游戏所需的图片素材：

```bash
python download_assets.py
```

### 4. 运行游戏

```bash
python main.py
```

## 📂 项目结构

```
multigame/
├── main.py              # 程序入口，主界面
├── ui_utils.py          # UI 工具库 (主题、自定义控件)
├── download_assets.py   # 资源下载脚本
├── games/               # 游戏逻辑模块
│   ├── snake.py
│   ├── tetris.py
│   ├── hangman.py       # 看图猜词
│   └── memory.py        # 记忆翻牌
└── images/              # 图片资源目录
```

## 🎨 主题配色

项目使用了一套现代化的深色配色方案：

- **背景色**: `#1e1e2e` (深蓝灰)
- **前景色**: `#cdd6f4` (柔和白)
- **强调色**: `#89b4fa` (淡蓝), `#f38ba8` (粉红), `#a6e3a1` (淡绿)
- **卡片背景**: `#313244`

## 📝 开发说明

- **添加新游戏**: 在 `games/` 目录下创建新的游戏类，继承自 `tk.Toplevel` 或 `tk.Frame`，并在 `main.py` 中注册即可。
- **修改 UI**: 主要 UI 组件和样式定义在 `ui_utils.py` 中。

---
Enjoy the games! 🚀
