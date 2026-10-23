import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface

def system_animation(delta_time:float):
    components = esper.get_components(CSurface, CAnimation)

    c_s:CSurface
    c_a:CAnimation
    for _, (c_s, c_a) in components:
        anim = c_a.animations[c_a.curr_anim_name]
        c_a.curr_anim_time += delta_time
        frames = anim.end - anim.start + 1
        step = int(c_a.curr_anim_time * anim.framerate)
        if step >= frames:
            c_a.finished = True
        c_a.curr_frame = anim.start + step % frames
        c_s.area.x = c_a.curr_frame * c_s.area.w
