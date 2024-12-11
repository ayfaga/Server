from typing import Any
import pygame


class button:
    def __init__(self, x, y, w, h, text, image_path=None, hover_image_path=None, sound_path=None, text_color=None):
        self.x = x
        self.y = y
        self.w = w  # width
        self.h = h  # height
        self.text = text
        self.img = pygame.image.load(image_path)
        self.img = pygame.transform.scale(self.img, (w, h))
        self.hover_image = self.img
        if hover_image_path:
            self.hover_image = pygame.image.load(hover_image_path)
            self.hover_image = pygame.transform.scale(self.hover_image, (w, h))
        self.rect = self.img.get_rect(topleft=(x, y))
        self.sound = None
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)
        self.is_hovered = False
        self.text_color = text_color

    def set_pos(self, x, y=None):
        self.x = x
        self.rect = self.img.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        current_img = self.hover_image if self.is_hovered else self.img
        screen.blit(current_img, self.rect.topleft)

        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(
                pygame.USEREVENT, button=self))

# a = button(20, 20, 250, 500, "PRESS ME", image_path="C:\Users\lookh\OneDrive\Deckstop\python\Ace_of_Hearts.png")
