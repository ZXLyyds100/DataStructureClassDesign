import os
import urllib.request
import ssl

# 忽略 SSL 证书验证（防止某些网络环境报错）
ssl._create_default_https_context = ssl._create_unverified_context

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')

# 图片资源清单 (URL, 保存文件名)
# 使用开源图标库或公共图床的资源
RESOURCES = [
    # 贪吃蛇
    ("https://cdn-icons-png.flaticon.com/512/3069/3069186.png", "snake_head.png"),
    ("https://cdn-icons-png.flaticon.com/512/2821/2821810.png", "snake_body.png"),
    ("https://cdn-icons-png.flaticon.com/512/415/415733.png", "snake_food.png"),
    
    # 扫雷
    ("https://cdn-icons-png.flaticon.com/512/148/148836.png", "mine.png"),
    ("https://cdn-icons-png.flaticon.com/512/1160/1160722.png", "flag.png"),
    
    # 记忆翻牌 (卡背)
    ("https://cdn-icons-png.flaticon.com/512/9466/9466270.png", "card_back.png"),
    
    # 水果系列 (用于记忆翻牌和猜单词)
    ("https://cdn-icons-png.flaticon.com/512/415/415733.png", "fruit_apple.png"),
    ("https://cdn-icons-png.flaticon.com/512/1135/1135543.png", "fruit_banana.png"),
    ("https://cdn-icons-png.flaticon.com/512/2224/2224113.png", "fruit_cherry.png"),
    ("https://cdn-icons-png.flaticon.com/512/590/590772.png", "fruit_grape.png"),
    ("https://cdn-icons-png.flaticon.com/512/135/135695.png", "fruit_lemon.png"),
    ("https://cdn-icons-png.flaticon.com/512/2224/2224256.png", "fruit_orange.png"),
    ("https://cdn-icons-png.flaticon.com/512/1135/1135609.png", "fruit_pear.png"),
    ("https://cdn-icons-png.flaticon.com/512/2224/2224300.png", "fruit_strawberry.png"),
    ("https://cdn-icons-png.flaticon.com/512/1135/1135505.png", "fruit_watermelon.png"),
    ("https://cdn-icons-png.flaticon.com/512/2224/2224135.png", "fruit_pineapple.png"),
    
    # 主页图标
    ("https://cdn-icons-png.flaticon.com/512/808/808439.png", "game_controller.png"),

    # 其他游戏图标
    ("https://cdn-icons-png.flaticon.com/512/1021/1021264.png", "tictactoe.png"), # Tic Tac Toe
    ("https://cdn-icons-png.flaticon.com/512/3081/3081840.png", "guess_number.png"), # Number/Question
    ("https://cdn-icons-png.flaticon.com/512/2282/2282332.png", "hangman.png"), # Hangman/Word
    ("https://cdn-icons-png.flaticon.com/512/2476/2476188.png", "blackjack.png"), # Cards
    ("https://cdn-icons-png.flaticon.com/512/3209/3209965.png", "memory.png"), # Brain/Memory
]

def download_assets():
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)
        print(f"创建目录: {ASSETS_DIR}")

    print("开始下载游戏素材...")
    for url, filename in RESOURCES:
        filepath = os.path.join(ASSETS_DIR, filename)
        if os.path.exists(filepath):
            print(f"[跳过] 已存在: {filename}")
            continue
            
        try:
            print(f"[下载中] {filename} ...")
            # 模拟浏览器 User-Agent 防止被拦截
            req = urllib.request.Request(
                url, 
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )
            with urllib.request.urlopen(req, timeout=10) as response, open(filepath, 'wb') as out_file:
                out_file.write(response.read())
            print(f"[成功] {filename}")
        except Exception as e:
            print(f"[失败] {filename}: {e}")

    print("\n素材下载完成！")

if __name__ == "__main__":
    download_assets()
