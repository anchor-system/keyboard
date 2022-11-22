from typing import Tuple

import pygame

class Screen:
    def __init__(self, surface: pygame.Surface, fullscreen: bool, width: int, height: int):
        self.surface = surface
        self.fullscreen = fullscreen
        self.width = width
        self.height = height
        self.text_size = self.width // 20
        self.font = pygame.font.Font(None, self.text_size)

    def update_resolution(self, new_width: int, new_height) -> None:
        self.width = new_width
        self.height = new_height
        self.text_size = self.width // 20
        self.font = pygame.font.Font(None, self.text_size)

    def center_point(self, p: Tuple[int]):
        x, y = p[0], p[1]
        return x + self.width / 2, y + self.height / 2
