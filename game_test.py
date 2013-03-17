#! /usr/bin/env python

import pygame, random

# These are used for directions
UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)

worm_length = 30 #Initial worm size
worm_growrate = 20 # Worm grows once per given ticks (higher = slower)
number_of_worms = 1

j = 0

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
        self.x += self.dir_x
        self.y += self.dir_y
        
        if (self.x, self.y) in self.body:
            self.crashed = True

        self.body.insert(0, (self.x, self.y))

        if len(self.body) > self.length:
            self.body.pop()

    def draw(self):
        for i in range(len(self.body)):
            self.surface.set_at(self.body[i], (255-i*255/self.length,\
                                               255-i*255/self.length,\
                                               255))

    def __repr__(self):
        return "%d,%d" % (self.x,self.y)

# Window dimensions
width = 640
height = 400

# Background colour
bgcolour = 0,0,255

# Max FPS
maxfps = 120

screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
running = True

# Our worm.
worms = []
for i in range(number_of_worms):
    worms.append(Worm(screen, (i+1)*width/(number_of_worms+1),\
                      (i+1)*height/(number_of_worms+1),\
                      worm_length))
print worms
while running:
    j+=1
    
    screen.fill(bgcolour)
    for w in worms:
        w.move()
        w.draw()

    if (j%worm_growrate==0):
        worms[0].length += 1

    for w in range(number_of_worms):
        if worms[w].crashed:
            print "Crash1!"
            print worms[w]
            running = False
        elif worms[w].x<=0 or worms[w].x>=width-1 or worms[w].y<=0 \
             or worms[w].y>=height-1:
            print "Crash2!"
            print worms[w]
            running = False
        else:
            for v in range(w+1,number_of_worms):
                if (worms[w].x,worms[w].y) in worms[v].body:
                    print "Crash3!"
                    print worms[w]
                    print worms[v]
                    running = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                running = False
        elif event.type == pygame.KEYDOWN:
            for w in range(number_of_worms):
                worms[w].key_event(event)
    pygame.display.flip()
    clock.tick(maxfps)

pygame.quit()
