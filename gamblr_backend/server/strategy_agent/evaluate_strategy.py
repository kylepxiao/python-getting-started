import numpy as np
import random
import marshal
import dill as pickle
from tabular import *

value_to_rank = {v: k for k, v in rank_to_value.items()}

picklefile = open('frozen_qmodel.pkl', 'rb')
model = pickle.load(picklefile)
picklefile.close()

decks = 1

def BlackJackStrategy(hand, dealer_card, method="random"):
    if method == "random":
        return RandomStrategy(hand, dealer_card)
    if method == "qlearner":
        return QLearningStrategy(hand, dealer_card)
    elif method == "tabular":
        return TabularStrategy(hand, dealer_card)
    else:
        return "Stay"

def RandomStrategy(hand, dealer_card):
    if random.random() > 0.5:
        return "hit"
    else:
        return "stay"

def generateProbabilityDistribution(card_count):
    distribition = []
    for i in range(13):
        prob = (1/13) - (6-i) * card_count / (13*6*(20*decks))
        distribition.append(prob)
    return distribition

def TabularStrategy(hand, dealer_card):
    hard_count=sum(hand)
    cards=len(hand)
    aces_count= 1*(1 in hand)
    soft_count=hard_count
    good_cards=[1,7,8,9,10]
    if hard_count<=11:
        soft_count= hard_count + 10*aces_count
    if cards==2 and soft_count==21:
        return 'Blackjack'
    if hand==[9,9] and dealer_card not in [1,7,10]:
        return 'Split'
    if cards==2:
        if hand[0]==hand[1]:
            card= hand[0]
            if card==1:
                return 'Split'
            if card==8 and dealer_card!=1:
                return 'Split'
            if card in [2,3,7] and dealer_card not in [1,8,9,10]:
                return 'Split'
            if card==6 and dealer_card not in good_cards:
                return 'Split'
            if card==4 and dealer_card in [5,6]:
                return 'Split'

    dealer_card = {"best_rank_match": value_to_rank[dealer_card]}
    hand = [{"best_rank_match": value_to_rank[val]} for val in hand]
    action = get_action(dealer_card, hand)
    adjusted_action = action.split(" ")[0] if " " in action else action
    adjusted_action = "Stay" if adjusted_action == "Stand" else adjusted_action
    return adjusted_action

def QLearningStrategy(hand, dealer_card):
    return model(hand, dealer_card)

def blackjack_hand_result(bet=10, player_hand='q', dealer_card='q', hard_code= 4, method="random", counting=False, card_count = 0):
    #Deck of cards, 4 types of 10, ordered by card count
    if card_count != 0:
        bet = min(1, bet+card_count)
        p = generateProbabilityDistribution(card_count)
    else:
        p = [1/13 for i in range(13)]
        
    
    deck=np.array([2,3,4,5,6,7,8,9,10,10,10,10,1])
    
    #hard stay condition for split aces
    
    hard_stay=False
    
    #Creating a random hand if none is input
    
    if type(player_hand)==str:
    
        player_hand=[random.choices(deck, weights=p)[0], random.choices(deck, weights=p)[0]]
        
    #Turning on hard stay for split aces
        
    if player_hand==[1]:
        hard_stay==True
        
    #Adding a 2nd card to hand after splits    
        
    while len(player_hand)<2:
        player_hand.append(random.choices(deck, weights=p)[0])
        
    #Creating dealer card, and dealer cards
        
    if type(dealer_card)==str:
    
        dealer_card=random.choices(deck, weights=p)[0]
        
    dealer_cards=[dealer_card]
    
    
    #If hard stay condition is false
        
    if hard_stay==False:
        
        #Seeing if player hit blackjack
        
        
        if BlackJackStrategy(player_hand, dealer_card, method=method) == 'Blackjack':
            
            #Seeing if casino also hit blackjack, in which case tie
            
            dealer_cards.append(random.choices(deck, weights=p)[0])
            if 1 in (dealer_cards):
                if sum(dealer_cards)==11:
                    return 0
                
             #Blackjack bonus, if not   

            return bet*1.5
        
        if type(hard_code)== str:
            if hard_code=='Hit':
                player_hand.append(random.choices(deck, weights=p)[0])
                return blackjack_hand_result(bet, player_hand, dealer_card, hard_code= 4, method=method)
            
            if hard_code=='Double':
                if len(player_hand)==2:
                    player_hand.append(random.choices(deck, weights=p)[0])
                    bet= bet*2
                    if sum(player_hand)>21:
                        return 0 - bet
                    
                else:
                    return 'Double Not Possible'
                
            if hard_code=='Split':
                
                
                if len(player_hand)==2: 
                    
                    if player_hand[0]==player_hand[1]:
                        
                        
                        res = blackjack_hand_result(bet=bet, player_hand=[player_hand[0]], dealer_card=dealer_card, hard_code= 'Split', method=method)
                        res+= blackjack_hand_result(bet=bet, player_hand=[player_hand[0]], dealer_card=dealer_card, hard_code= 'Split', method=method)

                        return res 
                        
                
                    
                    else:
                        return blackjack_hand_result(bet=bet, player_hand= player_hand, dealer_card=dealer_card, method=method)

                    
                else:
                    return blackjack_hand_result(bet=bet, player_hand=player_hand, dealer_card=dealer_card, method=method)

                    
        
        
        else:
        #Seeing how often it says to 'hit'

            while BlackJackStrategy(player_hand, dealer_card, method=method) == 'Hit':
                #Adding one card for every hit
                player_hand.append(random.choices(deck, weights=p)[0])

                #Player loses bet if hand goes above 21
                if sum(player_hand)>21:
                    return 0- bet

                #If player Doubles

            if BlackJackStrategy(player_hand, dealer_card, method=method)=='Double':
                #He gets exactly one extra card and the bet size is doubled
                player_hand.append(random.choices(deck, weights=p)[0])
                bet= bet * 2
                if sum(player_hand)>21:
                    return 0- bet

                #If player Splits

            if BlackJackStrategy(player_hand, dealer_card, method=method)== 'Split':

                #Runs the sim twice, as different hands, slightly less variance than real life, but it's okay

                res= blackjack_hand_result(bet, [player_hand[0]], dealer_card, method=method) 
                res+= blackjack_hand_result(bet, [player_hand[0]], dealer_card, method=method)
                

                return res
        
        while True:
            #Plays out the blackjack hand from dealer's side
            
            #Give dealer extra card if loop hasn't broken
            dealer_cards.append(random.choices(deck, weights=p)[0])
            
            
            #Keep track of sum of dealer's cards
            dealer_score= sum(dealer_cards)
            
            #Keep track of soft score if dealer has an ace
            
            soft_score= dealer_score
            if dealer_score<=11 and 1 in dealer_cards:
                soft_score+=10
                
            #If dealer gets blackjack you lose even if you have 21
            if len(dealer_cards)==2 and soft_score==21:
                return 0-bet
                
            #Keeps track of player's score     
            player_score=sum(player_hand)
            
            #Uses soft score if that is better for player
            if player_score<=11 and 1 in player_hand:
                player_score+=10
                
            
            #Dealer stays on all 17s
            if soft_score>=17:
                
                #If dealer bust, player wins bet
                if soft_score>21:
                    return bet
                
                #If player has more than dealer, player wins bet
                if player_score>soft_score:
                    return bet
                
                #Tie means no money changes hands
                if player_score==soft_score:
                    return 0
                
                #If player has lower, player loses bet
                if player_score<soft_score:
                    return 0 - bet
                

       
    
    if hard_stay==True:
        
        #Plays out only dealer's side, as player has to stop after 1 card
        
        while True:
            
            

                #Give dealer extra card if loop hasn't broken
            dealer_cards.append(random.choices(deck))
            
            
            #Keep track of sum of dealer's cards
            dealer_score= sum(dealer_cards)
            
            #Keep track of soft score if dealer has an ace
            
            soft_score= dealer_score
            if dealer_score<=11 and 1 in dealer_cards:
                soft_score+=10
                
            #If dealer gets blackjack you lose even if you have 21
            if len(dealer_cards)==2 and soft_score==21:
                return 0-bet
                
            #Keeps track of player's score     
            player_score=sum(player_hand)
            
            #Uses soft score if that is better for player
            if player_score<=11 and 1 in player_hand:
                player_score+=10
                
            
            #Dealer stays on all 17s
            if soft_score>=17:
                
                #If dealer bust, player wins bet
                if soft_score>21:
                    return bet
                
                #If player has more than dealer, player wins bet
                if player_score>soft_score:
                    return bet
                
                #Tie means no money changes hands
                if player_score==soft_score:
                    return 0
                
                #If player has lower, player loses bet
                if player_score<soft_score:
                    return 0 - bet

def blackjack_sim(n_hands=50_000, player_h='q', dealer_c='q', bet=10, hard_c=4, method="random", counting=False):
    pnl=0
    res=[]
    p=player_h
    q=len(player_h)
    card_count = 0
    for i in range(n_hands):
        if counting:
            card_count = random.random() * 6 - 3
        else:
            card_count = 0
        pnl+= blackjack_hand_result(bet=bet, player_hand=p[:q], dealer_card=dealer_c, hard_code= hard_c, method=method, counting=counting, card_count=card_count)
        
    return pnl

def gen_blackjack_counting_data(n_hands=50_000, player_h='q', dealer_c='q', bet=10, hard_c=4, method="random", counting=True):
    #pnl=0
    res=[]
    p=player_h
    q=len(player_h)
    card_count = 0
    data = []
    for i in range(n_hands):
        if counting:
            card_count = random.random() * 6 - 3
        else:
            card_count = 0
        current = blackjack_hand_result(bet=bet, player_hand=p[:q], dealer_card=dealer_c, hard_code= hard_c, method=method, counting=counting, card_count=card_count)
        #pnl+= current
        curr_bet = min(1, bet+card_count)
        data.append((card_count, curr_bet, current))
    return data


if __name__ == "__main__":
    with open('results.txt', 'a') as file:
        file.write("Random strategy")
        file.write("\n")
        house_edge=-100*(blackjack_sim(n_hands=1_000_000, bet=1, method="random", counting=False) / 1_000_000)
        file.write(str(house_edge))
        file.write("\n\n")

        file.write("Tabular strategy")
        file.write("\n")
        house_edge=-100*(blackjack_sim(n_hands=1_000_000, bet=1, method="tabular", counting=False) / 1_000_000)
        file.write(str(house_edge))
        file.write("\n\n")

        file.write("Q-learning strategy")
        file.write("\n")
        house_edge=-100*(blackjack_sim(n_hands=1_000_000, bet=1, method="qlearner", counting=False) / 1_000_000)
        file.write(str(house_edge))
        file.write("\n\n")

        for i in range(5):
            file.write("Deck Size: " + str(decks))
            file.write("\n\n")

            file.write("Random strategy with Counting")
            file.write("\n")
            house_edge=-100*(blackjack_sim(n_hands=1_000_000, bet=1, method="random", counting=True) / 1_000_000)
            file.write(str(house_edge))
            file.write("\n\n")

            file.write("Tabular strategy with Counting")
            file.write("\n")
            house_edge=-100*(blackjack_sim(n_hands=1_000_000, bet=1, method="tabular", counting=True) / 1_000_000)
            file.write(str(house_edge))
            file.write("\n\n")

            file.write("Q-learning strategy with Counting")
            file.write("\n")
            house_edge=-100*(blackjack_sim(n_hands=1_000_000, bet=1, method="qlearner", counting=True) / 1_000_000)
            file.write(str(house_edge))
            file.write("\n\n")
            
            decks += 1