import tkinter as tk
import random
from ui_utils import ModernButton, THEME

class BlackjackApp:
    CARD_WIDTH, CARD_HEIGHT = 80, 120
    CARD_BG = THEME['fg']
    CARD_OUTLINE = THEME['overlay']

    def __init__(self, root):
        self.root = root
        self.root.title('二十一点')
        self.root.geometry('800x700')
        self.root.config(bg=THEME['bg'])
        self._build()
        self.start_new_game()

    def _build(self):
        main_frame = tk.Frame(self.root, bg=THEME['bg'])
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="🃏 二十一点", font=("Helvetica", 24, "bold"), fg=THEME['fg'], bg=THEME['bg']).pack(pady=(0, 10))

        # Dealer's area
        dealer_area = tk.Frame(main_frame, bg=THEME['bg'])
        dealer_area.pack(pady=10)
        tk.Label(dealer_area, text="庄家", font=("Helvetica", 16, "bold"), fg=THEME['red'], bg=THEME['bg']).pack()
        self.dealer_canvas = tk.Canvas(dealer_area, width=700, height=self.CARD_HEIGHT + 20, bg=THEME['surface'], highlightthickness=0)
        self.dealer_canvas.pack()
        self.dealer_score_var = tk.StringVar()
        tk.Label(dealer_area, textvariable=self.dealer_score_var, font=("Helvetica", 14), fg=THEME['subtext'], bg=THEME['bg']).pack()

        # Result message
        self.result_var = tk.StringVar()
        tk.Label(main_frame, textvariable=self.result_var, font=("Helvetica", 20, "bold"), fg=THEME['yellow'], bg=THEME['bg']).pack(pady=15)

        # Player's area
        player_area = tk.Frame(main_frame, bg=THEME['bg'])
        player_area.pack(pady=10)
        tk.Label(player_area, text="玩家", font=("Helvetica", 16, "bold"), fg=THEME['green'], bg=THEME['bg']).pack()
        self.player_canvas = tk.Canvas(player_area, width=700, height=self.CARD_HEIGHT + 20, bg=THEME['surface'], highlightthickness=0)
        self.player_canvas.pack()
        self.player_score_var = tk.StringVar()
        tk.Label(player_area, textvariable=self.player_score_var, font=("Helvetica", 14), fg=THEME['subtext'], bg=THEME['bg']).pack()

        # Control buttons
        btn_frame = tk.Frame(main_frame, bg=THEME['bg'])
        btn_frame.pack(pady=20)
        
        ModernButton(btn_frame, text='🃏 要牌', command=self.hit, bg_color=THEME['blue']).pack(side=tk.LEFT, padx=10)
        ModernButton(btn_frame, text='✋ 停牌', command=self.stand, bg_color=THEME['orange']).pack(side=tk.LEFT, padx=10)
        ModernButton(btn_frame, text='🔄 新一局', command=self.start_new_game, bg_color=THEME['green']).pack(side=tk.LEFT, padx=10)

    def start_new_game(self):
        self.deck = [r + s for r in '23456789TJQKA' for s in '♥♦♣♠']
        random.shuffle(self.deck)
        self.dealer_hand = []
        self.player_hand = []
        self.dealer_shows_one = True
        self.game_over = False
        
        self.player_hand.append(self.draw())
        self.dealer_hand.append(self.draw())
        self.player_hand.append(self.draw())
        self.dealer_hand.append(self.draw())

        self.result_var.set("")
        # self.hit_btn.config(state=tk.NORMAL) # ModernButton doesn't support state config easily yet
        # self.stand_btn.config(state=tk.NORMAL)
        self.update_ui()

    def draw(self):
        return self.deck.pop()

    def calculate_value(self, hand):
        value = 0
        aces = 0
        for card in hand:
            rank = card[:-1]
            if rank in 'TJQK': value += 10
            elif rank == 'A': aces += 1
            else: value += int(rank)
        
        while aces > 0 and value + 11 <= 21:
            value += 11
            aces -= 1
        value += aces # Add remaining aces as 1
        return value

    def update_ui(self):
        self.player_canvas.delete("all")
        self.dealer_canvas.delete("all")

        # Draw player cards
        for i, card in enumerate(self.player_hand):
            self.draw_card(self.player_canvas, i, card)
        player_score = self.calculate_value(self.player_hand)
        self.player_score_var.set(f"分数: {player_score}")

        # Draw dealer cards
        for i, card in enumerate(self.dealer_hand):
            if i == 0 and self.dealer_shows_one:
                self.draw_card(self.dealer_canvas, i, None) # Face down
            else:
                self.draw_card(self.dealer_canvas, i, card)
        
        if self.dealer_shows_one:
            dealer_score = self.calculate_value([self.dealer_hand[1]])
            self.dealer_score_var.set(f"显示分数: {dealer_score}")
        else:
            dealer_score = self.calculate_value(self.dealer_hand)
            self.dealer_score_var.set(f"分数: {dealer_score}")

        if player_score > 21:
            self.result_var.set("💥 爆牌！你输了")
            self.end_game()

    def draw_card(self, canvas, index, card_str):
        x = index * (self.CARD_WIDTH + 10) + 10
        y = 10
        canvas.create_rectangle(x, y, x + self.CARD_WIDTH, y + self.CARD_HEIGHT, 
                                fill=self.CARD_BG, outline=self.CARD_OUTLINE, width=2)
        if card_str:
            rank = card_str[:-1]
            suit = card_str[-1]
            color = THEME['red'] if suit in '♥♦' else THEME['bg']
            canvas.create_text(x + self.CARD_WIDTH / 2, y + self.CARD_HEIGHT / 2,
                               text=f"{rank}\n{suit}", font=("Helvetica", 20, "bold"), fill=color, justify="center")
        else:
            canvas.create_line(x+10, y+10, x+self.CARD_WIDTH-10, y+self.CARD_HEIGHT-10, fill=THEME['blue'], width=3)
            canvas.create_line(x+10, y+self.CARD_HEIGHT-10, x+self.CARD_WIDTH-10, y+10, fill=THEME['blue'], width=3)

    def hit(self):
        if self.game_over: return
        self.player_hand.append(self.draw())
        self.update_ui()

    def stand(self):
        if self.game_over: return
        self.dealer_shows_one = False
        dealer_score = self.calculate_value(self.dealer_hand)
        while dealer_score < 17:
            self.dealer_hand.append(self.draw())
            dealer_score = self.calculate_value(self.dealer_hand)
        
        self.update_ui()
        player_score = self.calculate_value(self.player_hand)

        if dealer_score > 21 or player_score > dealer_score:
            self.result_var.set("🎉 你赢了！")
        elif player_score < dealer_score:
            self.result_var.set("😔 你输了")
        else:
            self.result_var.set("🤝 平局")
        
        self.end_game()

    def end_game(self):
        self.game_over = True
        # self.hit_btn.config(state=tk.DISABLED)
        # self.stand_btn.config(state=tk.DISABLED)
