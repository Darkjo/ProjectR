# utils.py

# Roulette color mapping
ROULETTE_COLORS = {
    0: "green",
    1: "red", 2: "black", 3: "red", 4: "black", 5: "red", 6: "black",
    7: "red", 8: "black", 9: "red", 10: "black", 11: "black", 12: "red",
    13: "black", 14: "red", 15: "black", 16: "red", 17: "black", 18: "red",
    19: "red", 20: "black", 21: "red", 22: "black", 23: "red", 24: "black",
    25: "red", 26: "black", 27: "red", 28: "black", 29: "black", 30: "red",
    31: "black", 32: "red", 33: "black", 34: "red", 35: "black", 36: "red"
}

# Dozen groupings
DOZEN_MAPPING = {
    '1st': list(range(1, 13)),
    '2nd': list(range(13, 25)),
    '3rd': list(range(25, 37)),
    'zero': [0]
}

# Column groupings
COLUMN_MAPPING = {
    '1st': [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],
    '2nd': [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
    '3rd': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
}

# Payout multipliers for different bet types (for future use)
PAYOUTS = {
    'straight': 35,
    'split': 17,
    'street': 11,
    'corner': 8,
    'six_line': 5,
    'column': 2,
    'dozen': 2,
    'even_chance': 1  # red/black, even/odd, 1-18/19-36
}
