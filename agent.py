import random
from collections import defaultdict

class RLAgent:
    def __init__(self):
        self.history = []  # Track past spins and context
        self.accuracy = 0.5
        self.alignments = []
        self.performance_log = []  # [(number, strategy, win, payout)]

    def record_alignment(self, success: bool):
        self.alignments.append(success)
        if len(self.alignments) > 50:
            self.alignments.pop(0)
        self.accuracy = sum(self.alignments) / len(self.alignments)

    def record_result(self, number, strategy, win, payout):
        self.performance_log.append({
            'number': number,
            'strategy': strategy,
            'win': win,
            'payout': payout
        })
        if len(self.performance_log) > 100:
            self.performance_log.pop(0)
        self.record_alignment(win)

    def get_accuracy(self) -> float:
        return round(self.accuracy, 2)

    def get_recommendation(self, bankroll, confidence=None):
        """
        Suggest strategy based on accuracy, bankroll, and (optionally) prediction confidence.
        """
        if confidence is not None:
            if confidence >= 0.7 and bankroll > 150 and self.accuracy > 0.6:
                return "martingale"
            elif confidence <= 0.4 or bankroll < 50:
                return "flat"
            elif self.recent_losing_streak() >= 3:
                return "fibonacci"
            return "paroli"
        else:
            # fallback if confidence is not provided
            if self.accuracy > 0.65 and bankroll > 150:
                return "martingale"
            elif self.accuracy < 0.4 or bankroll < 50:
                return "flat"
            elif self.recent_losing_streak() >= 3:
                return "fibonacci"
            return "paroli"

    def recent_losing_streak(self):
        streak = 0
        for result in reversed(self.alignments):
            if result is False:
                streak += 1
            else:
                break
        return streak

    def reset(self):
        self.history.clear()
        self.alignments.clear()
        self.performance_log.clear()
        self.accuracy = 0.5

    def get_summary(self):
        summary = defaultdict(lambda: {"wins": 0, "losses": 0, "profit": 0})
        for entry in self.performance_log:
            strat = entry['strategy']
            summary[strat]['profit'] += entry['payout']
            if entry['win']:
                summary[strat]['wins'] += 1
            else:
                summary[strat]['losses'] += 1

        summary_list = []
        for strat, data in summary.items():
            total = data['wins'] + data['losses']
            win_rate = round(100 * data['wins'] / total, 2) if total else 0
            summary_list.append({
                'strategy': strat,
                'wins': data['wins'],
                'losses': data['losses'],
                'profit': round(data['profit'], 2),
                'win_rate': win_rate
            })
        return summary_list
