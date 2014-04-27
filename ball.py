import os
from random import randint
import math
import pygame
from pygame.draw import *
from physics import *

class Ball(pygame.sprite.Sprite):
    def __init__(self, colour, speed, bat, bricks_group, score):
        #doing the neccesary
        pygame.sprite.Sprite.__init__(self)
        
        self.rect = pygame.Rect((295, 453), (12,12))
        self.image = self._create_image(colour).convert()
        self.sound = self.load_sound('bounce.wav')
        angles = [135, 45]
        #physics
        self.angle = angles[randint(0, 1)]
        self.increment_speed = 0
        self.vector = [self.angle, speed]
        self.dirty = []
        #print self.vector
        
        #importing scoreboard to die
        self.score = score
        
        #privates
        self.shot = False
        self.movepos = [0,0]
        self.bat = bat
        self.hit = False
        self.deflected = None
        
        #limits
        self.area = pygame.display.get_surface()
    
    #function to safely load sounds  
    def load_sound(self, file_):
        """returns the loaded sound or NoneSound() if mixer isnt initialized"""
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
  
    def _create_image(self, colour):
        img = pygame.image.load('data/ball.jpg').convert()
        img.set_colorkey((0,0,0))
        return img
        
    def update(self):        
        
        if not self.shot:
            self.rect.x = (self.bat.rect.x) + (self.bat.width/2)-12
        else:
            #set hit to false if bat isnt colliding with bat
            if not self.bat.rect.colliderect(self.rect):
                self.hit = False
                
            #refresh parameters
            newpos = self._calcnewpos()
            self.rect = newpos           

            #unpack vector
            (angle, z) = self.vector
            
            if self.increment_speed != 0:
                z += self.increment_speed
                self.speed = z
                self.increment_speed = 0
            
            #if angle exceeds the circular chart or goes in neg. direction,
            #adjust to so that it is positive and in the chart
            if angle > 360:
                print 'gotta cut', angle
                angle = angle - 360
            if angle < 0:
                angle = 360 - angle
            
            #check for deflection
            if self.deflected == 1.5:
            #sideway deflection
                quad = get_quadrant(angle)
                if quad is 1:
                    angle += 90
                elif quad is 2:
                    angle -= 90
                elif quad is 3:
                    angle += 90
                elif quad is 4:
                    angle -= 90
                    
            elif self.deflected == 2.5:
            #top and bottom deflection
                quad = get_quadrant(angle)
                if quad is 1:
                    angle += 270
                elif quad is 2:
                    angle += 90
                elif quad is 3:
                    angle -= 90
                else:
                    angle -= 270
                
            elif self.deflected == 1:
            #topleft corner deflection
                if get_quadrant(angle) is 4:
                    angle -= 90
                else:
                    angle += 90                
            else:
            #no collision
                angle = angle
                
            self.deflected = None
            #check for collision with area borders
            if not self.area.get_rect().contains(newpos):
                
                #sides are inverted due to function implementation          
                side = coll_side(self.area.get_rect(), newpos, True, True)
                
                if side and not self.hit_wall:
                    self.hit_wall = True
                    if side is 'top':
                        pass
                        if not self.score.finished:
                            self.reinit()
                    else:
                        self.sound.play()
                    
                    if side == 'left' or side == 'right':
                        quad = get_quadrant(angle)
                        if quad is 1:
                            angle += 90
                        elif quad is 2:
                            angle -= 90
                        elif quad is 3:
                            angle += 90
                        else:
                            angle -= 90
                    elif side == 'bottom':
                        quad = get_quadrant(angle)
                        if quad is 1:
                            angle += 270
                        elif quad is 2:
                            angle += 90
                        elif quad is 3:
                            angle -= 90
                        elif quad is 4:
                            angle -= 270
                    elif side == 'bottomright' or side == 'bottomleft':
                        angle += 180
                    elif side == 'topleft' or side == 'topright':
                        angle -= 180                         
            else:
                self.hit_wall = False
                angle = self._collide_bat(angle)
               
            self.vector = [angle, z]
            
    #a function to claculate the new position of the ball 
    def _calcnewpos(self):
        (angle,z) = self.vector
        
        dx = z*math.cos(math.radians(angle))
        if dx < 1 and dx > 0:
            dx = 1
        elif dx > -1 and dx < 0:
            dx = -1
        dy = z*math.sin(math.radians(angle))
        
        if dy < 1 and dy > 0:
            dy = 1
        elif dy > -1 and dy < 0:
            dy = -1    
        return self.rect.move(dx, -dy)
      
        
    def shoot(self):
        newpos = self._calcnewpos()
        self.rect = newpos
        self.shot = True
    
    def reinit(self):
        self.rect = pygame.Rect((295, 453), (12,12))
        self.vector[0] = self.angle
        print 'lives remaining:', self.score.lives
        self.shot = False
        
    def _collide_bat(self, angle):
        if not self.hit:
            side = coll_side(self.bat, self)
            if side:
                quad = get_quadrant(angle)
                self.hit = True
                self.bat.sound.play()
                if side == 'top' or side == 'bottom':
                    if quad == 3:
                        return angle - 90
                    elif quad == 4:
                        return angle - 270
                
                elif side == 'bottomleft' or side == 'bottomright':
                    return angle - 180
                elif side == 'left' or side == 'right':
                    return 180 + angle 
                elif side == 'topleft' or side == 'topright':
                	return 180 + angle
                else:
                    return angle
        return angle
               
                    
    def deflect(self, deflection):
        self.deflected = deflection
