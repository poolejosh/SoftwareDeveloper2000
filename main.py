import pygame
import os
import random
from common import logger
from text_wrap import drawText

from main_menu import MainMenu
from hideout import Hideout
from develop import Develop
from popup import PopUp
from feature_popup import FeaturePopUp
from player import Player
from virus_enemy import VirusEnemy

WIDTH, HEIGHT = 512, 512
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Software Developer 2000")

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

def draw_main_menu(main_menu, popup):
    if popup:
        WIN.blit(main_menu.background_inactive, main_menu)
    else:
        WIN.blit(main_menu.background, main_menu)
    header_rect = main_menu.header.get_rect()
    header_rect.centerx = main_menu.centerx
    header_rect.y = 12
    WIN.blit(main_menu.header, header_rect)
    
    for button in main_menu.buttons:
        WIN.blit(button.display, button)
        label_rect = button.label.get_rect()
        label_rect.center = button.center
        WIN.blit(button.label, label_rect)

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

def draw_hideout(hideout, popup):
    if popup:
        WIN.blit(hideout.background_inactive, hideout)
    else:
        WIN.blit(hideout.background, hideout)
    header_rect = hideout.header.get_rect()
    header_rect.centerx = hideout.centerx
    header_rect.y = 12
    WIN.blit(hideout.header, header_rect)

    user_title = hideout.progress_font.render("Users:", False, BLACK)
    WIN.blit(user_title, (53, 60))
    WIN.blit(hideout.progress_bar, (53, 85))
    users_progress = pygame.transform.scale(hideout.PROGRESS_FILL_IMAGE, (hideout.users * 4, 24))
    WIN.blit(users_progress, (56, 88))

    user_title = hideout.progress_font.render("Reputation:", False, BLACK)
    WIN.blit(user_title, (53, 125))
    WIN.blit(hideout.progress_bar, (53, 150))
    rep_progress = pygame.transform.scale(hideout.PROGRESS_FILL_IMAGE, (hideout.reputation * 4, 24))
    WIN.blit(rep_progress, (56, 153))
    drawText(WIN, hideout.money_label, BLACK, pygame.Rect(53, 200, hideout.width, hideout.height), hideout.progress_font)

    for button in hideout.buttons:
        WIN.blit(button.display, button)
        label_rect = button.label.get_rect()
        label_rect.center = button.center
        WIN.blit(button.label, label_rect)
    
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

        if isinstance(popup, FeaturePopUp):
            drawText(WIN, popup.feature_name_label, BLACK, popup.feature_name_label_rect, popup.body_font)
            drawText(WIN, popup.feature_cost_label, BLACK, popup.feature_cost_label_rect, popup.body_font)
            WIN.blit(popup.install_button.display, popup.install_button)
            install_button_label_rect = popup.install_button.label.get_rect()
            install_button_label_rect.center = popup.install_button.center
            WIN.blit(popup.install_button.label, install_button_label_rect)

    pygame.display.update()

def draw_develop_level(player, enemies, develop):
    WIN.blit(develop.background, (0, 0))

    for enemy in enemies:
        WIN.blit(enemy.sprite, enemy)
        # pygame.draw.rect(WIN, MAGENTA, enemy.hitbox, 1) # draw enemy hitbox

    if player.doing_aoe_attack:
        WIN.blit(player.aoe_attack.frame, (player.aoe_attack.x, player.aoe_attack.y))
        # pygame.draw.rect(WIN, BLUE, player.aoe_attack.hitbox, 1) # draw aoe attack hitbox

    if player.facing_left:
        WIN.blit(player.sprite_l, (player.x, player.y))
    else:
        WIN.blit(player.sprite_r, (player.x, player.y))

    # pygame.draw.rect(WIN, RED, player.hitbox, 1) # draw player hitbox

    if player.doing_directed_attack:
        WIN.blit(player.directed_attack.frame, (player.directed_attack.x, player.directed_attack.y))
        # pygame.draw.rect(WIN, GREEN, player.directed_attack.hitbox, 1) # draw directed attack hitbox

    WIN.blit(develop.health_bar, (5, 485))
    player_health = pygame.transform.scale(develop.HEALTH_FILL_IMAGE, (player.health * 20, 14))
    WIN.blit(player_health, (10, 490))
    
    pygame.display.update()

def main():
    logger.debug("Game is Running!")
    main_menu = MainMenu(0, 0)
    hideout = Hideout(0, 0)
    develop = Develop(0, 0)
    popup = None
    player = Player(WIDTH/2 - PLAYER_WIDTH/2, HEIGHT/2 - PLAYER_HEIGHT/2, PLAYER_WIDTH, PLAYER_HEIGHT, False)
    enemies = []
    virus = VirusEnemy(400, 300)

    clock = pygame.time.Clock()
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join("music", "Ludum Dare 32 - Track 4.wav"))
    pygame.mixer.music.set_volume(0.01) # TODO: 0.1 when done
    pygame.mixer.music.play(-1)
    run = True
    tick = 0
    mode = MAIN_MENU # current game mode
    while run:
        clock.tick(FPS) # limit game loop to 60 FPS 

        if mode == MAIN_MENU:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_button = pygame.mouse.get_pressed()
                    if mouse_button[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        if main_menu.buttons[0].mouse_on_button(mouse_pos) and not popup:
                            mode = HIDEOUT
                            pygame.mixer.music.load(os.path.join("music", "Ludum Dare 32 - Track 3.wav"))
                            pygame.mixer.music.play(-1)

                        elif main_menu.buttons[1].mouse_on_button(mouse_pos) and not popup:
                            popup = PopUp(64, 64, "How To Play", "how_to_play.txt")
                        
                        elif popup and popup.close_button.mouse_on_button(mouse_pos):
                                popup = None

            draw_main_menu(main_menu, popup)

        elif mode == HIDEOUT:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_button = pygame.mouse.get_pressed()
                    if mouse_button[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        if hideout.buttons[0].mouse_on_button(mouse_pos) and not popup:
                            mode = DEVELOP
                            pygame.mixer.music.load(os.path.join("music", "Ludum Dare 32 - Track 1.wav"))
                            pygame.mixer.music.play(-1)
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
                            player = Player(WIDTH/2 - PLAYER_WIDTH/2, HEIGHT/2 - PLAYER_HEIGHT/2, PLAYER_WIDTH, PLAYER_HEIGHT, False)

                        elif hideout.buttons[1].mouse_on_button(mouse_pos) and not popup:
                            if hideout.next_feature:
                                popup = FeaturePopUp(64, 64, "Next Feature", "next_feature.txt", hideout.next_feature[0])

                        elif hideout.buttons[2].mouse_on_button(mouse_pos) and not popup:
                            mode = MAIN_MENU
                            pygame.mixer.music.load(os.path.join("music", "Ludum Dare 32 - Track 4.wav"))
                            pygame.mixer.music.play(-1)

                        elif hideout.buttons[3].mouse_on_button(mouse_pos) and not popup:
                            popup = PopUp(64, 64, "Active Exploits", "exploits.txt")
                            for exploit in hideout.active_exploits:
                                popup.body_text += exploit.name + "- user rate: {}, rep rate: {}".format(exploit.user_rate, exploit.rep_rate) +  ", "

                        elif popup:
                            if popup.close_button.mouse_on_button(mouse_pos):
                                popup = None
                            elif isinstance(popup, FeaturePopUp) and popup.install_button.mouse_on_button(mouse_pos):
                                if hideout.install_next_feature():
                                    popup = None

                    
            draw_hideout(hideout, popup)

        elif mode == DEVELOP:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_button = pygame.mouse.get_pressed()
                    if not player.doing_directed_attack and not player.doing_aoe_attack:
                        if mouse_button[0] and player.doing_directed_attack == False:
                            mouse_pos = pygame.mouse.get_pos()
                            direction = player.mouse_direction_relative_to_player(mouse_pos)
                            
                            if direction:
                                player.doing_directed_attack = True
                                player.directed_attack.direction = direction
                                player.directed_attack.starting_tick = tick
                                pygame.mixer.Sound.play(player.directed_attack_sound)
                        
                        elif mouse_button[2] and player.doing_aoe_attack == False:
                            player.doing_aoe_attack = True
                            player.aoe_attack.starting_tick = tick
                            pygame.mixer.Sound.play(player.aoe_attack_sound)

            keys_pressed = pygame.key.get_pressed()
            player.handle_movement(keys_pressed)
            if (tick == 0):
                for enemy in enemies:
                    enemy.change_direction()
            
            for enemy in enemies:
                if enemy.invincible:
                    enemy.update_invincibility(tick)
            
            if player.invincible:
                player.update_invincibility(tick)

            if player.doing_directed_attack:
                player.resolve_directed_attack(tick)
                for enemy in enemies:
                    if player.directed_attack.hitbox.colliderect(enemy.hitbox):
                        if not enemy.invincible:
                            pygame.mixer.Sound.play(enemy.damaged_sound)
                            if enemy.inflict_damage(player.directed_attack.damage, tick):
                                enemy.direction = player.directed_attack.direction
                            else:
                                enemies.remove(enemy)

            elif player.doing_aoe_attack:
                player.resolve_aoe_attack(tick)
                for enemy in enemies:
                    if player.aoe_attack.hitbox.colliderect(enemy.hitbox):
                        if not enemy.invincible:
                            pygame.mixer.Sound.play(enemy.damaged_sound)
                            if enemy.inflict_damage(player.aoe_attack.damage, tick):
                                enemy.direction = enemy.direction_away_from_player(player)
                            else:
                                enemies.remove(enemy)
            
            for enemy in enemies:
                enemy.handle_movement()
                if enemy.hitbox.colliderect(player.hitbox):
                    if not player.invincible:
                        pygame.mixer.Sound.play(player.damaged_sound)
                        if not player.inflict_damage(enemy.damage, tick):
                            enemies = []
                            mode = HIDEOUT
                            pygame.mixer.music.load(os.path.join("music", "Ludum Dare 32 - Track 3.wav"))
                            pygame.mixer.music.play(-1)

            develop.set_background(tick)

            draw_develop_level(player, enemies, develop)

            if tick < 59:
                tick += 1
            else:
                tick = 0

            if len(enemies) == 0:
                if random.randint(0,4) == 0:
                    num_exploits = len(hideout.available_exploits)
                    if num_exploits > 0:
                        exploit = hideout.available_exploits[random.randint(0,num_exploits-1)]
                        hideout.activate_exploit(exploit)
                    else:
                        hideout.change_money(5)
                
                else:
                    hideout.change_money(5)

                mode = HIDEOUT
                pygame.mixer.music.load(os.path.join("music", "Ludum Dare 32 - Track 3.wav"))
                pygame.mixer.music.play(-1)
                hideout.users += hideout.user_rate
                hideout.reputation += hideout.rep_rate
                if hideout.users > 100:
                    hideout.users = 100
                if hideout.reputation > 100:
                    hideout.reputation = 100
                
                if hideout.users == 100 and hideout.reputation == 100:
                    popup = PopUp(64, 64, "You Win!", "win.txt")
    
    pygame.quit()

if __name__ == "__main__":
    main()
