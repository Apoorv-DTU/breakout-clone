import os
import pygame
import game

class Brick(pygame.sprite.Sprite):
    def __init__(self, score, colour, xy, size=30, points=0):
        pygame.sprite.Sprite.__init__(self)
        xy = (xy[0], xy[1]+ 60)
        self.size = size
        self.score = score
        self.points = points
        self.rect = pygame.Rect(xy, (size, 30))
        self.colour = colour
        self.image = self.create_img(colour).convert()
        self.destroyed = False
        self.sound = self.load_sound('break.wav')
    
    def create_img(self, colour):
        img = pygame.Surface(self.rect.size)
        img.fill(colour)
        return img
        
    def destroy(self):
        if not self.destroyed:
            self.destroyed = True
            self.sound.play()
            self.kill()
            self.score.update_score(self.points)
            game.notify(str(self.points), self.rect, 25, self.colour)
            return True
        else:
            return False
        
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
  
