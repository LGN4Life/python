# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 19:14:49 2019

@author: hjali
"""




def begin_poker(players,hole_cards,community_cards):
    from Poker.poker_tools import Deck
    from Poker.poker_tools import PokerHand
    
    current_deck = Deck
    player_hands = PokerHand(players,hole_cards+community_cards,current_deck)

    current_deck.shuffle()
    player_hands = current_deck.deal(players,hole_cards,player_hands)
    
    
    return current_deck,player_hands