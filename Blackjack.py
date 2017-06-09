# Mini-project #6 - Blackjack
# Only works on codeskulptor.org

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
player_score = 0
dealer_score = 0
player_hand = []
dealer_hand = []

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []
    
    def __str__(self):
        hnd = ''
        for i in range(len(self.hand)):
            hnd += str(self.hand[i]) + ' '
        return hnd
        
    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        hand_value = 0
        has_ace = False
        
        
        for card in self.hand:
            rank = card.get_rank()
            hand_value += VALUES[rank]
        
    
            if rank == 'A':
                has_ace = True
            
        if has_ace and hand_value <= 11:
            return hand_value + 10
        else: 
            return hand_value

    def draw(self, canvas, pos):
        for c in self.hand:
            c.draw(canvas, pos)
            pos[0] += 80
        

# define deck class 
class Deck:
    def __init__(self):
        self.deck_of_cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck_of_cards.append(Card(suit, rank))
                
    def shuffle(self):
        random.shuffle(self.deck_of_cards)

    def deal_card(self):
        return self.deck_of_cards.pop((random.randint(0, len(self.deck_of_cards))-1))
        
    def __str__(self):
        dck = ''
        for i in range(len(self.deck_of_cards)):
            dck += str(self.deck_of_cards[i]) + ' ' 
        return 'Deck: ' + dck
    

# define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, deck, player_score, dealer_score
    outcome = ''
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    
    if in_play:
        outcome =  'You have folded, House wins. Play again?'
        dealer_score += 1
        in_play = False
    
    else: 
        for i in range(2):
            player_hand.add_card(deck.deal_card())
    
        for j in range(2):
            dealer_hand.add_card(deck.deal_card())
    
        in_play = True
    
    
def hit():
    global player_hand, in_play, outcome, player_score, dealer_score
    
    if player_hand.get_value() < 21 and in_play == True:
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            outcome = 'Player busts, House wins. Play again?'
            dealer_score += 1
            in_play = False
    

def stand():
    global dealer_hand, in_play, outcome, player_score, dealer_score
    
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        
        if (dealer_hand.get_value() >= player_hand.get_value()) and (dealer_hand.get_value() <= 21):
            outcome = 'House wins. Play again?'
            dealer_score += 1
        elif dealer_hand.get_value() > 21:
            outcome = 'House busts, Player wins. Play again?'
            player_score += 1
        else:
            outcome = 'Player wins. Play again?'
            player_score += 1
            
        in_play = False
            
       
# define draw handler    
def draw(canvas):
    
    player_hand.draw(canvas, [120,400])
    dealer_hand.draw(canvas, [120, 100])
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [120 + 72/2, 100 + 96/2], CARD_BACK_SIZE)
    
    canvas.draw_text(outcome, [50,550], 24, 'White')
   
    canvas.draw_text('BLACKJACK', [165, 65], 48, 'Black')

    canvas.draw_text('Dealer: ' + str(dealer_score), [25, 150], 24, 'Red')
    canvas.draw_text('Player: ' + str(player_score), [25, 450], 24, 'Blue')
    canvas.draw_text('(Hit or Stand)', [25, 475], 12, 'Black')

    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

# create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# start game
deal()
frame.start()


