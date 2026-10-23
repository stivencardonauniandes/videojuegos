import pygame

class CSurface:
    def __init__(self, surf:pygame.Surface, area:pygame.Rect = None) -> None:
        self.surf = surf
        # Porción de la textura que se dibuja (un cuadro del sprite)
        self.area = area.copy() if area else surf.get_rect()

    @classmethod
    def from_texture(cls, image_path:str, number_frames:int = 1):
        surf = pygame.image.load(image_path).convert_alpha()
        width = surf.get_width() // number_frames
        return cls(surf, pygame.Rect(0, 0, width, surf.get_height()))

    def get_rect(self, pos:pygame.Vector2) -> pygame.Rect:
        return pygame.Rect(pos.x, pos.y, self.area.w, self.area.h)
