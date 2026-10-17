import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_tag_bullet import CTagBullet
from src.ecs.components.c_transform import CTransform

def system_screen_bullet(screen:pygame.Surface):
    screen_rect = screen.get_rect()
    components = esper.get_components(CTransform, CSurface, CTagBullet)

    c_t:CTransform
    c_s:CSurface
    for entity, (c_t, c_s, _) in components:
        bullet_rect = c_s.surf.get_rect(topleft=c_t.pos)
        if not screen_rect.contains(bullet_rect):
            esper.delete_entity(entity, immediate=True)
