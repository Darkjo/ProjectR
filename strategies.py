class StrategyEngine:
    def __init__(self):
        self.current_strategy = "Flat"
        self.loss_streak = 0
        self.win_streak = 0
        self.sequence = [1]  # Used for Fibonacci or Labouchere
        self.sequence_index = 0

    def reset(self):
        self.loss_streak = 0
        self.win_streak = 0
        self.sequence = [1]
        self.sequence_index = 0

    def set_strategy(self, name):
        self.current_strategy = name
        self.reset()

    def next_bet(self, base_bet):
        if self.current_strategy == "Flat":
            return base_bet

        elif self.current_strategy == "Martingale":
            return base_bet * (2 ** self.loss_streak)

        elif self.current_strategy == "Paroli":
            return base_bet * (2 ** self.win_streak)

        elif self.current_strategy == "Fibonacci":
            fib = [1, 1]
            for _ in range(2, self.loss_streak + 1):
                fib.append(fib[-1] + fib[-2])
            return base_bet * fib[self.loss_streak] if self.loss_streak < len(fib) else base_bet * fib[-1]

        elif self.current_strategy == "D'Alembert":
            return base_bet + self.loss_streak

        elif self.current_strategy == "Oscar's Grind":
            return base_bet if self.loss_streak > 0 else base_bet * (1 + self.win_streak)

        elif self.current_strategy == "1-3-2-6":
            seq = [1, 3, 2, 6]
            idx = self.win_streak % len(seq)
            return base_bet * seq[idx]

        elif self.current_strategy == "Reverse Martingale":
            return base_bet * (2 ** self.win_streak)

        elif self.current_strategy == "Hybrid":
            # Example hybrid: Martingale but cap at 3x; Paroli max 2 wins
            if self.loss_streak > 0:
                return base_bet * min(2 ** self.loss_streak, 4)
            elif self.win_streak > 0:
                return base_bet * min(2 ** self.win_streak, 4)
            return base_bet

        else:
            return base_bet

    def update_result(self, win):
        if win:
            self.win_streak += 1
            self.loss_streak = 0
        else:
            self.loss_streak += 1
            self.win_streak = 0
