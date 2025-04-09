def choose_strategy(tracker, agent, bankroll, confidence_enabled=True):
    """
    Chooses a roulette strategy based on bankroll health, streak history,
    and optionally reinforcement learning alignment accuracy.

    Args:
        tracker: RouletteTracker instance with spin/streak data
        agent: RLAgent instance with accuracy tracking
        bankroll (float): current bankroll
        confidence_enabled (bool): whether to return confidence score

    Returns:
        tuple: (strategy_name: str, confidence: float)
    """
    win_streak = tracker.get_current_win_streak()
    loss_streak = tracker.get_current_loss_streak()
    rl_accuracy = agent.get_accuracy()

    # Priority Logic
    if bankroll < 10:
        strategy = "Flat"
        confidence = 0.95
    elif loss_streak >= 3:
        strategy = "Martingale"
        confidence = 0.8
    elif win_streak >= 3:
        strategy = "Paroli"
        confidence = 0.75
    elif rl_accuracy > 0.7:
        strategy = "Hybrid"
        confidence = 0.85
    else:
        strategy = "Flat"
        confidence = 0.65

    return (strategy, confidence) if confidence_enabled else strategy
