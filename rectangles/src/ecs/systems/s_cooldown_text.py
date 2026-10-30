import esper
import pygame

from src.ecs.components.c_cooldown_text import CCooldownText
from src.ecs.components.c_special_attack import CSpecialAttack
from src.ecs.components.c_surface import CSurface

def system_cooldown_text():
    specials = esper.get_component(CSpecialAttack)
    if not specials:
        return
    _, c_sp = specials[0]

    c_ct:CCooldownText
    c_s:CSurface
    for _, (c_ct, c_s) in esper.get_components(CCooldownText, CSurface):
        cfg = c_ct.cfg
        if c_sp.ready:
            text, color = cfg["text_ready"], cfg["color_ready"]
        else:
            text = cfg["text_charging"].format(c_sp.remaining)
            color = cfg["color_charging"]
        if text != c_ct.last_text:
            c_ct.last_text = text
            new = CSurface.from_text(
                text, c_ct.font,
                pygame.Color(color["r"], color["g"], color["b"]))
            c_s.surf = new.surf
            c_s.area = new.area
