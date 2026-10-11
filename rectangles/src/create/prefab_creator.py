
import random

import esper
import pygame

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity

def create_square(size:pygame.Vector2,
                    pos:pygame.Vector2, vel:pygame.Vector2, col:pygame.Color):
    cuad_entity = esper.create_entity()
    esper.add_component(cuad_entity,
                CSurface(size, col))
    esper.add_component(cuad_entity,
                CTransform(pos))
    esper.add_component(cuad_entity, 
                CVelocity(vel))

def create_enemy_square(enemy_info:dict, pos:dict):
    size = pygame.Vector2(enemy_info["size"]["x"], enemy_info["size"]["y"])
    col = pygame.Color(enemy_info["color"]["r"],
                       enemy_info["color"]["g"],
                       enemy_info["color"]["b"])
    speed = random.uniform(enemy_info["velocity_min"],
                           enemy_info["velocity_max"])
    vel = pygame.Vector2(speed, 0).rotate(random.uniform(0, 360))
    create_square(size, pygame.Vector2(pos["x"], pos["y"]), vel, col)

def create_enemy_spawner(level_data:dict):
    spawner_entity = esper.create_entity()
    esper.add_component(spawner_entity, CEnemySpawner(level_data))
