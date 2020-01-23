
import numpy as np
from poker_tools import Deck
import begin_poker
print('before deal')
a_deck = Deck()


player_number = 3
community_cards = 1
a_deck,player_hands = begin_poker.begin_poker(player_number,2,community_cards,a_deck)
for index in range(community_cards):
    a_deck.deal_community(player_hands,1)

print('cards dealt')
for index in range(player_number):
    player_hands.display(index,a_deck)

player_straight_flushes,player_pairs =  player_hands.check_for_straight_flushes(a_deck)




