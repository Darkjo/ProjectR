from collections import defaultdict

class StrategyPerformanceTracker:
    def __init__(self):
        self.stats = defaultdict(lambda: {"spins": 0, "wins": 0, "losses": 0, "profit": 0.0})

    def update(self, strategy, win, profit):
        self.stats[strategy]["spins"] += 1
        if win:
            self.stats[strategy]["wins"] += 1
        else:
            self.stats[strategy]["losses"] += 1
        self.stats[strategy]["profit"] += profit

    def get_summary(self):
        summary = []
        for strategy, data in self.stats.items():
            win_rate = (data["wins"] / data["spins"] * 100) if data["spins"] > 0 else 0
            summary.append({
                "strategy": strategy,
                "spins": data["spins"],
                "wins": data["wins"],
                "losses": data["losses"],
                "profit": round(data["profit"], 2),
                "win_rate": round(win_rate, 2)
            })
        return summary
