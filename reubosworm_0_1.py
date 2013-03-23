#! /usr/bin/env python

import pygame, random, shelve, sys, os
from vector2d import *

save_game = shelve.open('save')
highscore = save_game.get('highscore')
save_game.close

# These are used for directions
UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)


food = True
wormcolour = 255,255,0
obscolour = 0,255,0
foodcolour = 255,0,0
hudcolour = 51,204,255

hud_font_size = 16
hud_font_colour = 255,255,255
hud_thickness = 20

pygame.font.init()
score_font = pygame.font.Font("ShareTechMono-Regular.ttf",hud_font_size)

s = raw_input("Diffculty (1-3): ")
if 0<int(s) and int(s) <4:
    difficulty = int(s)
else:
    difficulty = 1
if difficulty == 1:
    worm_length = 30 #Initial worm size
    worm_growrate = 0 # Worm grows once per given ticks (higher = slower)
    wormspeed = 1
    worm_grow_on_eat = 25
    number_of_obstacles = 0
    starting_lives = 3
    maxfps = 80
elif difficulty == 2:
    worm_length = 40
    worm_growrate = 150
    wormspeed = 2
    worm_grow_on_eat = 50
    number_of_obstacles = 2
    starting_lives = 2
    maxfps = 150
elif difficulty == 3:
    worm_length = 40
    worm_growrate = 100
    wormspeed = 3
    worm_grow_on_eat = 100
    number_of_obstacles = 5
    starting_lives = 0
    maxfps = 300

# Window dimensions
width = 640
height = 400

# Background colour
bgcolour = 0,0,0

# Max FPS
maxfps = 80

class Food:
    """ The food. """

    def __init__(self, surface, colour):
        """ Creates the food """
        self.surface = surface
##        self.pos=(int(random.random() * 3*width/5 + width/5),\
##                 int(random.random() * 3*height/5 + height/5))
        self.colour = colour
        self.move()
        
            
    def move(self):
        self.pos=(int(random.random() * 3*width/5 + width/5),\
                 int(random.random() * 3*height/5 + height/5))
        for i in range(0,11):
            for k in range(0,11):
                if self.surface.get_at((self.pos[0]+i,self.pos[1]+k))\
                   !=bgcolour:
                    self.move()
                    print "Redrawn at"
                    print self.pos
                    return

    def draw(self):
        pygame.draw.rect(self.surface, self.colour,\
                         (self.pos[0],self.pos[1],11,11), 0)

    def erase(self):
        pygame.draw.rect(self.surface, bgcolour, (self.pos[0], self.pos[1], \
                                                  11, 11))
                               


    def position(self):
        return self.pos
                

class Worm:
    """ A worm. """

    def __init__(self, surface, x, y, length,colour,speed):
        """ Creates a moving pixel. """
        self.surface = surface
        self.pos = (x,y)
        self.length = 1
        self.grow_to = length
        self.speed = speed
        self.speedvec = (0,-speed)
        self.dir = UP
        self.body =[]
        self.crashed = False
        self.eating = False
        self.colour = colour

    def key_event(self, event):
        """ Handle key events that affect the worm. """
        if event.key == pygame.K_UP:
            if self.dir == DOWN: return
            self.dir = UP
        elif event.key == pygame.K_DOWN:
            if self.dir == UP: return
            self.dir = DOWN
        elif event.key == pygame.K_LEFT:
            if self.dir == RIGHT: return
            self.dir = LEFT
        elif event.key == pygame.K_RIGHT:
            if self.dir == LEFT: return
            self.dir = RIGHT

    def move(self):
        """ Move the worm. """
        self.eating=False

        for i in range(0,self.speed):
            self.pos = tuple(sum(t) for t in zip(self.pos,self.dir))
            self.body.insert(0, self.pos)
            
        r,g,b,a = self.surface.get_at(self.pos)
        if (r,g,b) == wormcolour or (r,g,b) == obscolour or \
           (r,g,b) == hudcolour:
            self.crashed = True
        if (r,g,b) == foodcolour:
            self.eating=True
            self.grow_to += worm_grow_on_eat



        if (self.grow_to > self.length):
            self.length += self.speed

        if len(self.body) > self.length:
            for i in range(0,self.speed):
                self.body.pop()

    def draw(self):
##        for x,y in self.body:
##            self.surface.set_at((x, y), self.colour)
        for x,y in self.body[:self.speed]:
            #print "pixel at " + str(x) + "," + str(y)
            self.surface.set_at((x,y), self.colour)
        for x,y in self.body[-self.speed:]:
            #print "pixel removed at " + str(x) + "," + str(y)
            self.surface.set_at((x,y), bgcolour)

    def position(self):
        return self.x,self.y

    def eat(self):
        self.grow_to += worm_grow_on_eat



screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
running = True

pygame.mixer.init()
chomp = pygame.mixer.Sound("chomp.wav")
oh_no = pygame.mixer.Sound("oh_no.wav")

def game_init():
    global score, j, lives, w1, f1, obspos
    screen.fill(bgcolour)
    score = 0
    j = 0
    lives = starting_lives
    w1 = Worm(screen, width/2, height/2, worm_length, wormcolour, wormspeed)
    f1 = Food(screen, foodcolour)
    f1.draw()
    obspos=[]
    for i in range(number_of_obstacles):
        obspos.append((int(random.random() * 3*width/5 + width/5),\
                       int(random.random() * 3*height/5 + height/5)))
    pygame.time.delay(2000)

def new_life():
    global j, w1, f1, obspos
    screen.fill(bgcolour)
    j = 0
    w1 = Worm(screen, width/2, height/2, worm_length, wormcolour, wormspeed)
    f1 = Food(screen, foodcolour)
    f1.draw()
    obspos=[]
    for i in range(number_of_obstacles):
        obspos.append((int(random.random() * 3*width/5 + width/5),\
                       int(random.random() * 3*height/5 + height/5)))


game_init()
while running:
    pygame.draw.rect(screen,hudcolour,(0,0,width,hud_thickness))
    score_text = score_font.render("Score:"+str(score), False, hud_font_colour)
    lives_text = score_font.render("Lives:"+str(lives), False, hud_font_colour)
    screen.blit(score_text, (0,0))
    screen.blit(lives_text, (width-80,0))
    j+=1
    
##    screen.fill(bgcolour)
    for i in obspos:
        pygame.draw.rect(screen,obscolour,(i[0],i[1],11,11),0)
##    if food: f1.draw()
    if len(w1.body) > 0:
        w1.draw()
    w1.move()
    if food:
        if w1.eating:
            score+=1
            print "Score: %d" % score
            chomp.play()
            f1.erase()
            f1.move()
            f1.draw()

    if worm_growrate != 0:
        if (j%worm_growrate==0): w1.grow_to += 1

    if w1.crashed or w1.pos[0]<=0 or w1.pos[0]>=width-1 or \
       w1.pos[1]<=0 or w1.pos[1]>=height-1:
        print "Crash!"
        oh_no.play()
        if lives == 0:
            if score > highscore:
                highscore = score
            print "Your score: %d" % score
            print "highscore: %d" %highscore
            s = raw_input("Play again? y/n\n")
            if s == 'y':
                game_init()
            else:
                save_game = shelve.open('save')
                save_game['highscore'] = highscore
                save_game.close()
                running = False
        else:
            lives -= 1
            print "Lives remaining: %d" % lives
            new_life()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                running = False
        elif event.type == pygame.KEYDOWN:
                w1.key_event(event)
    pygame.display.flip()
    clock.tick(maxfps)

pygame.quit()
sys.exit()
