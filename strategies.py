class BaseStrategy:
    def __init__(self):
        self.base_bet = 1.0
        self.current_bet = self.base_bet

    def next_bet(self, win: bool) -> float:
        raise NotImplementedError("Must be implemented in subclass")

    def reset(self):
        self.current_bet = self.base_bet


class FlatStrategy(BaseStrategy):
    def next_bet(self, win: bool) -> float:
        return self.base_bet


class MartingaleStrategy(BaseStrategy):
    def next_bet(self, win: bool) -> float:
        if win:
            self.current_bet = self.base_bet
        else:
            self.current_bet *= 2
        return self.current_bet


class ParoliStrategy(BaseStrategy):
    def __init__(self):
        super().__init__()
        self.wins = 0

    def next_bet(self, win: bool) -> float:
        if win:
            self.wins += 1
            if self.wins >= 3:
                self.current_bet = self.base_bet
                self.wins = 0
            else:
                self.current_bet *= 2
        else:
            self.current_bet = self.base_bet
            self.wins = 0
        return self.current_bet


class FibonacciStrategy(BaseStrategy):
    def __init__(self):
        super().__init__()
        self.sequence = [1, 1]
        self.index = 0

    def next_bet(self, win: bool) -> float:
        if win:
            self.index = max(0, self.index - 2)
        else:
            if self.index >= len(self.sequence):
                self.sequence.append(self.sequence[-1] + self.sequence[-2])
            self.index += 1
        self.current_bet = self.base_bet * self.sequence[self.index]
        return self.current_bet


class DAlembertStrategy(BaseStrategy):
    def next_bet(self, win: bool) -> float:
        if win:
            self.current_bet = max(self.base_bet, self.current_bet - self.base_bet)
        else:
            self.current_bet += self.base_bet
        return self.current_bet


class LabouchereStrategy(BaseStrategy):
    def __init__(self):
        super().__init__()
        self.sequence = [1, 2, 3, 4]

    def next_bet(self, win: bool) -> float:
        if len(self.sequence) == 0:
            self.sequence = [1, 2, 3, 4]
        if win:
            if len(self.sequence) > 1:
                self.sequence = self.sequence[1:-1]
            else:
                self.sequence = []
        else:
            self.sequence.append(self.sequence[0] + self.sequence[-1])
        if len(self.sequence) >= 2:
            self.current_bet = self.base_bet * (self.sequence[0] + self.sequence[-1])
        else:
            self.current_bet = self.base_bet * self.sequence[0]
        return self.current_bet


class StrategyEngine:
    def __init__(self):
        self.strategies = {
            "Flat": FlatStrategy(),
            "Martingale": MartingaleStrategy(),
            "Paroli": ParoliStrategy(),
            "Fibonacci": FibonacciStrategy(),
            "DAlembert": DAlembertStrategy(),
            "Labouchere": LabouchereStrategy(),
        }

    def evaluate(self, number, strategy_name):
        """For now, simulate a win if number is even and not zero."""
        win = number % 2 == 0 and number != 0
        return win

    def get_bet_amount(self, strategy_name: str, win: bool) -> float:
        return self.strategies[strategy_name].next_bet(win)

    def reset_strategy(self, strategy_name: str):
        self.strategies[strategy_name].reset()

    def get_strategy_names(self):
        return list(self.strategies.keys())
