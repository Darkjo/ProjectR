def choose_strategy(bankroll, history, accuracy):
    """
    Choose a betting strategy based on current bankroll, spin history, and agent accuracy.
    
    Returns one of: "Flat", "Martingale", "Paroli", "Hybrid"
    """
    if accuracy > 0.7 and bankroll > 50:
        return "Paroli"
    elif bankroll < 20:
        return "Flat"
    elif len(history) >= 5 and accuracy < 0.5:
        return "Martingale"
    else:
        return "Hybrid"