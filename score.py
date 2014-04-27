import sys
import pygame
from consts import *

class Score(object):
    def __init__(self, bg=None, score=0):
        self.lives = 3
        self.score = score
        self.level = 1
        self.prev = score
        self.score_rect = pygame.Rect((10,0), (200,50))
        self.screen_width = pygame.display.get_surface().get_width()
        self.lives_xy = (self.screen_width, 20)
        self.bg = bg
        self.updated_level = 0
        self.finished = False
        self.ball_image = pygame.image.load('data/ball.jpg').convert()
        self.ball_image.set_colorkey((0,0,0))
        
    def die(self):
        self.lives -= 1
        if self.lives == -1:
            self.game_over()
            
    def game_over(self, win=False):
        print 'GAME OVER'
        sys.exit(0)
        
    def update_score(self, points):
        self.prev = self.score
        self.score += points
       
        if self.score >= 120 and self.prev < 120:
            self.update_level(2)
        if self.score >= 330 and self.prev < 330:
            self.update_level(3)
        if self.score >= 630 and self.prev < 630:
            self.update_level(4)
        if self.score >= 1080 and self.prev < 1080:
            self.update_level(5)          
        if self.score >= 1680 and self.prev < 1680:
            print 'LEVEL 6'
            self.update_level(6)
            self.win()
    
    def update_level(self, level):
        self.level = level
        self.updated_level = level
        
    def win(self):
        pass
        
    def update(self):
        self.updated_level = 0
        screen = pygame.display.get_surface() 
    
        font = pygame.font.Font(DEF_FONT, 30)
                
        score = "Score: " + str(self.score)
        text = font.render(score, True, WHITE, BG)
        text.set_colorkey(BG)
        
        screen.blit(
        self.bg, 
        self.score_rect,
        self.score_rect)
        
        screen.blit(text, 
        self.score_rect)
        
        (x,y) = self.lives_xy
        life_rect = pygame.Rect(x,y, 12, 12)
        screen.blit(self.bg, life_rect, life_rect)
        
        for life in range(self.lives):
            x = (self.screen_width-100)+(life*20)
            screen.blit(self.ball_image, (x,y))
            self.lives_xy = (x,y)

        return [self.score_rect, life_rect]
