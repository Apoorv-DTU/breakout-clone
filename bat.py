import os
import pygame
from consts import *

class Bat(pygame.sprite.Sprite):
    def __init__(self, speed):
        pygame.sprite.Sprite.__init__(self)
        self.width = 150
        x = (pygame.display.get_surface().get_size()[0]/2) - (self.width/2) 
        self.rect = pygame.Rect((x,465), (self.width, 10))
        self.image = self.create_img().convert()
        self.speed = speed
        self.movepos = [0, 0]
        self.area = pygame.display.get_surface().get_rect()
        self.state = 'still'
        self.sound = self.load_sound('hit.wav')

    def moveleft(self, speed=None):
        if speed:
            self.movepos[0] -= speed
        else:
            self.movepos[0] -= self.speed
                
    def moveright(self, speed=None):
        if speed:
            self.movepos[0] += speed
        else:
            self.movepos[0] += self.speed
        
    def update(self):
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos 
        pygame.event.pump() 
                   
        
    def create_img(self):
        img = pygame.Surface(self.rect.size)
        img.fill(LIGHT_BLUE)
        return img
        
    def load_sound(self, file_):
        class NoneSound:
            def play(self): pass
        if not pygame.mixer:
            return NoneSound()
        try:    
            name = os.path.join('data',file_)
            sound = pygame.mixer.Sound(name)
        except pygame.error, msg:
            print 'Cannot load sound:', file_
            raise SystemExit, msg
        return sound
