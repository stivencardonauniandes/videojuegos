class CEnemySpawner:
    def __init__(self, level_data:dict) -> None:
        self.time = 0.0
        self.spawn_events = [
            {
                "time": event["time"],
                "enemy_type": event["enemy_type"],
                "position": event["position"],
                "triggered": False,
            }
            for event in level_data["enemy_spawn_events"]
        ]
