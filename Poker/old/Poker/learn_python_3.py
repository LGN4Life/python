#def run_poker():
from poker_tools import Deck

a_deck = Deck()

import begin_poker

a_deck,player_hands = begin_poker.begin_poker(5,2,5,a_deck)

print(a_deck)
#return a_deck,player_hands