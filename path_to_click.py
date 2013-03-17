#! /usr/bin/env python

import pygame

x = y = 0
running = 1
width = 640
height = 416
bgcolour = 0,255,0
screen = pygame.display.set_mode((width, height))
mouse_x = -1
mouse_y = 0

while running:
    event = pygame.event.poll()
    screen.fill(bgcolour) 
    if event.type == pygame.QUIT:
        running = 0
    elif event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x,mouse_y = event.pos
        mouse_x = mouse_x/32
        mouse_y = (height - mouse_y)/32
        print "mouse at (%d, %d)" % (mouse_x,mouse_y)

    for i in range(0,mouse_x):
        pygame.draw.rect(screen, (255,0,0), (1+32*i,height-31,31,31))
    for i in range(0,mouse_y+1):
        pygame.draw.rect(screen, (255,0,0), (1+32*mouse_x,
                                             height-32*i+1,31,31))



    for i in range(0,width,32):
        pygame.draw.line(screen,(0,0,0),(i,0),(i,height-1))
    for i in range(0,height,32):
        pygame.draw.line(screen,(0,0,0),(0,i),(width-1,i))
        

    pygame.display.flip()
