# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 20:36:23 2019

@author: hjali
"""

suit_list = ('C','D','H','S')
value_list = list(range(2,11)) +['J','Q','K','A']


class Deck:
    def __init__(self):
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

class PokerHand:
    def __init__(self,players,total_cards,a_deck):
        self.cards = np.ones((players,total_cards),dtype=int)*-1
        self.values = np.ones((players,total_cards),dtype=int)*-1
        self.suits = np.ones((players,total_cards),dtype=int)*-1
    def display(self,player,deck):
        current_cards = self.cards[player]>=0
        current_cards = self.cards[player][current_cards]
        current_cards = [ deck.cards[i] for i in current_cards]
        
        print(current_cards)
        #return(current_cards)
    
    def check_for_straight_flushes(self,deck):
        winners = None
        unique_values = np.unique(a_deck.cards_numeric[self.cards,0])
        unique_values[::-1].sort()
        unique_suits = np.unique(a_deck.cards_numeric[self.cards,1])
        player_suits = a_deck.cards_numeric[self.cards,1]
        player_values = a_deck.cards_numeric[self.cards,0]
        unique_straight_flush = np.zeros(unique_suits[0],dtype=int)
        player_straight_flushes = np.ones((self.cards.shape[0],4),dtype=bool)*-1
        
        
        player_pairs = np.zeros((self.cards.shape[0],len(unique_values)),dtype=int)

        index=0
        value_index =-1;
        #loop through values first, then you don't have to look at 
        #lower anchor values once a straight flush as been found
        for current_value in unique_values: #loop through values to ultimately find the player with the best straight flush
            value_index +=1
            #values that would make the current straight
            straight_cards = np.arange(current_value-4,current_value+1)
            for player_number in range(self.cards.shape[0]): #loop through players
              
                player_pairs[player_number,value_index] = sum(player_values[player_number] ==current_value)
                
                
                current_unique_values = np.unique(player_values[player_number])
                straight_logical = np.isin(current_unique_values,straight_cards)
                
                if sum(straight_logical)==5 and player_straight_flushes[player_number,0]==-1: #does not overwright with lower values
                    player_straight_flushes[player_number,1] = current_value
                    
                for current_suit in unique_suits:
                    
                    current_suit_total = np.sum(player_suits[player_number]==current_suit)
           
                    if current_suit_total>4:
                        temp = player_suits[player_number]==current_suit;
                        player_straight_flushes[player_number,2] = max(player_values[player_number][temp])
                        suit_logical = player_suits[player_number]==current_suit
                        value_logical = player_values[player_number]==current_value   
                        if np.any(np.logical_and(suit_logical,value_logical)):

                            #cards that would make the current flush
                            current_flush_cards = np.sort(player_values[player_number][np.where(suit_logical)])
                            
                            #determine which cards are in the current straight and the current flush
                            flush_straight_logical = np.isin(current_flush_cards,straight_cards)
                            #if player already has a striaght flush, don't look at other suits
                            if sum(flush_straight_logical)>4:
                                print('player ' + str(player_number) + ' has a straight flush')
                                player_straight_flushes[player_number,0] = current_value
                                break
            #if one or more player already has a straight flush, don't look at lower values
            if max(player_straight_flushes[:,2])>0: 
                break



        HighCardKickers = np.max(player_values[:,0:2],axis=1)
        print('HighCardKickers = ' + str(HighCardKickers))

        #now that all the straight flushes have been calculated
        
        #straight flushes are the best
        winners = np.array(player_straight_flushes[:,0]>-1)
      
        if np.sum(winners)==1:
            print('player ' + str(np.where(winners)[0]) + ' wins with a straight flush' )
        elif sum(winners)>1:
            max_straight = max(player_straight_flushes[winners,0])
            winners = winners[np.where(player_straight_flushes[winners,3]==max_straight)]
            #winners=winners[0]
            if sum(winners)==1:
                print('player ' + str(np.where(winners)[0]) + ' wins with a high card straight flush' )
            else:
                print('players ' + str(np.where(winners)[0]) + ' split the pot with a high card straight flush' )
        else: 
            print('there are no straight flushes')
            winners = np.array(player_straight_flushes[:,1]>-1)
            if sum(winners)==1:
                print('player ' + str(np.where(winners)[0]) + ' wins with a straight' )
            elif sum(winners)>1:
                max_straight = max(player_straight_flushes[winners,1])
                winners = winners[np.where(player_straight_flushes[winners,1]==max_straight)]
         
                if sum(winners)==1:
                    print('player ' + str(np.where(winners)[0]) + ' wins with a high card straight' )
                else:
                    print('players ' + str(np.where(winners)[0]) + ' split the pot with a high card  straight' )
            else:
                print('there are no straights')
                winners = np.array(player_straight_flushes[:,2]>-1)
                if np.sum(winners)==1:
                    print('player ' + str(np.where(winners)[0]) + ' wins with a flush' )
                elif sum(winners)>1:
                    max_straight = max(player_straight_flushes[winners,2])
                    winners = winners[np.where(player_straight_flushes[winners,2]==max_straight)]

                    if sum(winners)==1:
                        print('player ' + str(np.where(winners)[0]) + ' wins with a high card flush' )
                    else:
                        print('players ' + str(np.where(winners)[0]) + ' split the pot with a high card  flush' )
                else:
                    print('there are no flushes')
                    winners = np.max(player_pairs,axis=1)==4
                    #pdb.set_trace()
                    if np.sum(winners)==1:
                        print('player ' + str(np.where(winners)[0]) + ' wins with a four of a kind' )
                    elif np.sum(winners)>1:
                        quad_values = np.any(player_pairs==4,axis=0) #True if any player has a quad at a given index
                        max_quad = np.max(np.where(quad_values))
                        max_quad_winners = np.where(player_pairs[:,max_quad]==4) #True if any player has a quad at a given index
                        
                        #winners = np.argmax(quad_index[1])# gives the index of the players with quads
                        #winners = winners[np.where(player_pairs[winners,:]==max_straight),True,False]
                        #pdb.set_trace()
                        print('max quad winners' + str(max_quad_winners[0]))
                        
                        if len(max_quad_winners[0])==1:
                            print('player ' + str(max_quad_winners[0]) + ' wins with a high card four of a kind' )
                        else:
                            print('players ' + str(max_quad_winners[0]) + ' split the pot with a high card four of a kind' )
                    else:
                        print('there are no quads')
                        players_pairs_logical = np.any(player_pairs==2,axis=1)
                        players_trips_logical = np.any(player_pairs==3,axis=1)
                        players_two_trips_logical = np.sum(player_pairs==3,axis=1)==2
                        
                        winners_full_house = np.logical_and(players_pairs_logical,players_trips_logical)
                        winners_full_house = np.logical_or(winners_full_house,players_two_trips_logical)
                        #pdb.set_trace()
                       
                        if np.sum(winners_full_house)==1:
                            print('player ' + str(np.where(winners_full_house)[0]) + ' wins with a full house' )
                        elif np.sum(winners_full_house)>1:
                            trips_index = np.sum(player_pairs[winners_full_house]==3, axis=0)>0
                         
                            #winners_trips=np.where(winners_trips)
                            max_trips =np.min(np.where(trips_index))
                            
               
                            temp_index = player_pairs[winners_full_house,max_trips]==3
                            temp_index = np.where(temp_index)
                            winners_full_house = winners_full_house[temp_index]
                            
                           
                            winners=winners_full_house
                           
                            #pdb.set_trace()
                            if np.sum(winners)==1:
                                print('player ' + str(np.where(winners)[0]) + ' wins with a high card full house' )
                            else:
                                
                                print('players ' + str(np.where(winners)[0]) + ' split the pot with a high card full house' )
                        else:
                            print('there are no full_houses')
                            winners_trips = np.max(player_pairs,axis=1)==3
                            
                            if np.sum(winners_trips)==1:
                                print('player ' + str(np.where(winners_trips)[0]) + ' wins with a three of a kind' )
                            elif sum(winners_trips)>1:
                                trips_index = player_pairs[winners_trips]==3
                                max_trips_index = min(np.where(trips_index)[0])
                                
                                high_trips_logical=player_pairs[:,max_trips_index]>0
                                #pdb.set_trace()
                                if np.sum(high_trips_logical)==1:
                                    print('player ' + str(np.where(high_trips_logical)[0]) + ' wins with a high card three of a kind' )
                                else:
                                    best_kicker = np.max(HighCardKickers[winners_trips])
                                    kicker_tie_break = HighCardKickers==best_kicker
                                    kicker_winner = np.logical_and(kicker_tie_break,high_trips_logical)
                                
                                    if np.sum(kicker_winner)==1:
                                        print('players ' + str(np.where(kicker_tie_break)[0]) + ' wins the pot with a three of a kind kicker' )
                                    else:
                                        print('players ' + str(np.where(kicker_tie_break)[0]) + ' split the pot with a three of a kind kicker' )
                            else:
                            
                                winners_pairs = np.sum(player_pairs==2,axis=1)>0
                                winners_two_pairs = np.sum(player_pairs==2,axis=1)>1
                               
                                pair_index = np.sum(player_pairs==2,axis=0)>0
                                two_pair_index = np.sum(player_pairs==2,axis=0)==2
                                if sum(winners_pairs)==1:
                                    print('player ' + str(np.where(winners_pairs)[0]) + ' wins with a pair' )
                                elif sum(winners_pairs)>1:
                                    # check for players with two pairs
                                    
                                    if sum(winners_two_pairs)==1:
                                        print('player  ' + str(np.where(winners_two_pairs)[0]) + ' wins with two pairs')
                                    elif sum(winners_two_pairs)>1:
                                        #pdb.set_trace()
                                        #two_pairs_index = np.sum(player_pairs[winners_two_pairs]==2,axis=1)
                                        two_pairs_logical = np.sum(player_pairs[winners_two_pairs]==2,axis=0)>1
                                        two_pairs_index = np.min(np.where(two_pairs_logical))
                                        #pdb.set_trace()
                                        #temp_index = np.argmax(pairs_index[1])# gives the index of the players with the best two pair
                                        winners = player_pairs[winners_two_pairs,two_pairs_index]>1
                                       
                                        #pdb.set_trace()
                                        if np.sum(winners)==1:
                                            print('player ' + str(np.where(winners)[0]) + ' wins with a high card two pair' )
                                        else:
                                            best_kicker = np.max(HighCardKickers[winners_two_pairs])
                                            kicker_tie_break = HighCardKickers==best_kicker
                                            #pdb.set_trace()
                                            kicker_winner = np.logical_and(kicker_tie_break,winners_two_pairs)
                                            if np.sum(kicker_winner)==1:
                                                print('players ' + str(np.where(kicker_tie_break)[0]) + ' wins the pot with a two pair kicker' )
                                            else:
                                                print('players ' + str(np.where(kicker_tie_break)[0]) + ' split the pot with a two pair kicker' )
                                    else:
                                        winners_pairs = np.sum(player_pairs==2,axis=1)>0
                                        pairs_index = np.any(player_pairs==2,axis=0)
                                    
                                        best_pair_index = np.min(np.where(pairs_index)[0])# gives the index of the best pair
                                    
                                        best_pair_logical = player_pairs[:,best_pair_index]>1
                                       
                                        winners=np.logical_and(winners_pairs,best_pair_logical)
                                  
                                        if np.sum(winners)==1:
                                            print('player ' + str(np.where(winners)[0]) + ' wins with a high card pair' )
                                        else:
                                            best_kicker = np.max(HighCardKickers[winners])
                                            kicker_tie_break = HighCardKickers==best_kicker
                                            #pdb.set_trace()
                                            kicker_winner = np.logical_and(kicker_tie_break,winners)
                                            if np.sum(kicker_winner)==1:
                                                print('players ' + str(np.where(kicker_tie_break)[0]) + ' wins the pot with a pair kicker' )
                                            else:
                                                print('players ' + str(np.where(kicker_tie_break)[0]) + ' split the pot with a pair kicker' )
                                else:
                                    print('there are no pairs')
                                    best_kicker = np.max(HighCardKickers)
                                    high_card_winner = HighCardKickers ==best_kicker
                                    if np.sum(high_card_winner)==1:
                                        print('players ' + str(np.where(high_card_winner)[0]) + ' wins the pot with a high card' )
                                    else:
                                        print('players ' + str(np.where(high_card_winner)[0]) + ' split the pot with a high card' )
        return player_straight_flushes,player_pairs