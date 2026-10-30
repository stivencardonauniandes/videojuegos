import asyncio
import pygame
import esper

from src.create.prefab_creator import (create_bullet, create_cooldown_text,
                                       create_enemy_spawner,
                                       create_input_player,
                                       create_instructions_text,
                                       create_pause_text,
                                       create_player_square,
                                       create_screen_shake,
                                       create_special_bullets,
                                       create_title_text)
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_screen_shake import CScreenShake
from src.ecs.components.c_special_attack import CSpecialAttack
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_tag_pause_text import CTagPauseText
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
from src.ecs.systems.s_cooldown_text import system_cooldown_text
from src.ecs.systems.s_screen_shake import system_screen_shake
from src.ecs.systems.s_special_cooldown import system_special_cooldown
from src.engine.service_locator import ServiceLocator
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
        self.is_paused = False
        self._player_keys = {"PLAYER_LEFT": False, "PLAYER_RIGHT": False,
                             "PLAYER_UP": False, "PLAYER_DOWN": False}
        self.bg_color = pygame.Color(self.window_cfg["bg_color"]["r"],
                                     self.window_cfg["bg_color"]["g"],
                                     self.window_cfg["bg_color"]["b"])
        esper.switch_world("main")

        # Original framerate = 0
        # Original bg_color (0, 200, 128)

    def _load_config_files(self):
        configs = ServiceLocator.configs_service
        self.window_cfg = configs.get("assets/cfg/window.json")
        self.enemies_cfg = configs.get("assets/cfg/enemies.json")
        self.player_cfg = configs.get("assets/cfg/player.json")
        self.bullet_cfg = configs.get("assets/cfg/bullet.json")
        self.explosion_cfg = configs.get("assets/cfg/explosion.json")
        self.level_cfg = configs.get("assets/cfg/level_01.json")
        self.interface_cfg = configs.get("assets/cfg/interface.json")
        self.special_cfg = configs.get("assets/cfg/special.json")

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
            self.player_cfg, self.level_cfg["player_spawn"], self.special_cfg)
        create_input_player()
        create_title_text(self.interface_cfg)
        create_instructions_text(self.interface_cfg)
        create_cooldown_text(self.interface_cfg)
        create_screen_shake()
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
        # En pausa no se ejecutan los sistemas: nada se mueve ni colisiona
        if self.is_paused:
            return
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
        system_special_cooldown(self.delta_time)
        system_screen_shake(self.delta_time)
        system_cooldown_text()

    def _draw(self):
        self.screen.fill(self.bg_color)
        system_rendering(self.screen)
        pygame.display.flip()

    def _do_action(self, c_input:CInputCommand):
        if c_input.name == "PAUSE":
            if c_input.phase == "START":
                self._toggle_pause()
        elif c_input.name in self._player_keys:
            # Se guarda el estado de la tecla (no se acumula velocidad)
            self._player_keys[c_input.name] = c_input.phase == "START"
            self._update_player_velocity()
        elif self.is_paused:
            return
        elif c_input.name == "PLAYER_FIRE":
            self._fire_bullet(c_input.mouse_pos)
        elif c_input.name == "PLAYER_SPECIAL" and c_input.phase == "START":
            self._fire_special()

    def _toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            create_pause_text(self.interface_cfg)
        else:
            for entity, _ in esper.get_component(CTagPauseText):
                esper.delete_entity(entity, immediate=True)

    def _fire_special(self):
        c_sp = esper.component_for_entity(self._player_entity, CSpecialAttack)
        if not c_sp.ready:
            return
        c_sp.remaining = c_sp.cooldown
        c_t = esper.component_for_entity(self._player_entity, CTransform)
        c_s = esper.component_for_entity(self._player_entity, CSurface)
        create_special_bullets(self.special_cfg, c_t.pos, c_s.area.size)
        for _, c_sh in esper.get_component(CScreenShake):
            c_sh.time = self.special_cfg["shake_time"]
            c_sh.magnitude = self.special_cfg["shake_magnitude"]

    def _update_player_velocity(self):
        keys = self._player_keys
        direction = pygame.Vector2(
            keys["PLAYER_RIGHT"] - keys["PLAYER_LEFT"],
            keys["PLAYER_DOWN"] - keys["PLAYER_UP"])
        if direction.length_squared() > 0:
            # Normalizado: la diagonal no supera la velocidad configurada
            direction.normalize_ip()
        c_v = esper.component_for_entity(self._player_entity, CVelocity)
        c_v.vel = direction * self.player_cfg["input_velocity"]

    def _fire_bullet(self, mouse_pos:tuple):
        if len(esper.get_component(CTagBullet)) >= self.level_cfg["player_spawn"]["max_bullets"]:
            return
        c_t = esper.component_for_entity(self._player_entity, CTransform)
        c_s = esper.component_for_entity(self._player_entity, CSurface)
        create_bullet(self.bullet_cfg, c_t.pos, c_s.area.size,
                      pygame.Vector2(mouse_pos))

    def _clean(self):
        pygame.quit()

    
