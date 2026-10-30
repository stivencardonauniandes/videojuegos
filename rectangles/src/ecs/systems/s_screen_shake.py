import random

import esper

from src.ecs.components.c_screen_shake import CScreenShake

def system_screen_shake(delta_time:float):
    c_sh:CScreenShake
    for _, c_sh in esper.get_component(CScreenShake):
        if c_sh.time > 0:
            c_sh.time = max(0.0, c_sh.time - delta_time)
            c_sh.offset.update(random.uniform(-c_sh.magnitude, c_sh.magnitude),
                               random.uniform(-c_sh.magnitude, c_sh.magnitude))
        else:
            c_sh.offset.update(0, 0)
