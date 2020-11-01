import random

class AIPlayer:
    def __init__(self):
        self.state_weights = {}
        self.hit_states = []
        self.stayed_states = []
        with open("ai_state_data", "a+"):
            pass
        with open("ai_state_data", "r+") as data:
            data = data.read()
            data = data.split("\n")
            if data[0] != "":
                first_line = data[0].split("-")
                self.games_played = int(first_line[0])
                self.epselon = float(first_line[1])
            else:
                self.games_played = 0
                self.epselon = .99
            for line in data[1:]:
                split_line = line.split("-")
                if len(split_line) > 1:
                    self.state_weights[split_line[0]] = [float(split_line[1]), int(split_line[2])]

    def play(self, state):
        if state not in self.state_weights:
            self.state_weights[state] = [.500, 0]
        if random.random() > self.epselon:
            weight = self.state_weights[state][0]
        else:
            weight = .5
        if random.random() >= weight:
            self.hit_states = [state]
            self.stayed_states = []
            print("The AI hit.")
            return "h"
        else:
            self.stayed_states = [state]
            self.hit_states = []
            print("The AI stayed.")
            return "s"

    def learn(self, outcome):
        if outcome == "w":
            for state in self.hit_states:
                if self.state_weights[state][0] > 0:
                    self.state_weights[state][0] -= .001
            for state in self.stayed_states:
                if self.state_weights[state][0] < 1:
                    self.state_weights[state][0] += .001
        if outcome == "l":
            for state in self.hit_states:
                if self.state_weights[state][0] < 1:
                    self.state_weights[state][0] += .001
            for state in self.stayed_states:
                if self.state_weights[state][0] > 0:
                    self.state_weights[state][0] -= .001
        for state in self.hit_states:
            self.state_weights[state][1] += 1
        for state in self.stayed_states:
            self.state_weights[state][1] += 1
        self.games_played += 1
        self.epselon *= .999999

    def save_data(self):
        with open("ai_state_data", "w") as data:
            data.write(str(self.games_played) + "-" + "{:.10f}".format(round(self.epselon, 10)))
            for state in self.state_weights:
                if self.state_weights[state][0] > 1:
                    self.state_weights[state][0] = 1
                if self.state_weights[state][0] < 0:
                    self.state_weights[state][0] = 0
                data.write("\n{0}-{1}-{2}".format(state, round(self.state_weights[state][0], 10), self.state_weights[state][1]))
