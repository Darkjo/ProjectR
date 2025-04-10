from collections import Counter
import math
from scipy.stats import chisquare

# Define European roulette properties
ROULETTE_COLORS = {
    0: 'green',
    1: 'red', 2: 'black', 3: 'red', 4: 'black', 5: 'red', 6: 'black',
    7: 'red', 8: 'black', 9: 'red', 10: 'black', 11: 'black', 12: 'red',
    13: 'black', 14: 'red', 15: 'black', 16: 'red', 17: 'black', 18: 'red',
    19: 'red', 20: 'black', 21: 'red', 22: 'black', 23: 'red', 24: 'black',
    25: 'red', 26: 'black', 27: 'red', 28: 'black', 29: 'black', 30: 'red',
    31: 'black', 32: 'red', 33: 'black', 34: 'red', 35: 'black', 36: 'red'
}

class RouletteTracker:
    def __init__(self):
        self.history = []
        self.predicted_dozen = None
        self.predicted_column = None
        self.predicted_numbers = []
        self.confidence = 0.0

    def add_spin(self, number):
        if isinstance(number, int) and 0 <= number <= 36:
            self.history.append(number)
        else:
            raise ValueError("Spin must be an integer between 0 and 36.")

    def reset(self):
        self.history.clear()

    def get_last_spin(self):
        return self.history[-1] if self.history else None

    def get_history(self, limit=None):
        return self.history if limit is None else self.history[-limit:]

    def get_number_frequency(self):
        return dict(Counter(self.history))

    def get_dozen_counts(self):
        dozens = {'1st': 0, '2nd': 0, '3rd': 0, 'zero': 0}
        for number in self.history:
            if number == 0:
                dozens['zero'] += 1
            elif 1 <= number <= 12:
                dozens['1st'] += 1
            elif 13 <= number <= 24:
                dozens['2nd'] += 1
            elif 25 <= number <= 36:
                dozens['3rd'] += 1
        return dozens

    def get_column_counts(self):
        columns = {'1st': 0, '2nd': 0, '3rd': 0}
        for number in self.history:
            if number == 0:
                continue
            col = (number - 1) % 3
            if col == 0:
                columns['1st'] += 1
            elif col == 1:
                columns['2nd'] += 1
            else:
                columns['3rd'] += 1
        return columns

    def get_color_counts(self):
        counts = {'red': 0, 'black': 0, 'green': 0}
        for number in self.history:
            color = ROULETTE_COLORS.get(number, 'unknown')
            if color in counts:
                counts[color] += 1
        return counts

    def predict_next(self):
        dozen_counts = self.get_dozen_counts()
        column_counts = self.get_column_counts()
        frequency = self.get_number_frequency()
        total_spins = len(self.history)

        self.predicted_dozen, dozen_max = max(dozen_counts.items(), key=lambda x: x[1])
        self.predicted_column, column_max = max(column_counts.items(), key=lambda x: x[1])
        self.predicted_numbers = sorted(frequency.items(), key=lambda x: x[1], reverse=True)[:5]
        self.predicted_numbers = [n for n, _ in self.predicted_numbers]

        dozen_conf = dozen_max / total_spins if total_spins else 0
        column_conf = column_max / total_spins if total_spins else 0
        top_number_conf = sum(freq for _, freq in Counter(self.history).most_common(5)) / total_spins if total_spins else 0
        self.confidence = round((dozen_conf + column_conf + top_number_conf) / 3, 2)

    def evaluate_prediction(self, number):
        is_win = False

        if number in self.predicted_numbers:
            is_win = True

        if self.predicted_dozen == "1st" and 1 <= number <= 12:
            is_win = True
        elif self.predicted_dozen == "2nd" and 13 <= number <= 24:
            is_win = True
        elif self.predicted_dozen == "3rd" and 25 <= number <= 36:
            is_win = True

        if self.predicted_column == "1st" and number in range(1, 37, 3):
            is_win = True
        elif self.predicted_column == "2nd" and number in range(2, 37, 3):
            is_win = True
        elif self.predicted_column == "3rd" and number in range(3, 37, 3):
            is_win = True

        return is_win

    def chi_square_test(self):
        observed = [self.get_color_counts()[c] for c in ['red', 'black', 'green']]
        expected = [len(self.history) * 18 / 37, len(self.history) * 18 / 37, len(self.history) * 1 / 37]
        stat, p = chisquare(f_obs=observed, f_exp=expected)
        return round(stat, 3), round(p, 4)

    def z_score_trend(self):
        if len(self.history) < 10:
            return None
        frequencies = Counter(self.history)
        avg = sum(frequencies.values()) / 37
        std = math.sqrt(sum((v - avg) ** 2 for v in frequencies.values()) / 37)
        z_scores = {num: (freq - avg) / std for num, freq in frequencies.items() if std > 0}
        return sorted(z_scores.items(), key=lambda x: abs(x[1]), reverse=True)[:5]

    def moving_average(self, window=10):
        if len(self.history) < window:
            return []
        return [sum(self.history[i-window:i]) / window for i in range(window, len(self.history)+1)]
