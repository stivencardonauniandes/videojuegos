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
        player_rect = c_s.get_rect(c_t.pos)
        player_rect.clamp_ip(screen_rect)
        c_t.pos.x = player_rect.x
        c_t.pos.y = player_rect.y
