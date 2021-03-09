import pygame
from popup import PopUp
from hideout_button import HideoutButton

BLACK = (0, 0, 0)

class FeaturePopUp(PopUp):
    def __init__(self, left, top, header_text, body_file, next_feature):
        PopUp.__init__(self, left, top, header_text, body_file)
        self.body_text.format(next_feature.name, next_feature.cost)

        self.feature_name_label = "Next feature: {}".format(next_feature.name)
        self.feature_name_label_rect = pygame.Rect(self.x + 15, self.y + 60, self.width - 20, (self.height - 70)/2)
        self.feature_cost_label = "Cost: ${}".format(next_feature.cost)
        self.feature_cost_label_rect = pygame.Rect(self.x + 15, self.y + 120, self.width - 20, (self.height - 70)/2)

        self.install_button = HideoutButton(0, self.y + 250, "Install")
        self.install_button.centerx = self.centerx