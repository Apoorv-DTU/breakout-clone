import pygame
from pygame.locals import *
import button
from consts import *

class MessageBox(object):
    def __init__(self, surface, MenuInfo):
    
        self.surface = surface
        self.colour = MenuInfo['colour1']
        self.light_colour = MenuInfo['colour2']
        self.caption = MenuInfo['caption']
        self.desc = MenuInfo['desc']
        self._subtext = None
        self._subtextpos = None
        self._bright_border = None
        self._light_border = None
        self._bg = None
        self._text = None
        self._textpos = None
        
        self._create_menu()
        
    def _create_menu(self):
        self._bg = pygame.Surface((self.surface.get_width(), 110))
        self._bg.fill((16, 16, 16))
    	self._bg = self._bg.convert() 
    	 
        self._bright_border = pygame.Surface((self.surface.get_width(), 10))
        self._bright_border.fill(self.colour)
        self._bright_border = self._bright_border.convert()
	
        self._light_border = pygame.Surface((self._bright_border.get_size()))
        self._light_border.fill(self.light_colour)
        self._light_border = self._light_border.convert()
    
        if pygame.font:
        
            font = pygame.font.Font(DEF_FONT, 45)
            self._text = font.render(self.caption, True, self.colour, PAUSE_BG)
            self._text.set_colorkey(PAUSE_BG)
            self._text = self._text.convert()
            x = self.surface.get_width()/2
            self._textpos = self._text.get_rect(centerx=x, y=120)
            
            font = pygame.font.Font(DEF_FONT, 15)
            self._subtext = font.render(self.desc, True, WHITE, PAUSE_BG)
            self._subtext.set_colorkey(PAUSE_BG)
            self._subtext = self._subtext.convert()
            self._subtextpos = self._subtext.get_rect(centerx=x, y=175)
            
    def show(self):
        for x in range(3):
            self.surface.blit(self._bg, (0,100))
            self.surface.blit(self._bright_border, (0, 100))
            self.surface.blit(self._light_border, (0,110))
            self.surface.blit(self._light_border, (0, 210))
            self.surface.blit(self._bright_border, (0, 220))
            self.surface.blit(self._text, self._textpos)
            self.surface.blit(self._subtext, self._subtextpos)
            pygame.display.flip()
            
class ButtonMsg(MessageBox):
    def __init__(self, surface, MenuInfo, B1_Info, B2_Info=None):
        super(ButtonMsg,self).__init__(surface, MenuInfo)
        
        self.b1_info = B1_Info
        self.b2_info = B2_Info
       
        self.b1_rect = B1_Info['rect']
        if B2_Info:
            self.b2_rect = B2_Info['rect']
       
        self.b1 = None
        self.b2 = None
        
        self.initialize()
        
    def initialize(self):
        self.b1 = button.Button(self.surface, self.b1_info)
                           
        if self.b2_info:
            self.b2 = button.Button(self.surface, self.b2_info)
                           
    def show(self):
        super(ButtonMsg, self).show()
        
        self.b1.show()
        if self.b2:
            self.b2.show()
                           
    def handle_event(self, event):
        if event.type not in [MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP]:
            return
        elif self.b1_rect.collidepoint(event.pos):
            if self.b2:
                self.b2.handle_event()
            self.b1.handle_event(event)
        elif self.b2:
            if self.b2_rect.collidepoint(event.pos):
                self.b1.handle_event()
                self.b2.handle_event(event)
        else:
            self.b1.handle_event()
            if self.b2:
                self.b2.handle_event()
