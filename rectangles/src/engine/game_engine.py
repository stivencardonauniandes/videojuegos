import asyncio
import json
import pygame
import esper

from src.create.prefab_creator import (create_bullet, create_enemy_spawner,
                                       create_input_player,
                                       create_player_square)
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_tag_bullet import CTagBullet
from src.ecs.components.c_tag_player import CTagPlayer
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_explosion_end import system_explosion_end
from src.ecs.systems.s_hunter_state import system_hunter_state
from src.ecs.systems.s_player_animation import system_player_animation
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_screen_bullet import system_screen_bullet
from src.ecs.systems.s_screen_player import system_screen_player
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce

class GameEngine:
    def __init__(self) -> None:
        self._load_config_files()

        pygame.init()
        pygame.display.set_caption(self.window_cfg["title"])
        self.screen = pygame.display.set_mode(
            (self.window_cfg["size"]["w"], self.window_cfg["size"]["h"]), 
            pygame.SCALED)

        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_cfg["framerate"]
        self.delta_time = 0
        self.bg_color = pygame.Color(self.window_cfg["bg_color"]["r"],
                                     self.window_cfg["bg_color"]["g"],
                                     self.window_cfg["bg_color"]["b"])
        esper.switch_world("main")

        # Original framerate = 0
        # Original bg_color (0, 200, 128)

    def _load_config_files(self):
        with open("assets/cfg/window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open("assets/cfg/enemies.json", encoding="utf-8") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open("assets/cfg/player.json", encoding="utf-8") as player_file:
            self.player_cfg = json.load(player_file)
        with open("assets/cfg/bullet.json", encoding="utf-8") as bullet_file:
            self.bullet_cfg = json.load(bullet_file)
        with open("assets/cfg/explosion.json", encoding="utf-8") as explosion_file:
            self.explosion_cfg = json.load(explosion_file)
        with open("assets/cfg/level_01.json", encoding="utf-8") as level_file:
            self.level_cfg = json.load(level_file)

    async def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            await asyncio.sleep(0)
        self._clean()

    def _create(self):
        self._player_entity = create_player_square(
            self.player_cfg, self.level_cfg["player_spawn"])
        create_input_player()
        create_enemy_spawner(self.level_cfg, self.enemies_cfg)

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0
    
    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            system_input_player(event, self._do_action)

    def _update(self):
        system_enemy_spawner(self.delta_time)
        system_hunter_state(self.delta_time)
        system_movement(self.delta_time)
        system_screen_bounce(self.screen)
        system_screen_player(self.screen)
        system_screen_bullet(self.screen)
        system_collision_bullet_enemy(self.explosion_cfg)
        system_collision_player_enemy(self.explosion_cfg)
        system_player_animation()
        system_animation(self.delta_time)
        system_explosion_end()

    def _draw(self):
        self.screen.fill(self.bg_color)
        system_rendering(self.screen)
        pygame.display.flip()

    def _do_action(self, c_input:CInputCommand):
        c_v = esper.component_for_entity(self._player_entity, CVelocity)
        speed = self.player_cfg["input_velocity"]
        sign = 1 if c_input.phase == "START" else -1

        if c_input.name == "PLAYER_LEFT":
            c_v.vel.x -= speed * sign
        elif c_input.name == "PLAYER_RIGHT":
            c_v.vel.x += speed * sign
        elif c_input.name == "PLAYER_UP":
            c_v.vel.y -= speed * sign
        elif c_input.name == "PLAYER_DOWN":
            c_v.vel.y += speed * sign
        elif c_input.name == "PLAYER_FIRE":
            self._fire_bullet(c_input.mouse_pos)

    def _fire_bullet(self, mouse_pos:tuple):
        if len(esper.get_component(CTagBullet)) >= self.level_cfg["max_bullets"]:
            return
        c_t = esper.component_for_entity(self._player_entity, CTransform)
        c_s = esper.component_for_entity(self._player_entity, CSurface)
        create_bullet(self.bullet_cfg, c_t.pos, c_s.area.size,
                      pygame.Vector2(mouse_pos))

    def _clean(self):
        pygame.quit()

    
