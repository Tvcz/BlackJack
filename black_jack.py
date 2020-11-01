#!/usr/bin/python3

import sys
import random
if len(sys.argv) > 1 and sys.argv[1] == "-a":
    from ai import AIPlayer

class BlackJack:
    def __init__(self):
        self.deck = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
        self.card_values = {"1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10, "A":11}
        self.games_played = 0
        self.player_wins = 0
        self.house_wins = 0
        self.games_tied = 0
        self.player_blackjacks = 0
        if len(sys.argv) > 1 and sys.argv[1] == "-a":
            self.ai = AIPlayer()

    def start(self):
        print("Dealing cards...")
        self.player_cards = [random.choice(self.deck)]
        self.house_cards = [random.choice(self.deck)]
        print("Player: " + ", ".join(self.player_cards) + " | House: [Unknown] " + ", ".join(self.house_cards[1:]))
        player_card = random.choice(self.deck)
        if player_card == "A" and self.value_sum(self.player_cards) >= 11:
            player_card = "1"
        self.player_cards.append(player_card)
        house_card = random.choice(self.deck)
        if house_card == "A" and self.value_sum(self.house_cards) >= 11:
            self.house_cards[0] = "1"
        self.house_cards.append(house_card)

        self.game_round()

        print("Player: {0} | House: {1}".format(", ".join(self.player_cards), ", ".join(self.house_cards)))

        player_win_conditions = (
        self.is_blackjack(self.player_cards) and not self.is_blackjack(self.house_cards),
        self.value_sum(self.player_cards) > self.value_sum(self.house_cards) and self.value_sum(self.player_cards) <= 21,
        self.value_sum(self.player_cards) <= 21 and self.value_sum(self.house_cards) > 21
        )

        house_win_conditions = (
        self.is_blackjack(self.house_cards) and not self.is_blackjack(self.player_cards),
        self.value_sum(self.house_cards) > self.value_sum(self.player_cards) and self.value_sum(self.house_cards) <= 21,
        self.value_sum(self.player_cards) > 21
        )

        tie_conditions = (
        self.value_sum(self.player_cards) == self.value_sum(self.house_cards) and self.value_sum(self.player_cards) <= 21 and not self.is_blackjack(self.player_cards) and not self.is_blackjack(self.house_cards),
        self.is_blackjack(self.player_cards) and self.is_blackjack(self.house_cards)
        )

        if self.is_blackjack(self.player_cards) and not self.is_blackjack(self.house_cards):
            self.player_blackjacks += 1

        for condition in player_win_conditions:
            if condition == True:
                print("The Player has won the game!")
                if len(sys.argv) > 1 and sys.argv[1] == "-a":
                    self.ai.learn("w")
                self.games_played += 1
                self.player_wins += 1
                return

        for condition in house_win_conditions:
            if condition == True:
                print("The House has won the game!")
                if len(sys.argv) > 1 and sys.argv[1] == "-a":
                    self.ai.learn("l")
                self.games_played += 1
                self.house_wins += 1
                return

        for condition in tie_conditions:
            if condition == True:
                print("The game is a tie.")
                if len(sys.argv) > 1 and sys.argv[1] == "-a":
                    self.ai.learn("t")
                self.games_played += 1
                self.games_tied += 1
                return

    def game_round(self):
        while self.value_sum(self.player_cards) < 21:
            print("Player: {0} | House: [Unknown] {1}".format(", ".join(self.player_cards), ", ".join(self.house_cards[1:])))
            if len(sys.argv) > 1 and sys.argv[1] == "-a":
                state = "{0}|{1}".format(self.visual_sum(self.player_cards), self.visual_sum(self.house_cards))
                choice = self.ai.play(state)
            else:
                choice = input("Would you like to hit or stay?\n>>> ").lower()[0]
            if choice == "h":
                card = random.choice(self.deck)
                print("The Player got a(n) {}.".format(card))
                if card == "A":
                    if self.value_sum(self.player_cards) >= 11:
                        card = "1"
                    print("The optimal value for the Ace will be automatically selected.")
                self.player_cards.append(card)
                continue
            if choice == "s":
                break
        if self.value_sum(self.player_cards) <= 21 and not self.is_blackjack(self.player_cards):
            while self.value_sum(self.house_cards) < 17 or self.is_soft(self.house_cards):
                print("Player: {0} | House: [Unknown] {1}".format(", ".join(self.player_cards), ", ".join(self.house_cards[1:])))
                card = random.choice(self.deck)
                print("The House got a(n) {}.".format(card))
                if card == "A" and self.value_sum(self.house_cards) >= 11:
                    card = "1"
                self.house_cards.append(card)

    def is_blackjack(self, container):
        if self.value_sum(container) == 21 and len(container) == 2:
            return True
        else:
            return False

    def is_soft(self, container):
        value = 0
        for item in container:
            value += self.card_values[item]
        ace_count = 0
        for item in container:
            if item == "A":
                ace_count += 1
        if ace_count > 0:
            value += ace_count - 1
            if value < 7:
                return True

    def visual_sum(self, container):
        value = 0
        for item in container:
            value += self.card_values[item]
        if value > 21:
            if "A" in container:
                value -= 10
        return value

    def value_sum(self, container):
        value = 0
        for item in container:
            value += self.card_values[item]
        if value > 21:
            if "A" in container:
                value -= 10
        return value

blackjack = BlackJack()
try:
    if len(sys.argv) > 2 and sys.argv[1] == "-a" and sys.argv[2] == "-t":
        if len(sys.argv) == 3:
            try:
                while True:
                    blackjack.start()
                    print("")
            finally:
                print("{0} games played, AI won {1}, House won {2}.".format(blackjack.games_played, blackjack.player_wins, blackjack.house_wins))
                print("The AI had {} blackjacks.".format(blackjack.player_blackjacks))
        if len(sys.argv) > 3:
            try:
                for iteration in range(int(sys.argv[3])):
                    blackjack.start()
                    print("")
            finally:
                print("{0} games played, AI won {1}, House won {2}.".format(blackjack.games_played, blackjack.player_wins, blackjack.house_wins))
                print("The AI had {} blackjacks.".format(blackjack.player_blackjacks))
    else:
        blackjack.start()
finally:
    if len(sys.argv) > 1 and sys.argv[1] == "-a":
        blackjack.ai.save_data()
