class StrategyPerformanceTracker:
    def __init__(self):
        self.stats = {}

    def update(self, strategy, win, profit):
        if strategy not in self.stats:
            self.stats[strategy] = {"wins": 0, "losses": 0, "profit": 0.0}
        if win:
            self.stats[strategy]["wins"] += 1
        else:
            self.stats[strategy]["losses"] += 1
        self.stats[strategy]["profit"] += profit

    def get_summary(self):
        summary = []
        for strategy, data in self.stats.items():
            total = data["wins"] + data["losses"]
            win_rate = (data["wins"] / total * 100) if total > 0 else 0
            summary.append({
                "strategy": strategy,
                "wins": data["wins"],
                "losses": data["losses"],
                "profit": round(data["profit"], 2),
                "win_rate": round(win_rate, 2),
            })
        return summary

    def reset(self):
        self.stats.clear()
