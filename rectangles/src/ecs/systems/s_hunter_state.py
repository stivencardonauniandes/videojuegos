import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_hunter_state import CHunterState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_tag_player import CTagPlayer
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity

def system_hunter_state(delta_time:float):
    players = esper.get_components(CTransform, CSurface, CTagPlayer)
    if not players:
        return
    _, (c_pt, c_ps, _) = players[0]
    player_center = pygame.Vector2(c_ps.get_rect(c_pt.pos).center)

    components = esper.get_components(CTransform, CVelocity, CSurface,
                                      CAnimation, CHunterState)
    c_t:CTransform
    c_v:CVelocity
    c_s:CSurface
    c_a:CAnimation
    c_h:CHunterState
    for _, (c_t, c_v, c_s, c_a, c_h) in components:
        center = pygame.Vector2(c_s.get_rect(c_t.pos).center)
        to_player = player_center - center
        to_origin = c_h.origin - c_t.pos

        if c_h.state == "IDLE":
            if to_player.length() <= c_h.distance_start_chase:
                c_h.state = "CHASE"
        elif c_h.state == "CHASE":
            if to_origin.length() > c_h.distance_start_return:
                c_h.state = "RETURN"
        elif c_h.state == "RETURN":
            if to_origin.length() <= c_h.velocity_return * delta_time:
                c_t.pos.update(c_h.origin)
                c_h.state = "IDLE"

        if c_h.state == "CHASE" and to_player.length_squared() > 0:
            c_v.vel = to_player.normalize() * c_h.velocity_chase
        elif c_h.state == "RETURN":
            c_v.vel = to_origin.normalize() * c_h.velocity_return
        else:
            c_v.vel = pygame.Vector2(0, 0)

        c_a.set_animation("MOVE" if c_h.state != "IDLE" else "IDLE")
