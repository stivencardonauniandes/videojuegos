import pygame

from src.engine.service_locator import ServiceLocator

class CSurface:
    def __init__(self, surf:pygame.Surface, area:pygame.Rect = None) -> None:
        self.surf = surf
        # Porción de la textura que se dibuja (un cuadro del sprite)
        self.area = area.copy() if area else surf.get_rect()

    @classmethod
    def from_texture(cls, image_path:str, number_frames:int = 1):
        surf = ServiceLocator.images_service.get(image_path)
        width = surf.get_width() // number_frames
        return cls(surf, pygame.Rect(0, 0, width, surf.get_height()))

    @classmethod
    def from_text(cls, text:str, font:pygame.font.Font, color:pygame.Color):
        return cls(font.render(text, False, color))

    def get_rect(self, pos:pygame.Vector2) -> pygame.Rect:
        return pygame.Rect(pos.x, pos.y, self.area.w, self.area.h)
