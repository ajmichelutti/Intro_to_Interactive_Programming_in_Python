# Implementation of classic arcade game Pong
# Written in python 2.6
# only works on codeskulptor.org
import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = True


ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [3, random.randint(-3,3)]

paddle1_pos = HEIGHT /2
paddle2_pos = HEIGHT /2
paddle1_vel = 0
paddle2_vel = 0

score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel, LEFT # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    if LEFT:
        ball_vel = [-3, random.randint(-3,3)]
    elif not LEFT:
        ball_vel = [3, random.randint(-3,3)]
        


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(ball_vel)
    paddle1_pos = HEIGHT /2
    paddle2_pos = HEIGHT /2
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel, LEFT
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
    # draw ball
    canvas.draw_circle(ball_pos, 25, 1, "white", "white")
    
    # update paddle's vertical position, keep paddle on the screen
    
    if (paddle1_pos <= HEIGHT - HALF_PAD_HEIGHT and paddle1_vel > 0) or (paddle1_pos >= HALF_PAD_HEIGHT and paddle1_vel < 0) :
        paddle1_pos += paddle1_vel    
    elif (paddle2_pos <= HEIGHT - HALF_PAD_HEIGHT and paddle2_vel > 0) or (paddle2_pos >= HALF_PAD_HEIGHT and paddle2_vel < 0) :
        paddle2_pos += paddle2_vel  
   
    # draw paddles
    canvas.draw_polygon([[0, paddle1_pos + HALF_PAD_HEIGHT], [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], [PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], [0, paddle1_pos - HALF_PAD_HEIGHT]], 2, 'yellow', 'yellow')
    canvas.draw_polygon([[WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], [WIDTH, paddle2_pos + HALF_PAD_HEIGHT], [WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT]], 2, 'red', 'red')
    
    # determine whether paddle and ball collide 
    
    if (ball_pos[0] < (BALL_RADIUS + PAD_WIDTH)) and (ball_pos[1] < (paddle1_pos + HALF_PAD_HEIGHT + BALL_RADIUS)) and (ball_pos[1] > (paddle1_pos - HALF_PAD_HEIGHT - BALL_RADIUS)):
        ball_vel[0] = -(ball_vel[0] - .5)
    
    elif (ball_pos[0] > (WIDTH -(BALL_RADIUS + PAD_WIDTH))) and (ball_pos[1] < (paddle2_pos + HALF_PAD_HEIGHT + BALL_RADIUS)) and (ball_pos[1] > (paddle2_pos - HALF_PAD_HEIGHT - BALL_RADIUS)):
        ball_vel[0] = -(ball_vel[0] + .5)
        
    elif (ball_pos[0] < (BALL_RADIUS + PAD_WIDTH)):
        LEFT = False
        spawn_ball(ball_vel)
        score1 += 1
        
         
    elif (ball_pos[0] > (WIDTH -(BALL_RADIUS + PAD_WIDTH))):
        LEFT = True
        spawn_ball(ball_vel)
        score2 += 1
        
        
        
   
    # draw scores
    canvas.draw_text(str(score2) + '/' + str(score1), (50,50), 36, 'green')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 5
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel = -5
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 5
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = -5
                              
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('New Game', new_game, 100)


# start frame
new_game()
frame.start()
