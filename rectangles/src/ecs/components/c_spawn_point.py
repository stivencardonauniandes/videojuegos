import pygame

class CSpawnPoint:
    def __init__(self, pos:pygame.Vector2) -> None:
        self.pos = pos.copy()
