import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_tag_enemy import CTagEnemy

def _bounce_axis(pos:float, vel:float, size:int, limit:int):
    """Devuelve (pos, vel) de un eje, evaluado de forma independiente."""
    if size >= limit:
        # No cabe en la pantalla: se centra y no rebota.
        return (limit - size) / 2, vel
    if pos < 0:
        return 0, abs(vel)
    if pos + size > limit:
        return limit - size, -abs(vel)
    return pos, vel

def system_screen_bounce(screen:pygame.Surface):
    screen_rect = screen.get_rect()
    components = esper.get_components(CTransform, CVelocity, CSurface, CTagEnemy)

    c_t:CTransform
    c_v:CVelocity
    c_s:CSurface
    for _, (c_t, c_v, c_s, _) in components:
        size = c_s.area.size
        c_t.pos.x, c_v.vel.x = _bounce_axis(c_t.pos.x, c_v.vel.x,
                                            size[0], screen_rect.width)
        c_t.pos.y, c_v.vel.y = _bounce_axis(c_t.pos.y, c_v.vel.y,
                                            size[1], screen_rect.height)
