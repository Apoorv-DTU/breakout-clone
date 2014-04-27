from random import randint
import pygame

def rand_size():
    size = []
    for i in range(9):
        byte = randint(5, 50)
        size.append(byte)
        byte = 55 - byte
        size.append(byte)
    size.append(30)
    return size

def coll_side(obj1, obj2, is_obj1_rect=False, is_obj2_rect=False):
    if is_obj1_rect:
        rect1 = obj1
    else:
        rect1 = obj1.rect
    if is_obj2_rect:
        rect2 = obj2
    else:
        rect2 = obj2.rect
        
    if not rect1:
        raise AttributeError, "rect1 is None"
    if not rect2:
        raise AttributeError, "rect2 is None"
    tl = rect1.collidepoint(rect2.topleft)
    bl = rect1.collidepoint(rect2.bottomleft)
    tr = rect1.collidepoint(rect2.topright)
    br = rect1.collidepoint(rect2.bottomright)
    
    if tl and bl:
        side = 'left'
    elif tl and tr:
        side = 'top'
    elif br and tr:
        side = 'right'
    elif br and bl:
        side = 'bottom'
    elif tl:
        side = 'topleft'
    elif tr:
        side = 'topright'
    elif bl:
        side = 'bottomleft'
    elif br:
        side = 'bottomright'
    else:
        side = None
    return side
    
def get_quadrant(angle):
        
    while angle < 0:
        angle = 360 + angle
    
    while angle > 360:
        angle = angle - 360
   
    if angle <= 90 and angle >= 0:
        quad = 1
    elif angle <= 180 and angle > 90:
        quad = 2
    elif angle <= 270 and angle > 180:
        quad = 3
    elif angle <= 360 and angle > 270:
        quad = 4
    return quad
