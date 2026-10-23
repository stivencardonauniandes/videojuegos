import esper
import pygame

from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_tag_bullet import CTagBullet
from src.ecs.components.c_tag_enemy import CTagEnemy
from src.ecs.components.c_transform import CTransform

def system_collision_bullet_enemy(explosion_cfg:dict):
    bullets = esper.get_components(CTransform, CSurface, CTagBullet)
    enemies = esper.get_components(CTransform, CSurface, CTagEnemy)

    for bullet_entity, (c_bt, c_bs, _) in bullets:
        bullet_rect = c_bs.get_rect(c_bt.pos)
        for enemy_entity, (c_et, c_es, _) in enemies:
            if not esper.entity_exists(enemy_entity):
                continue
            enemy_rect = c_es.get_rect(c_et.pos)
            if bullet_rect.colliderect(enemy_rect):
                create_explosion(explosion_cfg,
                                 pygame.Vector2(enemy_rect.center))
                esper.delete_entity(bullet_entity, immediate=True)
                esper.delete_entity(enemy_entity, immediate=True)
                break
