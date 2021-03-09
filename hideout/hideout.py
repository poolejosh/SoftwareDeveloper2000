import os
import pygame
from hideout.hideout_button import HideoutButton
from hideout.feature import Feature
from hideout.exploit import Exploit

WHITE = (255, 255, 255)

class Hideout(pygame.Rect):
    WIDTH, HEIGHT = 512, 512
    BACKGROUND_IMAGE = pygame.image.load(os.path.join("assets", "images", "ui", "background.png"))
    BACKGROUND_IMAGE_INACTIVE = pygame.image.load(os.path.join("assets", "images", "ui", "background_inactive.png"))
    PROGRESS_BAR_IMAGE = pygame.image.load(os.path.join("assets", "images", "ui", "progress_bar.png"))
    PROGRESS_FILL_IMAGE = pygame.image.load(os.path.join("assets", "images", "ui", "progress_fill.png"))
    
    def __init__(self, left, top, width=WIDTH, height=HEIGHT):
        pygame.Rect.__init__(self, left, top, width, height)
        self.background = pygame.transform.scale(self.BACKGROUND_IMAGE, (width, height))
        self.background_inactive = pygame.transform.scale(self.BACKGROUND_IMAGE_INACTIVE, (width, height))
        self.header_font = pygame.font.Font(os.path.join("assets", "fonts", "M_8pt.ttf"), 20)
        self.header = self.header_font.render("Hideout", False, WHITE)
        self.progress_font = pygame.font.Font(os.path.join("assets", "fonts", "M_8pt.ttf"), 14)
        self.progress_bar = pygame.transform.scale(self.PROGRESS_BAR_IMAGE, (406, 30))
        
        self.dollars = 0
        self.money_label = "Money: ${}".format(self.dollars)
        
        self.buttons = [
            HideoutButton(50, 250, label="Develop"),
            HideoutButton(260, 250, label="Next Feature"),
            HideoutButton(50, 350, label="Main Menu"),
            HideoutButton(260, 350, label="Exploits")
        ]

        self.users = 0
        self.user_rate = 0

        self.reputation = 0
        self.rep_rate = 0
        
        self.installed_features = []
        self.available_features = [
            (Feature("Domain Name", 0, 1, 1),  [Exploit("Malicious Misspellings", -1, 0), Exploit("DDOS", -1, -1)]),
            (Feature("Web Page", 10, 2, 2), [Exploit("XSS", 0, -1)]),
            (Feature("Database", 20, 1, 2), [Exploit("SQL Injection", 0, -2)])
        ]
        self.next_feature = self.available_features[0]
        self.available_exploits = []
        self.active_exploits = []

    def install_next_feature(self):
        if self.next_feature and self.next_feature[0].cost <= self.dollars:
            feature, exploits = self.available_features.pop(0)
            self.installed_features.append(feature)
            for exploit in exploits:
                self.available_exploits.append(exploit)
            
            self.change_money(-feature.cost)
            self.user_rate += feature.user_rate
            self.rep_rate += feature.rep_rate
            if len(self.available_features) > 0:
                self.next_feature = self.available_features[0]
            else:
                self.next_feature = None

            return True
        else:
            return False
    
    def activate_exploit(self, exploit):
        self.active_exploits.append(exploit)
        self.user_rate += exploit.user_rate
        self.rep_rate += exploit.rep_rate
        if self.user_rate < 0:
            self.user_rate = 0
        if self.rep_rate < 0:
            self.rep_rate = 0
        self.available_exploits.remove(exploit)

    def change_money(self, dollars):
        self.dollars += dollars
        self.money_label = "Money: ${}".format(self.dollars)
