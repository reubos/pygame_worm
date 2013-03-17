#! /usr/bin/env python

import pygame, random

# These are used for directions
UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)

worm_length = 30 #Initial worm size
worm_growrate = 20 # Worm grows once per given ticks (higher = slower)

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

        r,g,b,a = self.surface.get_at((self.x, self.y))
        if (r,g,b) == (255,255,255):
            self.crashed = True

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

while running:
    j+=1
    
    screen.fill(bgcolour)
    w1.draw()
    w1.move()

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
