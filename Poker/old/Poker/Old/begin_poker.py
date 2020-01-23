# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 19:14:49 2019

@author: hjali
"""




def begin_poker(players,hole_cards,community_cards):
    current_deck = Poker.Deck(np)
    player_hands = poker_hand(players,hole_cards+community_cards,current_deck)

    current_deck.shuffle()
    player_hands = current_deck.deal(players,hole_cards,player_hands)
    
    
    return current_deck,player_hands