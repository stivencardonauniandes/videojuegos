import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_tag_explosion import CTagExplosion

def system_explosion_end():
    components = esper.get_components(CAnimation, CTagExplosion)

    c_a:CAnimation
    for entity, (c_a, _) in components:
        if c_a.finished:
            esper.delete_entity(entity, immediate=True)
