import pygame
import os
import random
from common import logger
from other.text_wrap import drawText

from main_menu.main_menu import MainMenu
from hideout.hideout import Hideout
from develop.develop import Develop
from other.popup import PopUp
from hideout.feature_popup import FeaturePopUp
from player.player import Player
from enemies.virus_enemy import VirusEnemy

WIDTH, HEIGHT = 512, 512
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Web Developer 2000")

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
def draw_hideout(hideout, popup):
    # if theres a popup show inactive background
    if popup:
        WIN.blit(hideout.background_inactive, hideout)
    else:
        WIN.blit(hideout.background, hideout)
    
    # draw header
    header_rect = hideout.header.get_rect()
    header_rect.centerx = hideout.centerx
    header_rect.y = 12
    WIN.blit(hideout.header, header_rect)
    
    # draw users progress bar
    user_title = hideout.progress_font.render("Users:", False, BLACK)
    WIN.blit(user_title, (53, 60))
    WIN.blit(hideout.progress_bar, (53, 85))
    users_progress = pygame.transform.scale(hideout.PROGRESS_FILL_IMAGE, (hideout.users * 4, 24))
    WIN.blit(users_progress, (56, 88))

    # draw rep progress bar
    rep_title = hideout.progress_font.render("Reputation:", False, BLACK)
    WIN.blit(rep_title, (53, 125))
    WIN.blit(hideout.progress_bar, (53, 150))
    rep_progress = pygame.transform.scale(hideout.PROGRESS_FILL_IMAGE, (hideout.reputation * 4, 24))
    WIN.blit(rep_progress, (56, 153))

    # draw money amount
    drawText(WIN, hideout.money_label, BLACK, pygame.Rect(53, 200, hideout.width, hideout.height), hideout.progress_font)

    # draw buttons
    for button in hideout.buttons:
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

        # if its a feature popup draw class specific labels and button
        if isinstance(popup, FeaturePopUp):
            drawText(WIN, popup.feature_name_label, BLACK, popup.feature_name_label_rect, popup.body_font)
            drawText(WIN, popup.feature_cost_label, BLACK, popup.feature_cost_label_rect, popup.body_font)
            WIN.blit(popup.install_button.display, popup.install_button)
            install_button_label_rect = popup.install_button.label.get_rect()
            install_button_label_rect.center = popup.install_button.center
            WIN.blit(popup.install_button.label, install_button_label_rect)

    pygame.display.update()

# draw develop
def draw_develop_level(player, enemies, develop):
    # draw background
    WIN.blit(develop.background, (0, 0))

    # draw enemies
    for enemy in enemies:
        WIN.blit(enemy.sprite, enemy)
        # pygame.draw.rect(WIN, MAGENTA, enemy.hitbox, 1) # draw enemy hitbox

    # draw player's aoe attack
    if player.doing_aoe_attack:
        WIN.blit(player.aoe_attack.frame, (player.aoe_attack.x, player.aoe_attack.y))
        # pygame.draw.rect(WIN, BLUE, player.aoe_attack.hitbox, 1) # draw aoe attack hitbox

    # draw player depending on direction facing
    if player.facing_left:
        WIN.blit(player.sprite_l, (player.x, player.y))
    else:
        WIN.blit(player.sprite_r, (player.x, player.y))
    # pygame.draw.rect(WIN, RED, player.hitbox, 1) # draw player hitbox

    # draw player's directed attack
    if player.doing_directed_attack:
        WIN.blit(player.directed_attack.frame, (player.directed_attack.x, player.directed_attack.y))
        # pygame.draw.rect(WIN, GREEN, player.directed_attack.hitbox, 1) # draw directed attack hitbox

    # draw player health bar
    WIN.blit(develop.health_bar, (5, 485))
    player_health = pygame.transform.scale(develop.HEALTH_FILL_IMAGE, (player.health * 20, 14))
    WIN.blit(player_health, (10, 490))
    
    pygame.display.update()

def main():
    logger.debug("Game is Running!")
    # initialize main game objects
    main_menu = MainMenu(0, 0)
    hideout = Hideout(0, 0)
    develop = Develop(0, 0)
    popup = None
    player = Player(WIDTH/2 - PLAYER_WIDTH/2, HEIGHT/2 - PLAYER_HEIGHT/2, PLAYER_WIDTH, PLAYER_HEIGHT, False)
    enemies = []
    virus = VirusEnemy(400, 300)

    # create clock for fps timing
    clock = pygame.time.Clock()
    
    # make required pygame initializations
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join("assets", "music", "Ludum Dare 32 - Track 4.wav"))
    pygame.mixer.music.set_volume(0.05)
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
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_button = pygame.mouse.get_pressed()
                    if mouse_button[0]:
                        mouse_pos = pygame.mouse.get_pos()

                        # if player clicks develop, go to develop mode
                        if hideout.buttons[0].mouse_on_button(mouse_pos) and not popup:
                            mode = DEVELOP
                            pygame.mixer.music.load(os.path.join("assets", "music", "Ludum Dare 32 - Track 1.wav"))
                            pygame.mixer.music.play(-1)

                            # generate random amount of enemies in random positions
                            rand = random.randint(1, 5)
                            for i in range(rand):
                                side = random.randint(0,3)
                                if side == 0:
                                    enemies.append(VirusEnemy(i*100, 64))
                                elif side == 1:
                                    enemies.append(VirusEnemy(448, i*100))
                                elif side == 2:
                                    enemies.append(VirusEnemy(i*100, 448))
                                else:
                                    enemies.append(VirusEnemy(64, i*100))
                            
                            # reset player object
                            player = Player(WIDTH/2 - PLAYER_WIDTH/2, HEIGHT/2 - PLAYER_HEIGHT/2, PLAYER_WIDTH, PLAYER_HEIGHT, False)

                        # if player clicks next feature, show next available feature popup
                        elif hideout.buttons[1].mouse_on_button(mouse_pos) and not popup:
                            if hideout.next_feature:
                                popup = FeaturePopUp(64, 64, "Next Feature", "next_feature.txt", hideout.next_feature[0])

                        # if player clicks main menu, go back to main menu
                        elif hideout.buttons[2].mouse_on_button(mouse_pos) and not popup:
                            mode = MAIN_MENU
                            pygame.mixer.music.load(os.path.join("assets", "music", "Ludum Dare 32 - Track 4.wav"))
                            pygame.mixer.music.play(-1)

                        # if player clicks exploits, show active exploits
                        elif hideout.buttons[3].mouse_on_button(mouse_pos) and not popup:
                            popup = PopUp(64, 64, "Active Vulnerabilities", "exploits.txt")
                            for exploit in hideout.active_exploits:
                                popup.body_text += exploit.name + "- user rate: {}, rep rate: {}".format(exploit.user_rate, exploit.rep_rate) +  ", "

                        elif popup:
                            
                            # if player clicks close button, close popup
                            if popup.close_button.mouse_on_button(mouse_pos):
                                popup = None

                            # if player clicks install feature, try to install feature
                            elif isinstance(popup, FeaturePopUp) and popup.install_button.mouse_on_button(mouse_pos):
                                if hideout.install_next_feature():
                                    popup = None

            draw_hideout(hideout, popup)

        elif mode == DEVELOP:
            for event in pygame.event.get():

                # if player closes window, quit
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_button = pygame.mouse.get_pressed()

                    # check if player is already doing an attack
                    if not player.doing_directed_attack and not player.doing_aoe_attack:

                        # do directed attack
                        if mouse_button[0]:
                            mouse_pos = pygame.mouse.get_pos()
                            direction = player.mouse_direction_relative_to_player(mouse_pos)
                            
                            # if mouse is outisde of player, continue resolving directed attack
                            if direction:
                                player.doing_directed_attack = True
                                player.directed_attack.direction = direction
                                player.directed_attack.starting_tick = tick
                                pygame.mixer.Sound.play(player.directed_attack_sound)
                        
                        # do aoe attack
                        elif mouse_button[2]:
                            player.doing_aoe_attack = True
                            player.aoe_attack.starting_tick = tick
                            pygame.mixer.Sound.play(player.aoe_attack_sound)

            # handle player movement with keys
            keys_pressed = pygame.key.get_pressed()
            player.handle_movement(keys_pressed)

            # update enemy direction once a second
            if (tick == 0):
                for enemy in enemies:
                    enemy.change_direction()
            
            # update enemy invincibility status
            for enemy in enemies:
                if enemy.invincible:
                    enemy.update_invincibility(tick)
            
            # update player invincibility status
            if player.invincible:
                player.update_invincibility(tick)

            # resolve directed attack and inflict damage on enemies
            if player.doing_directed_attack:
                player.resolve_directed_attack(tick)
                for enemy in enemies:
                    if player.directed_attack.hitbox.colliderect(enemy.hitbox):
                        if not enemy.invincible:
                            if enemy.inflict_damage(player.directed_attack.damage, tick):
                                pygame.mixer.Sound.play(enemy.damaged_sound)
                                enemy.direction = player.directed_attack.direction
                            else:
                                pygame.mixer.Sound.play(enemy.dies_sound)
                                enemies.remove(enemy)

            # resolve aoe attack and inflict damage on enemies
            elif player.doing_aoe_attack:
                player.resolve_aoe_attack(tick)
                for enemy in enemies:
                    if player.aoe_attack.hitbox.colliderect(enemy.hitbox):
                        if not enemy.invincible:
                            if enemy.inflict_damage(player.aoe_attack.damage, tick):
                                pygame.mixer.Sound.play(enemy.damaged_sound)
                                enemy.direction = enemy.direction_away_from_player(player)
                            else:
                                pygame.mixer.Sound.play(enemy.dies_sound)
                                enemies.remove(enemy)
            
            # handle enemy movement and inflict damage on player if touching
            for enemy in enemies:
                enemy.handle_movement()
                if enemy.hitbox.colliderect(player.hitbox):
                    if not player.invincible:
                        pygame.mixer.Sound.play(player.damaged_sound)
                        if not player.inflict_damage(enemy.damage, tick):
                            enemies = []
                            mode = HIDEOUT
                            pygame.mixer.music.load(os.path.join("assets", "music", "Ludum Dare 32 - Track 3.wav"))
                            pygame.mixer.music.play(-1)

            # update moving background image
            develop.set_background(tick)

            draw_develop_level(player, enemies, develop)

            # update tick
            if tick < 59:
                tick += 1
            else:
                tick = 0

            # check for all enemies dead
            if len(enemies) == 0:

                # random change for exploit activated
                if random.randint(0,4) == 0:
                    num_exploits = len(hideout.available_exploits)
                    if num_exploits > 0:
                        exploit = hideout.available_exploits[random.randint(0,num_exploits-1)]
                        hideout.activate_exploit(exploit)
                    
                    # if no exploits available just add money
                    else:
                        hideout.change_money(5)
                
                # otherwise just add money
                else:
                    hideout.change_money(5)

                # go back to hideout
                mode = HIDEOUT
                pygame.mixer.music.load(os.path.join("assets", "music", "Ludum Dare 32 - Track 3.wav"))
                pygame.mixer.music.play(-1)

                # update num users and rep
                hideout.users += hideout.user_rate
                hideout.reputation += hideout.rep_rate
                if hideout.users > 100:
                    hideout.users = 100
                if hideout.reputation > 100:
                    hideout.reputation = 100
                
                # check for win
                if hideout.users == 100 and hideout.reputation == 100:
                    popup = PopUp(64, 64, "You Win!", "win.txt")
    
    pygame.quit()

if __name__ == "__main__":
    main()
