
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

   

