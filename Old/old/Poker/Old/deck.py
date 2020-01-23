# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 16:11:46 2019

@author: hjali
"""
import numpy as np
suit_list = ('C','D','H','S')
value_list = list(range(2,11)) +['J','Q','K','A']
print(np)

class deck:
    def __init__(self,np):
        self.suit_list = suit_list
        self.value_list = value_list
        self.order = np.array(range(52),dtype=int)
        self.cards_numeric = np.zeros((52,3),dtype=int)
        self.cards  = [None]*52
        print('new deck created')
     
        index = 0;
        for suit_index in range(len(suit_list)):
            for value_index in range(len(value_list)):
        
                self.cards[index] = [str(value_list[value_index]),suit_list[suit_index]]
                self.cards_numeric[index] = [value_index, suit_index,index]
                index +=1
    def shuffle(self,*args):
        if not args:
            print('no prior hands')
        else:
            hands = args[0]
            self.order = np.concatenate((self.order, hands.flatten()), axis=0) 
        np.random.shuffle(self.order)
    def deal(self,num_players,cards_per_hand,player_hands):
        for index in range(num_players):
            for card_index  in range(cards_per_hand):
                player_hands.cards[index,card_index] = self.order[0]
                self.order = self.order[1:]
        return player_hands
    def deal_community(self,player_hands,cards):
        current_card_count =  sum(player_hands.cards[0]>=0)
        if current_card_count+cards> player_hands.cards.shape[1]:
            print('can\'t add that many cards' )
            return
        
        for i in np.arange(current_card_count,current_card_count+cards):
            for player_num in range(len(player_hands.cards[:,0])):
                player_hands.cards[player_num,i] = self.order[0]
            self.order = self.order[1:]
            