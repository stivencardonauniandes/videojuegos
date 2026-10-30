
import random

import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_hunter_state import CHunterState
from src.ecs.components.c_cooldown_text import CCooldownText
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_screen_shake import CScreenShake
from src.ecs.components.c_special_attack import CSpecialAttack
from src.ecs.components.c_tag_pause_text import CTagPauseText
from src.ecs.components.c_tag_ui import CTagUI
from src.ecs.components.c_spawn_point import CSpawnPoint
from src.ecs.components.c_tag_bullet import CTagBullet
from src.ecs.components.c_tag_enemy import CTagEnemy
from src.ecs.components.c_tag_explosion import CTagExplosion
from src.ecs.components.c_tag_player import CTagPlayer
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator

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
    ServiceLocator.sounds_service.play(enemy_info["sound"])
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

def create_player_square(player_info:dict, player_lvl_info:dict,
                         special_info:dict):
    c_anim = CAnimation(player_info["animations"])
    c_surf = CSurface.from_texture(player_info["image"], c_anim.number_frames)
    pos = pygame.Vector2(player_lvl_info["position"]["x"],
                         player_lvl_info["position"]["y"])
    player_entity = create_sprite(c_surf, pos, pygame.Vector2(0, 0))
    esper.add_component(player_entity, c_anim)
    esper.add_component(player_entity, CSpawnPoint(pos))
    esper.add_component(player_entity, CTagPlayer())
    esper.add_component(player_entity, CSpecialAttack(special_info))
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
    ServiceLocator.sounds_service.play(bullet_info["sound"])
    return bullet_entity

def create_special_bullets(special_info:dict, player_pos:pygame.Vector2,
                           player_size:tuple):
    origin = player_pos + pygame.Vector2(player_size) / 2
    for angle in (45, 135, 225, 315):
        c_surf = CSurface.from_texture(special_info["image"])
        size = pygame.Vector2(c_surf.area.size)
        vel = pygame.Vector2(special_info["velocity"], 0).rotate(angle)
        bullet_entity = create_sprite(c_surf, origin - size / 2, vel)
        esper.add_component(bullet_entity, CTagBullet())
    ServiceLocator.sounds_service.play(special_info["sound"])

def create_explosion(explosion_info:dict, center:pygame.Vector2):
    c_anim = CAnimation(explosion_info["animations"])
    c_surf = CSurface.from_texture(explosion_info["image"], c_anim.number_frames)
    pos = center - pygame.Vector2(c_surf.area.size) / 2
    explosion_entity = create_sprite(c_surf, pos, pygame.Vector2(0, 0))
    esper.add_component(explosion_entity, c_anim)
    esper.add_component(explosion_entity, CTagExplosion())
    ServiceLocator.sounds_service.play(explosion_info["sound"])
    return explosion_entity

def create_input_player():
    inputs = {
        "PLAYER_LEFT": CInputCommand("PLAYER_LEFT", pygame.K_LEFT),
        "PLAYER_RIGHT": CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT),
        "PLAYER_UP": CInputCommand("PLAYER_UP", pygame.K_UP),
        "PLAYER_DOWN": CInputCommand("PLAYER_DOWN", pygame.K_DOWN),
        "PLAYER_FIRE": CInputCommand("PLAYER_FIRE", pygame.BUTTON_LEFT,
                                     is_mouse=True),
        "PLAYER_SPECIAL": CInputCommand("PLAYER_SPECIAL", pygame.K_SPACE),
        "PAUSE": CInputCommand("PAUSE", pygame.K_p),
    }
    for c_input in inputs.values():
        esper.add_component(esper.create_entity(), c_input)


def _create_text(interface_cfg:dict, text_cfg:dict, text:str=None):
    font = ServiceLocator.fonts_service.get(interface_cfg["font"],
                                            text_cfg["size"])
    color = text_cfg["color"]
    c_surf = CSurface.from_text(text or text_cfg["text"], font,
                                pygame.Color(color["r"], color["g"], color["b"]))
    pos = pygame.Vector2(text_cfg["position"]["x"], text_cfg["position"]["y"])
    # Los textos centrados usan x como centro; los demás como borde izquierdo
    entity = esper.create_entity()
    esper.add_component(entity, c_surf)
    esper.add_component(entity, CTransform(pos))
    esper.add_component(entity, CTagUI())
    return entity, c_surf

def _center_text(entity:int, c_surf:CSurface):
    c_t = esper.component_for_entity(entity, CTransform)
    c_t.pos.x -= c_surf.area.w / 2

def create_title_text(interface_cfg:dict):
    entity, c_surf = _create_text(interface_cfg, interface_cfg["title"])
    _center_text(entity, c_surf)

def create_instructions_text(interface_cfg:dict):
    entity, c_surf = _create_text(interface_cfg, interface_cfg["instructions"])
    _center_text(entity, c_surf)
    c_t = esper.component_for_entity(entity, CTransform)
    c_t.pos.y -= c_surf.area.h

def create_pause_text(interface_cfg:dict):
    entity, c_surf = _create_text(interface_cfg, interface_cfg["pause"])
    _center_text(entity, c_surf)
    c_t = esper.component_for_entity(entity, CTransform)
    c_t.pos.y -= c_surf.area.h / 2
    esper.add_component(entity, CTagPauseText())
    return entity

def create_cooldown_text(interface_cfg:dict):
    special = interface_cfg["special"]
    font = ServiceLocator.fonts_service.get(interface_cfg["font"],
                                            special["size"])
    entity, _ = _create_text(
        interface_cfg, {"size": special["size"], "color": special["color_ready"],
                        "position": special["position"]},
        special["text_ready"])
    esper.add_component(entity, CCooldownText(interface_cfg, font))

def create_screen_shake():
    esper.add_component(esper.create_entity(), CScreenShake())
