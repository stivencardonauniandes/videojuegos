import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_tag_player import CTagPlayer
from src.ecs.components.c_velocity import CVelocity

def system_player_animation():
    components = esper.get_components(CVelocity, CAnimation, CTagPlayer)

    c_v:CVelocity
    c_a:CAnimation
    for _, (c_v, c_a, _) in components:
        c_a.set_animation("MOVE" if c_v.vel.length_squared() > 0 else "IDLE")
