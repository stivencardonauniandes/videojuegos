import esper

from src.ecs.components.c_spawn_point import CSpawnPoint
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_tag_enemy import CTagEnemy
from src.ecs.components.c_tag_player import CTagPlayer
from src.ecs.components.c_transform import CTransform

def system_collision_player_enemy():
    players = esper.get_components(CTransform, CSurface, CSpawnPoint, CTagPlayer)
    enemies = esper.get_components(CTransform, CSurface, CTagEnemy)

    c_pt:CTransform
    c_ps:CSurface
    c_sp:CSpawnPoint
    for _, (c_pt, c_ps, c_sp, _) in players:
        player_rect = c_ps.surf.get_rect(topleft=c_pt.pos)
        for enemy_entity, (c_et, c_es, _) in enemies:
            enemy_rect = c_es.surf.get_rect(topleft=c_et.pos)
            if player_rect.colliderect(enemy_rect):
                esper.delete_entity(enemy_entity, immediate=True)
                c_pt.pos.update(c_sp.pos)
                player_rect.topleft = c_pt.pos
