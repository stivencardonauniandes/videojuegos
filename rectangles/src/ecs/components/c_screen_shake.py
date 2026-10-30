import pygame

class CScreenShake:
    def __init__(self) -> None:
        self.time = 0.0
        self.magnitude = 0.0
        self.offset = pygame.Vector2(0, 0)
