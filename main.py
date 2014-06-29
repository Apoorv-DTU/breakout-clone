import os
import sys
import pygame
from pygame.locals import *
from consts import *
import menu
import breakout
from game import QuitException

def main():
    pygame.init()
    
    screen = pygame.display.set_mode(RES)
    pygame.display.set_caption('BreakOut')
    
    bg = pygame.Surface(screen.get_size()).convert()
    bg.fill(BG)
    
    x = screen.get_width()/2
    
    MenuInfo = {'colour1': ORANGE,
                'colour2': YELLOW,
                'caption': 'Breakout',
                'desc': 'A simple breakout clone.'
                }
   
    ButtonInfo = {'caption': "Play",
                  'rect': pygame.Rect(x-200,205, 100,30),
                  'color': ORANGE,
                  'bg': BUT_BG,
                  'OnUp': start,
                  'OnDown': None,
                  'OnHover': None}
    
    
    ButtonInfo2 = {'caption': "Exit",
                  'rect': pygame.Rect(x+100,205, 100,30),
                  'color': ORANGE,
                  'bg': BUT_BG,
                  'OnUp': quit,
                  'OnDown': None,
                  'OnHover': None}
    
    title = menu.ButtonMsg(screen, MenuInfo, ButtonInfo, ButtonInfo2)
    screen.blit(bg, (0,0))
    title.show()
    
    font_path = os.path.join('data', 'OpenSans-Light.ttf')
    
    x = screen.get_width()/2
    y = screen.get_height()-30
    
    clock = pygame.time.Clock()
    
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            else:
                title.handle_event(event)
        
        pygame.display.update()

def start():
    try:
        breakout.start()
    except QuitException as qe:
        if qe.value == 1:
            start()
        elif qe.value == 0:
            main()

def quit():
    sys.exit(0)
    
if __name__ == '__main__':
    main()
