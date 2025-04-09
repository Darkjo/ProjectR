from collections import defaultdict, deque

class RouletteTracker:
    def __init__(self):
        self.history = []
        self.freq = defaultdict(int)
        self.max_history = 200
        self.trend_data = defaultdict(lambda: deque(maxlen=5))
        self.alignment_total = 0
        self.alignment_hits = 0

    def add_spin(self, number, rl_number=None, full_alignment=False):
        if 0 <= number <= 36:
            self.history.append((number, rl_number, full_alignment))
            self.freq[number] += 1
            if len(self.history) > self.max_history:
                removed, _, align = self.history.pop(0)
                self.freq[removed] -= 1
                if align:
                    self.alignment_total -= 1

    def undo_spin(self):
        if self.history:
            number, rl, align = self.history.pop()
            self.freq[number] -= 1
            if align:
                self.alignment_total -= 1
                if number == rl:
                    self.alignment_hits -= 1
            return number, rl, align
        return None, None, None

    def get_recent_numbers(self, limit=10):
        return [num for num, _, _ in self.history[-limit:]]

    def get_hot_numbers(self, top_n=5):
        return sorted(self.freq.items(), key=lambda x: x[1], reverse=True)[:top_n]

    def get_top_dozen(self):
        dozen_counts = {1: 0, 2: 0, 3: 0}
        for num, _, _ in self.history:
            if 1 <= num <= 12:
                dozen_counts[1] += 1
            elif 13 <= num <= 24:
                dozen_counts[2] += 1
            elif 25 <= num <= 36:
                dozen_counts[3] += 1
        top = max(dozen_counts, key=dozen_counts.get)
        return top

    def get_top_street(self):
        street_hits = defaultdict(int)
        for num, _, _ in self.history:
            if num == 0:
                continue
            street = ((num - 1) // 3) * 3 + 1
            street_hits[street] += 1
        if not street_hits:
            return (0, 1, 2)
        top = max(street_hits, key=street_hits.get)
        return (top, top+1, top+2)

    def get_alignment_stats(self):
        if self.alignment_total == 0:
            return "N/A"
        rate = self.alignment_hits / self.alignment_total * 100
        return f"{self.alignment_hits}/{self.alignment_total} ({rate:.1f}%)"
