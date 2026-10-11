
import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity

def system_movement(delta_time:float):
    components = esper.get_components(CTransform, CVelocity)

    c_t:CTransform
    c_v:CVelocity
    for _, (c_t, c_v) in components:
        c_t.pos.x += c_v.vel.x * delta_time
        c_t.pos.y += c_v.vel.y * delta_time