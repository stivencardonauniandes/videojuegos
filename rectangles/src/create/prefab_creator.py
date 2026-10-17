
import random

import esper
import pygame

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_spawn_point import CSpawnPoint
from src.ecs.components.c_tag_bullet import CTagBullet
from src.ecs.components.c_tag_enemy import CTagEnemy
from src.ecs.components.c_tag_player import CTagPlayer
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
    return cuad_entity

def create_enemy_square(enemy_info:dict, pos:dict):
    size = pygame.Vector2(enemy_info["size"]["x"], enemy_info["size"]["y"])
    col = pygame.Color(enemy_info["color"]["r"],
                       enemy_info["color"]["g"],
                       enemy_info["color"]["b"])
    speed = random.uniform(enemy_info["velocity_min"],
                           enemy_info["velocity_max"])
    vel = pygame.Vector2(speed, 0).rotate(random.uniform(0, 360))
    enemy_entity = create_square(size, pygame.Vector2(pos["x"], pos["y"]),
                                 vel, col)
    esper.add_component(enemy_entity, CTagEnemy())

def create_enemy_spawner(level_data:dict, enemies_cfg:dict):
    spawner_entity = esper.create_entity()
    esper.add_component(spawner_entity, CEnemySpawner(level_data, enemies_cfg))


def create_player_square(player_info:dict, player_lvl_info:dict):
    size = pygame.Vector2(player_info["size"]["x"], player_info["size"]["y"])
    col = pygame.Color(player_info["color"]["r"],
                       player_info["color"]["g"],
                       player_info["color"]["b"])
    pos = pygame.Vector2(player_lvl_info["position"]["x"],
                         player_lvl_info["position"]["y"])
    player_entity = create_square(size, pos, pygame.Vector2(0, 0), col)
    esper.add_component(player_entity, CSpawnPoint(pos))
    esper.add_component(player_entity, CTagPlayer())
    return player_entity

def create_bullet(bullet_info:dict, player_pos:pygame.Vector2,
                  player_size:tuple, target_pos:pygame.Vector2):
    size = pygame.Vector2(bullet_info["size"]["x"], bullet_info["size"]["y"])
    col = pygame.Color(bullet_info["color"]["r"],
                       bullet_info["color"]["g"],
                       bullet_info["color"]["b"])
    origin = player_pos + pygame.Vector2(player_size) / 2
    direction = target_pos - origin
    if direction.length_squared() == 0:
        return None
    vel = direction.normalize() * bullet_info["velocity"]
    bullet_entity = create_square(size, origin - size / 2, vel, col)
    esper.add_component(bullet_entity, CTagBullet())
    return bullet_entity

def create_input_player():
    inputs = {
        "PLAYER_LEFT": CInputCommand("PLAYER_LEFT", pygame.K_LEFT),
        "PLAYER_RIGHT": CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT),
        "PLAYER_UP": CInputCommand("PLAYER_UP", pygame.K_UP),
        "PLAYER_DOWN": CInputCommand("PLAYER_DOWN", pygame.K_DOWN),
        "PLAYER_FIRE": CInputCommand("PLAYER_FIRE", pygame.BUTTON_LEFT,
                                     is_mouse=True),
    }
    for c_input in inputs.values():
        esper.add_component(esper.create_entity(), c_input)
