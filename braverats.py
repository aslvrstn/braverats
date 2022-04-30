import random
from collections import Counter
from enum import Enum
from typing import Optional, List


class Card(Enum):
    MUSICIAN = 0
    PRINCESS = 1
    SPY = 2
    ASSASSIN = 3
    AMBASSADOR = 4
    WIZARD = 5
    GENERAL = 6
    PRINCE = 7


FULL_HAND = [
    Card.MUSICIAN,
    Card.PRINCESS,
    Card.SPY,
    Card.ASSASSIN,
    Card.AMBASSADOR,
    Card.WIZARD,
    Card.GENERAL,
    Card.PRINCE,
]


WINNING_SCORE = 4


class Player:
    def __init__(self, cards_in_hand: Optional[List[Card]] = None):
        self.cards_in_hand = cards_in_hand or FULL_HAND.copy()
        self.points = 0
        self.bonus_for_round = 0

    def __str__(self):
        return f"Points: {self.points}. Cards left: {self.cards_in_hand}"


class GameState:
    def __init__(self):
        self.p1 = Player()
        self.p2 = Player()
        self.num_nullified_rounds = 0

    def __str__(self):
        return (
            f"P1: {self.p1}\n"
            + f"P2: {self.p2}\n"
            + f"stack: {self.num_nullified_rounds}"
        )

    def play_round(self, p1card: Card, p2card: Card):
        if p1card not in self.p1.cards_in_hand:
            raise ValueError(f"P1 doesn't currently hold a {p1card}")
        if p2card not in self.p2.cards_in_hand:
            raise ValueError(f"P2 doesn't currently hold a {p2card}")

        self.p1.cards_in_hand.remove(p1card)
        self.p2.cards_in_hand.remove(p2card)

        points_for_winning = 1

        if p1card == Card.MUSICIAN or p2card == Card.MUSICIAN:
            if p1card == Card.WIZARD:
                res = "P1"
            elif p2card == Card.WIZARD:
                res = "P2"
            else:
                res = "PUSH"
        elif p1card == Card.PRINCESS and p2card == Card.PRINCE:
            points_for_winning = 9999
            res = "P1"
        elif p2card == Card.PRINCESS and p1card == Card.PRINCE:
            points_for_winning = 9999
            res = "P2"
        else:
            # Boring case!
            res = self.result(p1card, p2card)

        if res == "P1":
            self.p1.points += self.num_nullified_rounds + points_for_winning
            self.num_nullified_rounds = 0
        elif res == "P2":
            self.p2.points += self.num_nullified_rounds + points_for_winning
            self.num_nullified_rounds = 0
        elif res == "PUSH":
            self.num_nullified_rounds += 1
        else:
            raise ValueError(f"Unknown result: res")

        return res

    def result(self, p1card: Card, p2card: Card):
        p1_val = p1card.value + self.p1.bonus_for_round
        p2_val = p2card.value + self.p2.bonus_for_round
        if p1_val > p2_val:
            return "P1"
        elif p2_val > p1_val:
            return "P2"
        else:
            return "PUSH"

    def who_has_won(self):
        if self.p1.points >= WINNING_SCORE:
            return "P1"
        elif self.p2.points >= WINNING_SCORE:
            return "P2"
        else:
            return None

    def game_over(self):
        return self.who_has_won() is not None or (not self.p1.cards_in_hand and not self.p2.cards_in_hand)


def play_random_game() -> str:
    state = GameState()
    print(state)
    while not state.game_over():
        p1play = random.choice(state.p1.cards_in_hand)
        p2play = random.choice(state.p2.cards_in_hand)
        res = state.play_round(p1play, p2play)
        print(f"P1 played {p1play}. P2 played {p2play}. Result: {res}")
        print(state)

    winner = state.who_has_won()
    print(f"{winner} won!")
    return winner


if __name__ == "__main__":
    win_counts = Counter()
    for i in range(1000):
        winner = play_random_game()
        win_counts[winner] += 1

    print(win_counts)