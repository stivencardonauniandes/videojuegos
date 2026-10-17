import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_tag_bullet import CTagBullet
from src.ecs.components.c_tag_enemy import CTagEnemy
from src.ecs.components.c_transform import CTransform

def system_collision_bullet_enemy():
    bullets = esper.get_components(CTransform, CSurface, CTagBullet)
    enemies = esper.get_components(CTransform, CSurface, CTagEnemy)

    for bullet_entity, (c_bt, c_bs, _) in bullets:
        bullet_rect = c_bs.surf.get_rect(topleft=c_bt.pos)
        for enemy_entity, (c_et, c_es, _) in enemies:
            if not esper.entity_exists(enemy_entity):
                continue
            enemy_rect = c_es.surf.get_rect(topleft=c_et.pos)
            if bullet_rect.colliderect(enemy_rect):
                esper.delete_entity(bullet_entity, immediate=True)
                esper.delete_entity(enemy_entity, immediate=True)
                break
