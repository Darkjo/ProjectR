from collections import defaultdict
import random

class RLAgent:
    def __init__(self):
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.alpha = 0.1
        self.gamma = 0.95
        self.epsilon = 0.1

    def get_state(self, tracker):
        hot = tuple([num for num, _ in tracker.get_hot_numbers(3)])
        return hot

    def get_possible_actions(self, state):
        return list(state)

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.get_possible_actions(state))
        else:
            return max(self.q_table[state], key=self.q_table[state].get, default=random.choice(self.get_possible_actions(state)))

    def learn(self, state, action, reward, next_state):
        max_future = max(self.q_table[next_state].values(), default=0)
        current = self.q_table[state][action]
        self.q_table[state][action] = current + self.alpha * (reward + self.gamma * max_future - current)
