import random
from collections import deque

# Клас Карти з атрибутами
class Card:
    def __init__(self, name, attack, defense):
        self.name = name
        self.attack = attack
        self.defense = defense

    def __repr__(self):
        return f"{self.name}(A:{self.attack}, D:{self.defense})"

# Клас Гравця
class Player:
    def __init__(self, name):
        self.name = name
        self.deck = []  # Колода
        self.hand = []  # Рука
        self.discard_pile = []  # Відбій
        self.points = 0  # Очки

    def draw_card(self):
        if not self.deck:
            self.shuffle_discard_into_deck()
        if self.deck:
            self.hand.append(self.deck.pop())

    def shuffle_discard_into_deck(self):
        random.shuffle(self.discard_pile)
        self.deck.extend(self.discard_pile)
        self.discard_pile = []

    def __repr__(self):
        return f"{self.name}(Points: {self.points})"

# Функція для створення колоди карт
def create_deck():
    cards = [
        Card('Warrior', 5, 4),
        Card('Archer', 3, 2),
        Card('Mage', 4, 1),
        Card('Knight', 6, 6),
        Card('Assassin', 7, 2)
    ] * 4  # Кожна карта по 4 екземпляри
    random.shuffle(cards)
    return deque(cards)

# Функція для роздачі карт
def deal_initial_hands(players, cards_per_player=5):
    for _ in range(cards_per_player):
        for player in players:
            player.draw_card()

# Функція для битви між двома картами
def battle(card1, card2):
    if card1.attack > card2.defense:
        return card1
    elif card2.attack > card1.defense:
        return card2
    else:
        return None

# Основна логіка гри
def play_game(players):
    # Роздаємо початкові карти
    for player in players:
        player.deck = create_deck()
    deal_initial_hands(players)

    round_number = 1
    while any(player.hand for player in players):
        print(f"Round {round_number}")
        for player in players:
            if not player.hand:
                continue

            opponent = random.choice([p for p in players if p != player and p.hand])
            if not opponent:
                continue

            player_card = player.hand.pop(0)
            opponent_card = opponent.hand.pop(0)
            print(f"{player.name} plays {player_card} vs {opponent.name} plays {opponent_card}")

            winner_card = battle(player_card, opponent_card)
            if winner_card == player_card:
                player.points += 1
                opponent.discard_pile.append(opponent_card)
            elif winner_card == opponent_card:
                opponent.points += 1
                player.discard_pile.append(player_card)
            else:
                player.discard_pile.append(player_card)
                opponent.discard_pile.append(opponent_card)

        round_number += 1

    # Виведення результатів
    for player in players:
        print(f"{player.name} has {player.points} points")

# Створюємо гравців
players = [Player('Alice'), Player('Bob')]

# Запускаємо гру
play_game(players)
# Функція для покупки карт
def buy_cards(player, available_cards, number_of_cards=1):
    for _ in range(number_of_cards):
        if player.points >= 1:
            bought_card = random.choice(available_cards)
            player.deck.append(bought_card)
            player.points -= 1

# Функція для обміну картами
def trade_cards(player1, player2, card_from_player1, card_from_player2):
    if card_from_player1 in player1.hand and card_from_player2 in player2.hand:
        player1.hand.remove(card_from_player1)
        player2.hand.remove(card_from_player2)
        player1.hand.append(card_from_player2)
        player2.hand.append(card_from_player1)