import esper

from src.ecs.components.c_special_attack import CSpecialAttack

def system_special_cooldown(delta_time:float):
    c_sp:CSpecialAttack
    for _, c_sp in esper.get_component(CSpecialAttack):
        c_sp.remaining = max(0.0, c_sp.remaining - delta_time)
