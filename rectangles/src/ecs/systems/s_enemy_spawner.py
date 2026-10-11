import esper

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.create.prefab_creator import create_enemy_square

def system_enemy_spawner(enemies_cfg:dict, delta_time:float):
    components = esper.get_component(CEnemySpawner)

    c_spw:CEnemySpawner
    for _, c_spw in components:
        c_spw.time += delta_time
        for event in c_spw.spawn_events:
            if not event["triggered"] and c_spw.time >= event["time"]:
                event["triggered"] = True
                create_enemy_square(enemies_cfg[event["enemy_type"]],
                                    event["position"])
