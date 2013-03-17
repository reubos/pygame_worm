#! /usr/bin/env python

import pygame, random

# These are used for directions
UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)

worm_length = 30 #Initial worm size
worm_growrate = 20 # Worm grows once per given ticks (higher = slower)
number_of_obstacles = 15

food_eaten = 0
j = 0

class Food:
    """ The food. """

    def __init__(self, surface):
        """ Creates the food """
        self.surface = surface
        self.pos=(int(random.random() * 3*width/5 + width/5),\
                 int(random.random() * 3*height/5 + height/5))
        
            
    def move(self):
        self.pos=(int(random.random() * 3*width/5 + width/5),\
                 int(random.random() * 3*height/5 + height/5))

    def draw(self):
        for i in range(-5,6):
            for k in range(-5,6):
                if self.surface.get_at((self.pos[0]+i,self.pos[1]+k))\
                   ==bgcolour:
                   self.surface.set_at((self.pos[0]+i,self.pos[1]+k),(255,0,0))
                else:
                    self.move()
                    self.draw()
                    print "Redrawn at"
                    print self.pos
                    return
                

class Worm:
    """ A worm. """

    def __init__(self, surface, x, y, length):
        """ Creates a moving pixel. """
        self.surface = surface
        self.x = x
        self.y = y
        self.length = length
        self.dir_x = 0
        self.dir_y = -1
        self.body =[]
        self.crashed = False
        self.eating = False

    def key_event(self, event):
        """ Handle key events that affect the worm. """
        if event.key == pygame.K_UP:
            self.dir_x= 0
            self.dir_y = -1
        elif event.key == pygame.K_DOWN:
            self.dir_x = 0
            self.dir_y = 1
        elif event.key == pygame.K_LEFT:
            self.dir_x = -1
            self.dir_y = 0
        elif event.key == pygame.K_RIGHT:
            self.dir_x = 1
            self.dir_y = 0

    def move(self):
        """ Move the worm. """
        self.eating=False
        self.x += self.dir_x
        self.y += self.dir_y

        r,g,b,a = self.surface.get_at((self.x, self.y))
        if (r,g,b) == (255,255,255) or (r,g,b) == (0,255,0):
            self.crashed = True
        if (r,g,b) == (255,0,0):
            self.eating=True

        self.body.insert(0, (self.x, self.y))

        if len(self.body) > self.length:
            self.body.pop()

    def draw(self):
        for x,y in self.body:
            self.surface.set_at((x, y), (255,255,255))

# Window dimensions
width = 640
height = 400

# Background colour
bgcolour = 0,0,0

# Max FPS
maxfps = 80

screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
running = True

# Our worm. 
w1 = Worm(screen, width/2, height/2, worm_length)
f1 = Food(screen)

obspos=[]
for i in range(number_of_obstacles):
    obspos.append((int(random.random() * 3*width/5 + width/5),\
                 int(random.random() * 3*height/5 + height/5)))
    
while running:
    j+=1
    
    screen.fill(bgcolour)
    for i in obspos:
        for k in range(-5,6):
            for l in range(-5,6):
                screen.set_at((i[0]+k,i[1]+l),(0,255,0))

    f1.draw()
    w1.draw()
    w1.move()

    if w1.eating:
        print "Yummy!"
        food_eaten+=1
        print food_eaten
        f1.move()

    if (j%worm_growrate==0):
        w1.length += 1


            

    if w1.crashed or w1.x<=0 or w1.x>=width-1 or w1.y<=0 or w1.y>=height-1:
        print "Crash!"
        running = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                running = False
        elif event.type == pygame.KEYDOWN:
                w1.key_event(event)
    pygame.display.flip()
    clock.tick(maxfps)

pygame.quit()
