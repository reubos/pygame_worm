#! /usr/bin/env python

# Creates a worm which grows over time which you can move with the arrow keys

import pygame, random

# These are used for directions
UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)

worm_length = 30 #Initial worm size
worm_growrate = 2 # Worm grows once per given ticks (higher = slower)

j = 0

class MovingWorm:
    """ A moving pixel class. """

    def __init__(self, x, y, length):
        """ Creates a moving pixel. """
        self.x = x
        self.y = y
        self.hdir = 0
        self.vdir = -1
        self.length = length
        self.pixels = []
        for i in range(self.length,0,-1):
            self.pixels.append((x-i,y))
        self.alive = True

    def direction(self, pdir):
        """ Changes the pixels direction. """
        self.hdir, self.vdir = pdir

    def move(self):
        """ Moves the pixel. """
        self.x += self.hdir
        self.y += self.vdir
        #print j, worm_growrate
        if j % worm_growrate != 0:
            self.pixels.pop(0)
        if (self.x,self.y) not in self.pixels:
            self.pixels.append((self.x,self.y))
        else:
            print "Crash!"
            self.alive = False
    def draw(self, surface):
        for pixel in self.pixels:
            surface.set_at((pixel[0], pixel[1]), (255,255,255))

# Window dimensions
width = 640
height = 400

# Background colour
bgcolour = 0,0,0

screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
running = True

# Create a moving pixel.
pix = MovingWorm(width/2, height/2, 150)

while running:
    j += 1
    pix.move()

    #print pix.pixels

    if pix.x <= 0 or pix.x >= width or pix.y <= 0  or pix.y >= height:
        print "Crash!"
        running = False

    if not pix.alive:
        running = False
    
    screen.fill(bgcolour)
    pix.draw(screen)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                running = False
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pix.direction(UP)
                elif event.key == pygame.K_DOWN:
                    pix.direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    pix.direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    pix.direction(RIGHT)
    clock.tick(240)
    pygame.display.flip()
    pygame.time.wait(10)
