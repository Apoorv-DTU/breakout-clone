from random import randint
import threading
import sys
import pygame
from pygame.locals import *
import brick
from bat import Bat
from ball import Ball
from physics import *
from score import Score
from consts import *
import game

game_over = False
win = False

def start():
    init()
    play() 

def init():
    global game_over
    global win
    
    game_over = False
    win = False

def break_wall(ball_g, bricks_g):
    collisions = pygame.sprite.groupcollide(ball_g, bricks_g, False, False)
    if len(collisions) > 0:
        ball = ball_g.sprites()[0]
        bricks = collisions[ball]
        side = coll_side(bricks[0], ball)
        return bricks, side
    else:
        return None, None

def init_bricks(score, colour, y, points):
    bricks = []
    bs = pygame.sprite.RenderPlain()
    for i in range(30):
        size = rand_size()
        b = brick.Brick(score, colour, (i*30+(i*3)+8, y), points=points)
        bricks.append(b)
        bs.add(b)
    return bricks, bs

def init_wall(score):
    wall = []
    wall_g = pygame.sprite.RenderPlain()
    chart = {
    0: (255, 51, 51),
    1: (255, 153, 51),
    2: (255, 255, 51),
    3: (51, 255, 51),
    4: (51, 51, 255)
    }
    
    points = {0:20, 1:15, 2:10, 3:7, 4:4}
    
    for l in range(5):
        colour = chart[l]
        brick_line, brick_line_g = init_bricks(score ,colour, (l*32)+5, \
        points=points[l])
        wall.append(brick_line)
        wall_g.add(brick_line_g)
        
    return wall, wall_g 

def win_screen():
    global win
    win = True

def game_over_screen():
    global game_over
    game_over = True

def tutorial():
    t1 = game.notify("Move the bat using arrows (or mouse) ...", 
    colour=LIGHT_BLUE)
    while t1.isAlive() == True:
        pygame.time.wait(10)
    t1 = game.notify("... And shoot using SpaceBar.", colour=LIGHT_BLUE)        
    while t1.isAlive() == True:
        pygame.time.wait(10)
    t1 = game.notify("Prevent the ball from going down.", colour=RED)
    while t1.isAlive() == True:
        pygame.time.wait(10)
    game.notify("Press escape to pause the game.", colour=ORANGE)

def play():
    global game_over
    #initialize pygame & window
    screen = pygame.display.get_surface()
    
   
    #fill background
    bg = pygame.Surface((screen.get_size()))
    bg.fill(BG)
    bg = bg.convert()
    screen.blit(bg, (0, 0))
    
    #initialize scoreboard
    score_board = Score(bg)
    score_board.game_over = game_over_screen
    score_board.win = win_screen
   
    #initialize the wall (bricks)
    wall, wall_g = init_wall(score_board)
    
    #initialize the bat
    bat = Bat(10)
    batsprite = pygame.sprite.RenderPlain(bat)
    
    #initialize the ball
    ball = Ball((255, 255, 255), 5, bat, wall, score_board)
    ballsprite = pygame.sprite.RenderPlain(ball)
    
    clock = pygame.time.Clock()
    pause = False 
    game.init()

    t1 = threading.Thread(target=tutorial, args=())
    t1.start()

    out_count = 0

    while True:
        
        while pause == True:
            clock.tick(60)
            pygame.mouse.set_visible(True)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        bat.movepos = [0,0]
                        pause = False
                        game.resume()
                        game.notify("Game Resumed")
                              
                elif event.type == QUIT:
                    sys.exit(0)
                else:
                    game.handle_pause_event(event)
                    
        while game_over == True:
            clock.tick(60)
            pygame.mouse.set_visible(True)
            game.game_over_screen()
            pygame.display.flip()
            for event in pygame.event.get():                              
                if event.type == QUIT:
                    sys.exit(0) 
                else:
                    game.handle_event(event)
                    
        while win == True:
            clock.tick(60)
            pygame.mouse.set_visible(True)
            game.win_screen()
            pygame.display.flip()
            for event in pygame.event.get():                              
                if event.type == QUIT:
                    sys.exit(0) 
                else:
                    game.handle_win_event(event)
                
        #handle events
        while pause == False and game_over == False and win == False:
            clock.tick(60) #max frame rate
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        bat.moveleft()
                    elif event.key == K_RIGHT:
                        bat.moveright()   
                    elif event.key == K_SPACE:
                        screen.blit(bg, ball.rect, ball.rect)
                        ball.shoot()
                    elif event.key == K_ESCAPE:
                        pause = True 
                        game.pause()
                        
                elif event.type == KEYUP:
                    if event.key == K_LEFT or event.key == K_RIGHT:
                        bat.movepos = [0, 0]
                elif event.type == MOUSEMOTION:
                
                    pygame.mouse.set_visible(False)
                    
                    x, y = pygame.mouse.get_pos()
                    bx, by = bat.rect.midtop
                    if x > screen.get_width()-(bat.width/2):
                        x = screen.get_width()-(bat.width/2)
                        
                    elif x < bat.width/2:
                        x = bat.width/2
                        
                    screen.blit(bg, bat.rect, bat.rect)
                    bat.rect.midtop = (x,by)
            
            if not screen.get_rect().contains(ball.rect):
                out_count += 1
                if out_count >= 10:
                    score_board.die()  
            else:
                out_count = 0        
                      
            cols, side = break_wall(ballsprite, wall_g)
            
            if cols:
                if side is 'left' or side is 'right':
                    ball.deflect(1.5)
                if side is 'top' or side is 'bottom':
                    ball.deflect(2.5) 
                elif side == 'topright' or side == 'topleft':
                    ball.deflect(1)
                elif side == 'bottomright' or side == 'bottomleft':
                    ball.deflect(1)    
                else:
                    ball.deflect(1)
                for i in range(len(cols)):
                    cols[i].destroy()
                    
            side = coll_side(ball.area.get_rect(), ball.rect, True, True)
            if side == 'top':
                score_board.die()
        
            if score_board.updated_level != 0:
                print 'speed increased'
                ball.increment_speed = 3
            if pause == False:        
            	for y in range(5):
                    for i in range(30):
                        if wall[y][i].destroyed == False:
                            screen.blit(bg, wall[y][i].rect, wall[y][i].rect)
                            #wall[y][i].destroy()
                        
                        
                score_board.update()
                
                screen.blit(bg, bat.rect, bat.rect)
                screen.blit(bg, ball.rect, ball.rect)
                ballsprite.update()
                batsprite.update()
                ballsprite.draw(screen)
                batsprite.draw(screen)
                wall_g.draw(screen)
                
            pygame.display.update()
            
if __name__ == '__main__': start()
