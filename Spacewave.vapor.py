## Program only works in codeskulptor.org

# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
high_score = 0
lives = 3
time = 0
started = False

ANGULAR_VEL = .1
ACCELERATION = .15
FRICTION = .98
SCALE = 4.5
MISSILE_VEL = 10

explosion_group = set([])
EXPLOSION_CENTER = [64, 64]
EXPLOSION_SIZE = [128, 128]
EXPLOSION_DIM = 24 

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# vaporwave background 1
tokyo_rain_info = ImageInfo([800, 532],[1600, 1064])
tokyo_rain_image = simplegui.load_image('http://i.imgur.com/j1DWGOB.jpg')

# vaporwave background 2
vaporwave_background_info = ImageInfo([600, 392],[1200, 784])
vaporwave_background_image = simplegui.load_image('https://mir-s3-cdn-cf.behance.net/project_modules/max_1200/45563229856031.5611fc1811e24.png')

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# Title theme
title_info = ImageInfo([1024, 674], [2048, 1347])
title_image = simplegui.load_image('https://dl.dropbox.com/s/cm89tert7hx3u0r/REALFINAL.png?dl=0')

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")

# microsoft logo
logo_info = ImageInfo([592, 552], [1185, 1104], 60) 
logo_image = simplegui.load_image('http://vignette4.wikia.nocookie.net/logopedia/images/2/29/Windows_95_Logo.svg/revision/latest?cb=20160811163821')

# greek bust image
greek_bust_info = ImageInfo([204, 250],[408, 500], 50)
greek_bust_image = simplegui.load_image('https://dl.dropbox.com/s/6dxp45cawtg1u23/Greek%20bust.png?dl=0')

# vaporwave plant image
plant_info = ImageInfo([760, 800],[1520,1600], 20, 800)
plant_image = simplegui.load_image('https://d1v8u1ev1s9e4n.cloudfront.net/54d106955ccacf24ac356fe8')

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
macintosh_plus_sound = simplegui.load_sound('https://dl.dropbox.com/s/xlju2uiwputbg3s/Macintosh%20Plus%20-%20Floral%20Shoppe%20-%2002%20%E3%83%AA%E3%82%B5%E3%83%95%E3%83%A9%E3%83%B3%E3%82%AF420%20-%20%E7%8F%BE%E4%BB%A3%E3%81%AE%E3%82%B3%E3%83%B3%E3%83%94%E3%83%A5%E3%83%BC.mp3?dl=0')
# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def rotate_clockwise(self):
        self.angle_vel += ANGULAR_VEL
    def rotate_counter_clockwise(self):
        self.angle_vel -= ANGULAR_VEL
       
    def thrusters_on(self):
        self.thrust = True
        ship_thrust_sound.rewind()
        ship_thrust_sound.play()
    def thrusters_off(self):
        self.thrust = False
        ship_thrust_sound.pause()
        
    def shoot(self):
        global missile_group 
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + MISSILE_VEL * forward[0], self.vel[1] + MISSILE_VEL * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
        
    def draw(self,canvas):
        canvas.draw_image(ship_image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
            
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel
        self.vel[0] *= FRICTION
        self.vel[1] *= FRICTION
     
        if self.thrust == True:
            self.vel[0] += angle_to_vector(self.angle)[0] * ACCELERATION
            self.vel[1] += angle_to_vector(self.angle)[1] * ACCELERATION
            self.image_center[0] = 45 + 90
        else:
            self.image_center[0] = 45
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
            
    def collide(self, other_object):
        if dist([self.pos[0], self.pos[1]], [other_object.pos[0], other_object.pos[1]]) < self.radius + other_object.radius:
            return True
        return False
           
    def draw(self, canvas):
        global time
        if self.animated == True:
            explosion_index = (time % EXPLOSION_DIM) // 1
            current_explosion_center = [EXPLOSION_CENTER[0] +  explosion_index * EXPLOSION_SIZE[0], EXPLOSION_CENTER[1]]
            canvas.draw_image(explosion_image, current_explosion_center, EXPLOSION_SIZE, self.pos, EXPLOSION_SIZE) 
            time += 1
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size , self.pos, self.image_size, self.angle)
        
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel
        
        if self.lifespan:
            if self.age > self.lifespan:
                return True
            else: self.age += 1
        return False

# various sprite classes to process image sizes accordingly
class SmallerSprite(Sprite):
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size , self.pos , [self.image_size[0] / SCALE, self.image_size[1] / SCALE], self.angle)
class SmallestSprite(Sprite):
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size , self.pos , [self.image_size[0]/8, self.image_size[1]/8], self.angle)
class SmallestSpriteEver(Sprite):
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size , self.pos , [self.image_size[0] / 25, self.image_size[1] / 25], self.angle)

# draws sprites on the canvas    
def process_sprite_group(group, canvas):
    other_group = set([])
    for i in group:
        i.draw(canvas)
        i.update()
        if i.update() == True:
            other_group.add(i)
    return group.difference_update(other_group)

# Collision helper functions to determine weather 2 objects collide
def group_collide(group, other_object):
    global explosion_group
    collided_group = set([])
    for i in group:
        if i.collide(other_object):
            collided_group.add(i)
            explosion_group.add(Sprite(i.pos, [0,0], i.angle, i.angle_vel, explosion_image, explosion_info, explosion_sound))
            group.difference_update(collided_group)
            return True

def group_group_collide(group, other_group):
    total = 0
    for i in set(group):
        collision = group_collide(other_group, i)
        if collision == True:
            group.remove(i)
            total += 1
    return total
            
def exit_game():
    frame.stop()
    macintosh_plus_sound.pause()
    
def draw(canvas):
    global time, lives, score, started, greek_heads, high_score
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    
    #canvas.draw_image(tokyo_rain_image, tokyo_rain_info.get_center(), tokyo_rain_info.get_size(), [WIDTH /2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(vaporwave_background_image, vaporwave_background_info.get_center(), vaporwave_background_info.get_size(), [WIDTH /2, HEIGHT / 2], [WIDTH, HEIGHT])
    #canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw/update ship and sprites
    my_ship.draw(canvas)
    my_ship.update()
    process_sprite_group(greek_heads, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    process_sprite_group(plant_group, canvas)
    
    # draw score text
    canvas.draw_text('Score: ' + str(score), [625, 50], 24, 'Pink')
    canvas.draw_text('Lives: ' + str(lives), [625, 75], 24, 'Cyan')
    canvas.draw_text('High Score: ' + str(high_score), [625, 575], 24, 'indigo')
    
    if not started:
        canvas.draw_image(title_image, title_info.get_center(), 
                          title_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          (title_info.get_size()[0]/SCALE, title_info.get_size()[1]/SCALE))

    if group_collide(greek_heads, my_ship) == True:
        lives -= 1
    if group_group_collide(greek_heads, missile_group) == True:
        score += 10
    if group_group_collide(plant_group, missile_group) == True:
        score += 50
        
    if score > high_score:
        high_score = score
    if lives <= 0:
        started = False
        lives = 3
        score = 0
        greek_heads = set([])
    
# timer handler that spawns a rock

def rock_spawner():
    global greek_heads
    if started:
        greek_bust_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        greek_bust_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
        greek_bust_avel = random.random() * .2 -.1
        greek_bust = random.choice([SmallerSprite(greek_bust_pos, greek_bust_vel, 0, greek_bust_avel, greek_bust_image, greek_bust_info), SmallestSprite(greek_bust_pos, greek_bust_vel, 0, greek_bust_avel, logo_image, logo_info)]) 
        if len(greek_heads) <= 11:
            greek_heads.add(greek_bust)
        
def plant_spawner():
    global plant_group
    if started:
        plant_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        plant_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
        plant_avel = random.random() * .2 -.1
        plant = SmallestSpriteEver(plant_pos, plant_vel, 0, plant_avel, plant_image, plant_info)
        if len(plant_group) <= 0:
            plant_group.add(plant)
    
# initialize frame
frame = simplegui.create_frame("spacewave. ~V A P O R~", WIDTH, HEIGHT)

# initialize ship and sprite groups
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
greek_heads = set([])
missile_group = set([])
plant_group = set([])

# define key handlers
inputs = {'left' : [my_ship.rotate_counter_clockwise, my_ship.rotate_clockwise], 
          'right' : [my_ship.rotate_clockwise, my_ship.rotate_counter_clockwise],
          'up' : [my_ship.thrusters_on, my_ship.thrusters_off],
          'space' : [my_ship.shoot, None], 'e' : [exit_game, None]}

def keydown(key):
    for i in inputs:
        if key == simplegui.KEY_MAP[i]:
            inputs[i][0]()
        
def keyup(key):
    for i in inputs:
        if key == simplegui.KEY_MAP[i] and i != 'space' and i != 'e':
            inputs[i][1]() 

def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        macintosh_plus_sound.play()
        started = True
        
# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)
timer2 = simplegui.create_timer(random.randrange(7500.0, 25000.0), plant_spawner)

# get things rolling
timer.start()
timer2.start()
frame.start()
ship_thrust_sound.set_volume(.4)
macintosh_plus_sound.set_volume(.2)
