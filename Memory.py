# implementation of card game - Memory
# written in python 2.6
# only works on codeskulptor.org

import simplegui
import random
click1 = 0
click2 = 0
list1 = [0,1,2,3,4,5,6,7] 
list2 = [0,1,2,3,4,5,6,7]
deck_cards = list1 + list2
turns = 0
state = 0

# helper function to initialize globals
def new_game():
    global deck_cards, turns, state, exposed
    state = 0
    turns = 0
    random.shuffle(deck_cards)
    exposed = [False for num in range(len(deck_cards))]
    label.set_text('Turn(s): ' + str(turns))

    
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed, state, deck_cards, click1, click2, turns
    choice = (pos[0] // 50)
    if state == 0:
        exposed[choice] = True
        click1 = choice
        state = 1
    elif state == 1:
        if exposed[choice] == True:
            pass
        else:
            exposed[choice] = True
            click2 = choice
            turns += 1
            state = 2
    elif state ==2:
        if deck_cards[click1] != deck_cards[click2]:
            exposed[click1] = False
            exposed[click2] = False
        exposed[choice] = True
        click1 = choice
        state = 1
        
    label.set_text('Turn(s): ' + str(turns))
    
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(16):
        if exposed[i]:
            canvas.draw_text(str(deck_cards[i]), (50*i+10, 60), 40, "Blue")
        else:
            canvas.draw_polygon([(50*i, 0), (50*i, 100), (50*i + 50, 100), (50*i + 50, 0)], 3, "White", "Red")
    


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
frame.set_canvas_background('White')
label = frame.add_label('Turn(s): ' + str(turns), 100)


# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)


# get things rolling
new_game()
frame.start()
