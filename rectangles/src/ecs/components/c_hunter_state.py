import pygame

class CHunterState:
    def __init__(self, origin:pygame.Vector2, enemy_info:dict) -> None:
        self.state = "IDLE"
        self.origin = origin.copy()
        self.velocity_chase = enemy_info["velocity_chase"]
        self.velocity_return = enemy_info["velocity_return"]
        self.distance_start_chase = enemy_info["distance_start_chase"]
        self.distance_start_return = enemy_info["distance_start_return"]
