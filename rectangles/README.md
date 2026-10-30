# Solo Aliens Pa' (SAP)

Rectángulos de colores que aparecen según un nivel y rebotan en la pantalla. El jugador se mueve con las flechas y dispara balas con el clic izquierdo hacia el ratón para destruir los rectángulos.
Hecho con Python, pygame-ce y esper (ECS).

## Itch.io

- https://s7iven.itch.io/solo-aliens-pa-sap?secret=QiBssJd7PqESDhLhMHd4IBcRq0

## Requisitos

- Python 3.14 (el proyecto usa un entorno virtual en `.venv/`)
- [uv](https://docs.astral.sh/uv/) (opcional, para crear el entorno)

## Instalación

Con `uv`:

```bash
uv venv --python 3.14
uv pip install -r requirements.txt
```

Sin `uv`:

```bash
python3.14 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Ejecución

Desde la raíz del proyecto (las rutas a `assets/cfg/` son relativas):

```bash
source .venv/bin/activate
python main.py
```

O sin activar el entorno:

```bash
.venv/bin/python main.py
```

Al cerrar la ventana el programa termina.

En WSL se necesita WSLg. Si falla el display, ejecuta `wsl --update` en PowerShell y luego `wsl --shutdown`.

## Configuración

Todo está en `assets/cfg/`:

- `window.json`: título, tamaño, color de fondo y framerate.
- `enemies.json`: tipos de rectángulo (tamaño, color, velocidad mínima y máxima).
- `level_01.json`: posición inicial del jugador (`player_spawn`), límite de balas (`max_bullets`) y eventos de aparición (tiempo, tipo de enemigo y posición).
- `player.json`: tamaño, color y velocidad de entrada (`input_velocity`) del jugador.
- `bullet.json`: imagen, sonido y velocidad (`velocity`) de la bala.
- `interface.json`: fuente, texto, color, tamaño y posición de los textos.
- `special.json`: ataque especial (sonido, imagen, velocidad, `cooldown` de 2.5 s y temblor de pantalla).

Todos los recursos (json, imágenes, sonidos, fuentes) se cargan con `ServiceLocator` (`src/engine/service_locator.py` y `src/engine/services/`).

## Controles

Flechas: mover. Clic izquierdo: disparar. Espacio: ataque especial (4 balas en diagonal, recarga 2.5 s, se ve en pantalla). P: pausar/reanudar.

Para probar otra configuración, reemplaza el contenido de estos archivos.

## Estructura

```
main.py                         Punto de entrada
src/engine/game_engine.py       Game loop y carga de configuración
src/create/prefab_creator.py    Creación de entidades
src/ecs/components/             CTransform, CVelocity, CSurface, CEnemySpawner, CInputCommand, CSpawnPoint, CTagPlayer/Bullet/Enemy
src/ecs/systems/                Movimiento, rebote, dibujado, spawner, input, límites de pantalla, colisiones
```
