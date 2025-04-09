# logic.py
class SpinTracker:
    def __init__(self):
        self.spin_history = []

    def add_spin(self, spin):
        self.spin_history.append(spin)

    def get_recent_spins(self, limit=10):
        return self.spin_history[-limit:]
