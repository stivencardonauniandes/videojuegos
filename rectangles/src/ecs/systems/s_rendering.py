
import esper
import pygame

from src.ecs.components.c_screen_shake import CScreenShake
from src.ecs.components.c_tag_ui import CTagUI
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface

def system_rendering(screen:pygame.Surface):
    shakes = esper.get_component(CScreenShake)
    offset = shakes[0][1].offset if shakes else pygame.Vector2(0, 0)
    components = esper.get_components(CTransform, CSurface)

    c_t:CTransform
    c_s:CSurface
    # La interfaz no tiembla con el efecto de pantalla
    for entity, (c_t, c_s) in components:
        pos = c_t.pos if esper.has_component(entity, CTagUI) else c_t.pos + offset
        screen.blit(c_s.surf, pos, c_s.area)
