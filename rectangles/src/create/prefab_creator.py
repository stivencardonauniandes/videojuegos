
import random

import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_hunter_state import CHunterState
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_spawn_point import CSpawnPoint
from src.ecs.components.c_tag_bullet import CTagBullet
from src.ecs.components.c_tag_enemy import CTagEnemy
from src.ecs.components.c_tag_explosion import CTagExplosion
from src.ecs.components.c_tag_player import CTagPlayer
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity

def create_sprite(c_surf:CSurface, pos:pygame.Vector2, vel:pygame.Vector2):
    entity = esper.create_entity()
    esper.add_component(entity, c_surf)
    esper.add_component(entity, CTransform(pos))
    esper.add_component(entity, CVelocity(vel))
    return entity

def create_enemy_square(enemy_info:dict, pos:dict):
    position = pygame.Vector2(pos["x"], pos["y"])
    if "velocity_chase" in enemy_info:
        return create_hunter(enemy_info, position)
    c_surf = CSurface.from_texture(enemy_info["image"])
    speed = random.uniform(enemy_info["velocity_min"],
                           enemy_info["velocity_max"])
    vel = pygame.Vector2(speed, 0).rotate(random.uniform(0, 360))
    enemy_entity = create_sprite(c_surf, position, vel)
    esper.add_component(enemy_entity, CTagEnemy())
    return enemy_entity

def create_hunter(enemy_info:dict, pos:pygame.Vector2):
    c_anim = CAnimation(enemy_info["animations"])
    c_surf = CSurface.from_texture(enemy_info["image"], c_anim.number_frames)
    hunter_entity = create_sprite(c_surf, pos, pygame.Vector2(0, 0))
    esper.add_component(hunter_entity, c_anim)
    esper.add_component(hunter_entity, CHunterState(pos, enemy_info))
    esper.add_component(hunter_entity, CTagEnemy())
    return hunter_entity

def create_enemy_spawner(level_data:dict, enemies_cfg:dict):
    spawner_entity = esper.create_entity()
    esper.add_component(spawner_entity, CEnemySpawner(level_data, enemies_cfg))

def create_player_square(player_info:dict, player_lvl_info:dict):
    c_anim = CAnimation(player_info["animations"])
    c_surf = CSurface.from_texture(player_info["image"], c_anim.number_frames)
    pos = pygame.Vector2(player_lvl_info["position"]["x"],
                         player_lvl_info["position"]["y"])
    player_entity = create_sprite(c_surf, pos, pygame.Vector2(0, 0))
    esper.add_component(player_entity, c_anim)
    esper.add_component(player_entity, CSpawnPoint(pos))
    esper.add_component(player_entity, CTagPlayer())
    return player_entity

def create_bullet(bullet_info:dict, player_pos:pygame.Vector2,
                  player_size:tuple, target_pos:pygame.Vector2):
    c_surf = CSurface.from_texture(bullet_info["image"])
    size = pygame.Vector2(c_surf.area.size)
    origin = player_pos + pygame.Vector2(player_size) / 2
    direction = target_pos - origin
    if direction.length_squared() == 0:
        return None
    vel = direction.normalize() * bullet_info["velocity"]
    bullet_entity = create_sprite(c_surf, origin - size / 2, vel)
    esper.add_component(bullet_entity, CTagBullet())
    return bullet_entity

def create_explosion(explosion_info:dict, center:pygame.Vector2):
    c_anim = CAnimation(explosion_info["animations"])
    c_surf = CSurface.from_texture(explosion_info["image"], c_anim.number_frames)
    pos = center - pygame.Vector2(c_surf.area.size) / 2
    explosion_entity = create_sprite(c_surf, pos, pygame.Vector2(0, 0))
    esper.add_component(explosion_entity, c_anim)
    esper.add_component(explosion_entity, CTagExplosion())
    return explosion_entity

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
