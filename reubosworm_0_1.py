#! /usr/bin/env python

import pygame, random, shelve, sys, os

# Import the highscores
save_game = shelve.open('save')
highscore = save_game.get('highscores') # load highscore for easy
if highscore == None:
    highscore = [0,0,0,0]
    save_game['highscores'] = [0,0,0,0]
    
save_game.close

##print highscore

# These are used for directions
UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)

# Enable food in game
food = True

# Set the colours for objects ingame
wormcolour = 255,255,0
obscolour = 0,255,0
foodcolour = 255,0,0

# The HUD settings
hud_font = "ShareTechMono-Regular.ttf" # Font used for score and lives
hud_font_size = 16 # Size of HUD font
hud_font_colour = 255,255,255 # Colour of HUD font
hudcolour = 51,204,255 # Colour of HUD background
hud_thickness = 20 # Thickness of top of HUD

# Window dimensions
width = 640
height = 400

# Background colour
bgcolour = 0,0,0

# Max FPS
maxfps = 80

pygame.font.init()
score_font = pygame.font.Font(hud_font,hud_font_size)

s = raw_input("Diffculty (1-4): ")
if 0<int(s) and int(s) <5:
    difficulty = int(s)
else:
    difficulty = 1
if difficulty == 1:
    worm_length = 30 # Initial worm size
    worm_growrate = 0 # Worm grows once per given ticks (higher = slower)
    wormspeed = 1 # The starting speed of the worm (pixels/tick)
    wormaccelerate = 0 # Worm accelerates one per given ticks
    worm_accelerate_on_eat = 100 # Worm accelerates after given amount of food
    worm_grow_on_eat = 25 # Worm grows by given amount of pixels on eating
    number_of_obstacles = 0 # Given number of obstacles appear on screen
    starting_lives = 3 # Worm has chances to die and start over
elif difficulty == 2:
    worm_length = 40
    worm_growrate = 150
    wormspeed = 2
    wormaccelerate = 0
    worm_accelerate_on_eat = 20
    worm_grow_on_eat = 50
    number_of_obstacles = 2
    starting_lives = 2
elif difficulty == 3:
    worm_length = 40
    worm_growrate = 100
    wormspeed = 3
    wormaccelerate = 0
    worm_accelerate_on_eat = 10
    worm_grow_on_eat = 100
    number_of_obstacles = 5
    starting_lives = 0
elif difficulty == 4:
    worm_length = 40
    worm_growrate = 10
    wormspeed = 3
    wormaccelerate = 1000
    worm_accelerate_on_eat = 10
    worm_grow_on_eat = 100
    number_of_obstacles = 5
    starting_lives = 0

# The Menu Settings
menu_font_colour = 255,255,255
menu_font_size = 16
menu_font = "AveriaGruesaLibre-Regular.ttf"
menu_title_font = "Lobster.ttf"
menu_title_font_size = 50
highscore_colour = 255,0,0


class Menu:
    """ The menu. """

    def __init__(self, surface, colour, font, title_font, size, title_size,\
                 highscore_colour):
        """ Initialises the menu """
        self.surface = surface
        self.colour = colour
        self.font = pygame.font.Font(font, size)
        self.title_font = pygame.font.Font(title_font, title_size)
        self.subtitle_font = pygame.font.Font(title_font, size)
        self.highscore_colour = highscore_colour
        self.on_screen = "Main"

    def draw(self):
        self.surface.fill(bgcolour)
        new_highscore_text = self.font.render(\
            "NEW HIGHSCORE!!!",False,self.highscore_colour)
        menu_title_text = self.title_font.render(\
            "PTHYON",False,self.colour)
        by_reubos_text = self.subtitle_font.render(\
            "by reubos",False,self.colour)
        start_game_text = self.font.render(\
            "[SPACE] START GAME",False,self.colour)
        highscores_text = self.font.render("[H]IGHSCORES",False,self.colour)
        options_text = self.font.render("[O]PTIONS",\
                                            False,self.colour)
        quit_text = self.font.render("[ESC] QUIT",False,self.colour)
        if new_highscore:
            self.surface.blit(new_highscore_text, (0,0))
        self.surface.blit(menu_title_text, (213,74))
        self.surface.blit(by_reubos_text, (403,119))
        self.surface.blit(start_game_text, (213,136))
        self.surface.blit(highscores_text, (213,156))
        self.surface.blit(options_text, (213,176))
        self.surface.blit(quit_text, (213,216))

        pygame.display.flip()
        self.alive = True

    def disp_options(self):
        self.surface.fill(bgcolour)

        score_colour = [self.colour,self.colour,self.colour,self.colour]
        score_colour[difficulty-1] = self.highscore_colour
        options_title_text = self.title_font.render(\
            "OPTIONS",False,self.colour)
        diff1_text = self.font.render(\
            "[1] EASY",False,score_colour[0])
        diff2_text = self.font.render(\
            "[2] MEDIUM",False,score_colour[1])
        diff3_text = self.font.render(\
            "[3] HARD",False,score_colour[2])
        diff4_text = self.font.render(\
            "[4] HARDER",False,score_colour[3])
        back_text = self.font.render(\
            "[B] ACK",False,self.colour)
        self.surface.blit(options_title_text, (213,74))
        self.surface.blit(diff1_text, (213,129))
        self.surface.blit(diff2_text, (213,149))
        self.surface.blit(diff3_text, (213,169))
        self.surface.blit(diff4_text, (213,189))
        self.surface.blit(back_text, (213,229))
        
        pygame.display.flip()

    def disp_highscores(self):
##        print "disp_hs_loaded"
        self.surface.fill(bgcolour)
        score_colour = [self.colour,self.colour,self.colour,self.colour]
        new_highscore_text = self.font.render(\
            "NEW HIGHSCORE!!!",False,self.highscore_colour)
        if new_highscore:
            self.surface.blit(new_highscore_text, (0,0))
            if difficulty == 1:
                score_colour[0] = self.highscore_colour
            elif difficulty == 2:
                score_colour[1] = self.highscore_colour
            elif difficulty == 3:
                score_colour[2] = self.highscore_colour
            elif difficulty == 4:
                score_colour[3] = self.highscore_colour

        hs_title_text = self.title_font.render(\
            "HIGHSCORES",False,self.colour)
        diff1_hs_text = self.font.render(\
            "EASY  ",False,score_colour[0])
        diff1_hs = self.font.render(\
            str(highscore[0]),False,score_colour[0])
        diff2_hs_text = self.font.render(\
            "MEDIUM  ",False,score_colour[1])
        diff2_hs = self.font.render(\
            str(highscore[1]),False,score_colour[1])
        diff3_hs_text = self.font.render(\
            "HARD  ",False,score_colour[2])
        diff3_hs = self.font.render(\
            str(highscore[2]),False,score_colour[2])
        diff4_hs_text = self.font.render(\
            "HARDER  ",False,score_colour[3])
        diff4_hs = self.font.render(\
            str(highscore[3]),False,score_colour[3])
        back_text = self.font.render(\
            "[B]ACK",False,self.colour)
        self.surface.blit(hs_title_text, (213,74))
        self.surface.blit(diff1_hs_text, (213,129))
        self.surface.blit(diff1_hs, (313,129))
        self.surface.blit(diff2_hs_text, (213,149))
        self.surface.blit(diff2_hs, (313,149))
        self.surface.blit(diff3_hs_text, (213,169))
        self.surface.blit(diff3_hs, (313,169))
        self.surface.blit(diff4_hs_text, (213,189))
        self.surface.blit(diff4_hs, (313,189))
        self.surface.blit(back_text, (213,229))
        pygame.display.flip()

    def key_event(self, event):
        """ Handle key events that affect the worm. """
        if event.key == pygame.K_SPACE:
            self.alive = False
        elif event.key == pygame.K_h:
            self.disp_highscores()
            self.on_screen = "Highscores"
        elif event.key == pygame.K_b:
            self.draw()
            self.on_screen = "Main"
        elif event.key == pygame.K_o:
            self.disp_options()
            self.on_screen = "Options"
        elif event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    def set_alive(self, boolval):
        self.alive = boolval
    
                              

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
chomp = pygame.mixer.Sound("chomp.wav") # The eating food sound
oh_no = pygame.mixer.Sound("oh_no.wav") # The crash sound

def game_init():
    global score, j, ac, fc, lives, w1, f1, obspos, menu, new_highscore
    score = 0
    j = 0
    ac = 0
    fc = 0
    lives = starting_lives
    w1 = Worm(screen, width/2, height/2, worm_length, wormcolour, wormspeed)
    f1 = Food(screen, foodcolour)
    menu = Menu(screen, menu_font_colour, menu_font, \
                menu_title_font, menu_font_size, menu_title_font_size,\
                highscore_colour)
    menu.draw()
##    print "menu drawn"
    while menu.alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                menu.key_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print event.pos
    screen.fill(bgcolour)
    f1.draw()
    obspos=[]
    for i in range(number_of_obstacles):
        obspos.append((int(random.random() * 3*width/5 + width/5),\
                       int(random.random() * 3*height/5 + height/5)))
    new_highscore = False
##    pygame.time.delay(2000)

def new_life():
    global j, ac, fc, w1, f1, obspos
    screen.fill(bgcolour)
    j = 0
    ac = 0
    fc = 0
    w1 = Worm(screen, width/2, height/2, worm_length, wormcolour, wormspeed)
    f1 = Food(screen, foodcolour)
    f1.draw()
    obspos=[]
    for i in range(number_of_obstacles):
        obspos.append((int(random.random() * 3*width/5 + width/5),\
                       int(random.random() * 3*height/5 + height/5)))


new_highscore = False
game_init()
while running:
    pygame.draw.rect(screen,hudcolour,(0,0,width,hud_thickness))
    pygame.draw.rect(screen,hudcolour,(0,0,5,height))
    pygame.draw.rect(screen,hudcolour,(width-5,0,5,height))
    pygame.draw.rect(screen,hudcolour,(0,height-5,width,5))
    score_text = score_font.render("Score:"+str(score), False, hud_font_colour)
    lives_text = score_font.render("Lives:"+str(lives), False, hud_font_colour)
    screen.blit(score_text, (0,0))
    screen.blit(lives_text, (width-80,0))
    j+=1
    ac+=1
    
##    screen.fill(bgcolour)
    for i in obspos:
        pygame.draw.rect(screen,obscolour,(i[0],i[1],11,11),0)
##    if food: f1.draw()
    if len(w1.body) > 0:
        w1.draw()
    w1.move()
    if food:
        if w1.eating:
            fc+=1
            if (fc%worm_accelerate_on_eat==0):w1.speed += 1
            score+=1
##            print "Score: %d" % score
            chomp.play()
            f1.erase()
            f1.move()
            f1.draw()

    if worm_growrate != 0:
        if (j%worm_growrate==0): w1.grow_to += 1
    if wormaccelerate != 0:
        if (ac%wormaccelerate==0): w1.speed += 1

    if w1.crashed or w1.pos[0]<=0 or w1.pos[0]>=width-1 or \
       w1.pos[1]<=0 or w1.pos[1]>=height-1:
        print "Crash!"
        oh_no.play()
        if lives == 0:
            if score > highscore[difficulty-1]:
                highscore[difficulty-1] = score
                new_highscore = True
                print "New Highscore!"
            print "Your score: %d" % score
            print "highscore: %d" %highscore[difficulty-1]
            save_game = shelve.open('save')
            print 
            save_game['highscores'] = highscore
##            print save_game['highscores']
            save_game.close()

            game_init()
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
