import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_tag_player import CTagPlayer
from src.ecs.components.c_transform import CTransform

def system_screen_player(screen:pygame.Surface):
    screen_rect = screen.get_rect()
    components = esper.get_components(CTransform, CSurface, CTagPlayer)

    c_t:CTransform
    c_s:CSurface
    for _, (c_t, c_s, _) in components:
        # Se mantienen las coordenadas decimales (sin pasar por pygame.Rect)
        c_t.pos.x = max(0, min(c_t.pos.x, screen_rect.w - c_s.area.w))
        c_t.pos.y = max(0, min(c_t.pos.y, screen_rect.h - c_s.area.h))
