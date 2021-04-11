import pygame
import os
import random
from common import logger
from other.text_wrap import drawText

from main_menu.main_menu import MainMenu
from hideout.hideout import Hideout
from other.popup import PopUp
from check_vuln import check

WIDTH, HEIGHT = 512, 512
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vulnerability Finder")

MAIN_MENU = "MAIN_MENU"
HIDEOUT = "HIDEOUT"
DEVELOP = "DEVELOP"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)

FPS = 60

PLAYER_WIDTH, PLAYER_HEIGHT = 64, 64

# method for drawing main menu
def draw_main_menu(main_menu, popup):
    # if theres a popup show inactive background
    if popup:
        WIN.blit(main_menu.background_inactive, main_menu)
    else:
        WIN.blit(main_menu.background, main_menu)
    
    # draw header
    header_rect = main_menu.header.get_rect()
    header_rect.centerx = main_menu.centerx
    header_rect.y = 12
    WIN.blit(main_menu.header, header_rect)
    
    # draw buttons
    for button in main_menu.buttons:
        WIN.blit(button.display, button)
        label_rect = button.label.get_rect()
        label_rect.center = button.center
        WIN.blit(button.label, label_rect)

    # draw popup
    if popup:
        WIN.blit(popup.background, popup)
        header_rect = popup.header.get_rect()
        header_rect.centerx = popup.centerx
        header_rect.y = popup.y + 12
        WIN.blit(popup.header, header_rect)
        WIN.blit(popup.close_button.display, popup.close_button)
        close_button_label_rect = popup.close_button.label.get_rect()
        close_button_label_rect.center = popup.close_button.center
        WIN.blit(popup.close_button.label, close_button_label_rect)
        drawText(WIN, popup.body_text, BLACK, popup.body_rect, popup.body_font)

    pygame.display.update()

# method for drawing hideout
def draw_hideout(hideout, result):
    # if theres a popup show inactive background
    WIN.blit(hideout.background, hideout)
    
    # draw header
    header_rect = hideout.header.get_rect()
    header_rect.centerx = hideout.centerx
    header_rect.y = 12
    WIN.blit(hideout.header, header_rect)

    
    if not result:
        drawText(WIN, hideout.body_text, BLACK, hideout.body_rect, hideout.body_font)
    else:
        message = hideout.body_font.render("Vulnerability fixed!", False, BLACK)
        message_rect = pygame.Rect(hideout.x + 15, hideout.y + 60, hideout.width, hideout.height / 2)
        WIN.blit(message, message_rect)


    pygame.display.update()

def main():
    logger.debug("Game is Running!")
    # initialize main game objects
    main_menu = MainMenu(0, 0)
    hideout = Hideout(0, 0)
    popup = None

    # create clock for fps timing
    clock = pygame.time.Clock()
    
    # make required pygame initializations
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join("assets", "music", "Ludum Dare 32 - Track 4.wav"))
    pygame.mixer.music.set_volume(0.03)
    pygame.mixer.music.play(-1)
    run = True
    tick = 0
    mode = MAIN_MENU # current game mode
    while run:
        clock.tick(FPS) # limit game loop to 60 FPS 

        if mode == MAIN_MENU:
            for event in pygame.event.get():

                # if player closes window, quit
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_button = pygame.mouse.get_pressed()
                    if mouse_button[0]:
                        mouse_pos = pygame.mouse.get_pos()

                        # if player click play game, go to hideout
                        if main_menu.buttons[0].mouse_on_button(mouse_pos) and not popup:
                            mode = HIDEOUT
                            pygame.mixer.music.load(os.path.join("assets", "music", "Ludum Dare 32 - Track 3.wav"))
                            pygame.mixer.music.play(-1)

                        # if player clicks how to play, show how to play popup
                        elif main_menu.buttons[1].mouse_on_button(mouse_pos) and not popup:
                            popup = PopUp(64, 64, "How To Play", "how_to_play.txt")
                        
                        # close popup if close button is clicked
                        elif popup and popup.close_button.mouse_on_button(mouse_pos):
                                popup = None

            draw_main_menu(main_menu, popup)

        elif mode == HIDEOUT:
            for event in pygame.event.get():
                
                # if player closes window, quit
                if event.type == pygame.QUIT:
                    run = False

            result = check()
            
            draw_hideout(hideout, result)

    
    pygame.quit()

if __name__ == "__main__":
    main()
