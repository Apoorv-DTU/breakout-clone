import pygame
from pygame.locals import *
from consts import *

class Button(object):
    def __init__(self, surface, b_info):
    
        self.caption = b_info['caption']
        self.rect = b_info['rect']
        self.color = b_info['color']
        self.bg = b_info['bg']
        self.On_Down = b_info['OnDown']
        self.On_Up = b_info['OnUp']
        self.On_Hover = b_info['OnHover']
        
        self.surface = surface
        self.is_down = False
        
        font = pygame.font.Font(DEF_FONT, 20)
        self._text = font.render(self.caption, True, self.color, self.bg)
        self._text.set_colorkey(self.bg)
        self._text = self._text.convert()
        
        x = self.rect.x + self.rect.width/2
        y = self.rect.y + self.rect.height/2
        self._textpos = self._text.get_rect(centerx=x,centery=y)
        self._textpos_down = self._textpos.copy()
        self._textpos_down.x += 3
        self._textpos_down.y += 3
        
    def show(self):
        self.draw_normal()
        
    def draw_normal(self):
        button = pygame.Surface(self.rect.size)
        button.fill(self.bg)
        self.surface.blit(button, self.rect)
        self.surface.blit(self._text, self._textpos)
        pygame.draw.rect(self.surface, self.color, self.rect, 2)
        
    def draw_hover(self):
        button = pygame.Surface(self.rect.size)
        button.fill(self.bg)
        self.surface.blit(button, self.rect)
        self.surface.blit(self._text, self._textpos)
        pygame.draw.rect(self.surface, WHITE, self.rect, 2)
        
    def draw_down(self):
        button = pygame.Surface(self.rect.size)
        button.fill(self.bg)
        self.surface.blit(button, self.rect)
        self.surface.blit(self._text, self._textpos_down)
        pygame.draw.rect(self.surface, self.bg, self.rect, 2)
        points = [self.rect.bottomleft, self.rect.topleft, self.rect.topright]
        pygame.draw.lines(self.surface, BLACK, 0, points, 2)
        
    def handle_event(self, event=None):
        if event is None:
            self.is_down = False
            self.draw_normal()
        elif event.type == MOUSEBUTTONDOWN:
            self.is_down = True
            self.draw_down()
            if self.On_Down:
                self.On_Down()
            
        elif event.type == MOUSEBUTTONUP:
            self.is_down = False
            self.draw_normal()
            if self.On_Up:
                self.On_Up()
            
        elif event.type == MOUSEMOTION:
            if not self.rect.collidepoint(event.pos):
                self.draw_normal()
            elif not self.is_down and self.rect.collidepoint(event.pos):
                self.draw_hover()
                if self.On_Hover:
                    self.On_Hover()
