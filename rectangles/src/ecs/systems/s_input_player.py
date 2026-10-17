import esper
import pygame

from src.ecs.components.c_input_command import CInputCommand

def system_input_player(event:pygame.event.Event, do_action:callable):
    components = esper.get_component(CInputCommand)

    c_input:CInputCommand
    for _, c_input in components:
        if c_input.is_mouse:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == c_input.key:
                c_input.phase = "START"
                c_input.mouse_pos = event.pos
                do_action(c_input)
        elif event.type == pygame.KEYDOWN and event.key == c_input.key:
            c_input.phase = "START"
            do_action(c_input)
        elif event.type == pygame.KEYUP and event.key == c_input.key:
            c_input.phase = "END"
            do_action(c_input)
