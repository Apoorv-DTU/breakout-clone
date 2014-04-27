from random import randint
import threading
import pygame
from consts import *
import menu
import button

paused = False
finished = False
screen = None
PauseMenu = None
WinScreen = None
GameOverScreen = None
kill_notifs = False

class QuitException(Exception):
    def __init__(self, value):
        self.value = value

def get_quips():
    quips = ["You deserve it.",
             "You kinda suck at this.",
             "I have a small puppy that's better at this.",
             "Your let your cow down.",
             "Please DONT try again, its a shame to watch you play.",
             "You are not good at this. Are you ?"]
             
    return quips[randint(0,4)]

def exit_to_menu():
    raise QuitException(0)

def retry():
    raise QuitException(1)

def init():
    global PauseMenu
    global GameOverScreen
    global kill_notifs
    global WinScreen
    global finished
    
    kill_notifs = False
    finished = False
    
    screen = pygame.display.get_surface()
    x = screen.get_width()/2 
    
    MenuInfo = {'colour1': ORANGE,
                'colour2': LIGHT_ORANGE,
                'caption': "Paused",
                'desc': "Press Escape to resume"}
               
    ButtonInfo = {'caption': "Quit",
                  'rect': pygame.Rect(x-50,205, 100,30),
                  'color': ORANGE,
                  'bg': BUT_BG,
                  'OnUp': exit_to_menu,
                  'OnDown': None,
                  'OnHover': None}    
    
    PauseMenu = menu.ButtonMsg(screen, MenuInfo, ButtonInfo)
    
    MenuInfo['caption'] = "Game Over!"
    MenuInfo['desc'] = get_quips()
    MenuInfo['colour1'] = RED
    MenuInfo['colour2'] = LIGHT_RED
    
    ButtonInfo['rect'] = pygame.Rect(x-200,205, 100,30)
    ButtonInfo['color'] = RED
    
    b_retry = ButtonInfo.copy()
    
    b_retry['caption'] = "Retry"
    b_retry['OnUp'] = retry
    b_retry['rect'] = pygame.Rect(x+100,205, 100,30)
    
    GameOverScreen = menu.ButtonMsg(screen, MenuInfo, b_retry, ButtonInfo)

    MenuInfo['caption'] = "You Win!"
    MenuInfo['desc'] = "You made me proud."
    MenuInfo['colour1'] = BLUE
    MenuInfo['colour2'] = LIGHT_BLUE
    
    ButtonInfo['color'] = BLUE
    b_retry['color'] = BLUE
    
    WinScreen = menu.ButtonMsg(screen, MenuInfo, b_retry, ButtonInfo)

def pause(game_over=[False, False]):
    screen = pygame.display.get_surface()
    darkness = pygame.Surface(screen.get_size())
    darkness.fill((0,0,0))
    darkness.set_alpha(150)
    screen.blit(darkness, (0,0))
    paused = True
    global kill_notifs
    kill_notifs = True

    show_pause_menu()
    
def resume():

    screen = pygame.display.get_surface()
    pygame.mouse.set_visible(False)
    darkness = pygame.Surface(screen.get_size())
    darkness.fill((30,30,30))
    screen.blit(darkness, (0,0))
    global paused
    paused = False
    
    global kill_notifs
    kill_notifs = False

def show_pause_menu():
    global PauseMenu
    PauseMenu.show()      

def win_screen():
    global WinScreen
    global finished
    global kill_notifs
    
    if finished == False:
        kill_notifs = True
        finished = True
        WinScreen.show()
    
def handle_event(event):
    global GameOverScreen
    GameOverScreen.handle_event(event)
    
def handle_pause_event(event):
    global PauseMenu
    PauseMenu.handle_event(event)

def handle_win_event(event):
    global WinScreen
    WinScreen.handle_event(event)

def _notify(msg, rect, size, colour):
    
    global kill_notifs
    screen = pygame.display.get_surface()
    font = pygame.font.Font(DEF_FONT, size)
    text = font.render(msg, True, colour, BG).convert()
    text.set_colorkey(BG)
    if not rect:
        textpos = text.get_rect(centerx=screen.get_width()/2)
    else:
        textpos = rect

    bg = pygame.Surface(screen.get_size()).convert()
    bg.fill(BG)

    alpha = 300
    while alpha >= -1:
        if kill_notifs == False:
            
            screen.blit(bg, textpos, textpos)
            screen.blit(text, textpos)
            text.set_alpha(alpha)
            pygame.time.wait(10)
        else:
            pass
        alpha -= 1

def game_over_screen():
    global GameOverScreen
    global finished
    global kill_notifs
    if finished == False:
        kill_notifs = True
        finished = True
        GameOverScreen.show()
        
def notify(msg, rect=None, size=30, colour=WHITE):
    t1 = threading.Thread(target=_notify, args=(msg, rect, size, colour))
    t1.start()
    return t1
