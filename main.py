# -*- coding: ascii -*-
from pygame import Rect
import random

WIDTH, HEIGHT, STATE = 800, 600, "menu"
GRAVITY, GROUND_LEVEL = 0.5, 500
MAX_ENEMIES_ON_SCREEN, WORLD_DISTANCE_TO_WIN = 7, 8000
try:
    music.play("music_fundo"); music.set_volume(0.2)
except:
    print("Arquivo de musica nao encontrado.")
sons_ligados = True
world_progress, enemies_killed = 0, 0
class Enemy(Actor):
    def __init__(self, image, pos):
        super().__init__(image, pos=pos, anchor=('center', 'bottom'))
        self.animation_speed = 15; self.animation_timer = 0; self.current_frame = 0; self.animation_frames = []
    def animate(self):
        if not self.animation_frames: return
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0; self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.current_frame]
class FixedObstacle(Enemy):
    def __init__(self, frames, pos):
        super().__init__(frames[0], pos); self.animation_frames = frames
    def update(self): self.animate()
class MovingEnemy(Enemy):
    def __init__(self, frames, pos, direction):
        super().__init__(frames[0], pos); self.animation_frames = frames
        self.move_speed = random.uniform(1.5, 3.0); self.direction = direction
    def update(self):
        self.animate(); self.x += self.move_speed * self.direction
        if self.right < -50 or self.left > WIDTH + 50:
            if self in enemies: enemies.remove(self)
class Bomb(Actor):
    def __init__(self, pos, direction=1):
        super().__init__('bomba', pos=pos, anchor=('center', 'bottom'))
        self.velocity_y = -5; self.velocity_x = 8 * direction; self.exploded = False; self.timer = 0
    def update(self):
        if not self.exploded:
            self.velocity_y += GRAVITY; self.y += self.velocity_y; self.x += self.velocity_x
            if self.bottom >= GROUND_LEVEL: self.bottom = GROUND_LEVEL; self.explode()
        else:
            self.timer += 1
            if self.timer > 30:
                if self in bombs: bombs.remove(self)
    def explode(self): self.image = 'bomba1'; self.exploded = True; self.timer = 0
class Hero(Actor):
    def __init__(self, **kwargs):
        super().__init__('frente', **kwargs)
        self.velocity_x=0; self.velocity_y=0; self.on_ground=True; self.can_double_jump=False
        self.idle_images=['frente','frente2']; self.idle_animation_speed=15 # Velocidade da animacao parado
        self.idle_frame=0; self.idle_timer=0; self.jump_strength=-10.5
        self.double_jump_strength=-8.5; self.move_speed=5; self.friction=0.8
        self.lives=3; self.invincible_timer=0; self.facing_direction=1
    def update(self):
        if self.invincible_timer > 0:
            self.invincible_timer -= 1; self.visible = self.invincible_timer % 10 < 5
        else: self.visible = True
        self._handle_input(); self._apply_gravity(); self._update_position()
        self._check_ground_collision(); self._update_animation()
    def _apply_gravity(self): self.velocity_y += GRAVITY
    def _update_position(self): self.y += self.velocity_y; self.x += self.velocity_x
    def _check_ground_collision(self):
        if self.bottom >= GROUND_LEVEL:
            self.bottom = GROUND_LEVEL; self.velocity_y = 0
            if not self.on_ground: self.on_ground = True; self.can_double_jump = False
    def _update_animation(self):
        if not self.on_ground:
            if self.velocity_x < -0.1: self.image = 'costas'
            elif self.velocity_y > 1: self.image = 'queda'
        else:
            self.idle_timer += 1
            if self.idle_timer >= self.idle_animation_speed:
                self.idle_timer=0; self.idle_frame=(self.idle_frame + 1)%len(self.idle_images)
                self.image = self.idle_images[self.idle_frame]
    def _handle_input(self):
        if keyboard.right: self.velocity_x=self.move_speed; self.facing_direction=1
        elif keyboard.left: self.velocity_x=-self.move_speed; self.facing_direction=-1
        else: self.velocity_x *= self.friction
    def jump(self):
        if self.on_ground:
            if sons_ligados: sounds.jump.play()
            self.velocity_y=self.jump_strength; self.on_ground=False; self.can_double_jump=True; self.image='pulo1'
    def double_jump(self):
        if self.can_double_jump:
            if sons_ligados: sounds.jump2.play()
            self.velocity_y=self.double_jump_strength; self.can_double_jump=False; self.image='pulo2'
    def lose_life(self):
        global STATE
        if self.invincible_timer == 0:
            if sons_ligados: sounds.bat.play()
            self.lives-=1; self.invincible_timer=120
            if self.lives < 0: STATE="game_over"
            else: life_icons[self.lives].image='vida0'; self.pos=(WIDTH//2,GROUND_LEVEL)

hero = Hero(pos=(100, GROUND_LEVEL), anchor=('center', 'bottom'))
bombs, enemies, life_icons = [], [], []
victory_flag = Actor('vitoria', pos=(-1000, GROUND_LEVEL), anchor=('center', 'bottom'))
ENEMY_DATA = {
    'joaninha': (['joaninha', 'joaninha2', 'joaninha3', 'joaninha4'], -50),
    'rato': (['rato', 'rato2', 'rato3'], 0),
    'sapo': (['sapo', 'sapo2', 'sapo3'], 0)
}

def reset_game():
    global STATE, enemies, life_icons, bombs, world_progress, enemies_killed
    hero.lives = 3; hero.pos = (100, GROUND_LEVEL); hero.invincible_timer = 0; hero.facing_direction = 1
    bombs, enemies, enemies_killed, world_progress = [], [], 0, 0
    life_icons = [Actor('vida', pos=(WIDTH-40-(i*80), 40)) for i in range(hero.lives)]
    victory_flag.pos = (WORLD_DISTANCE_TO_WIN - 200, GROUND_LEVEL)
    enemies = [FixedObstacle(['espinho', 'espinho2'], pos=(600, GROUND_LEVEL)),
               FixedObstacle(['parado1', 'parado2'], pos=(1000, GROUND_LEVEL))]
    STATE = "jogo"

def spawn_new_enemy():
    if len(enemies) >= MAX_ENEMIES_ON_SCREEN: return
    enemy_type = random.choice(list(ENEMY_DATA.keys()))
    frames, y_offset = ENEMY_DATA[enemy_type]
    x_pos, direction = WIDTH + 50, -1
    enemies.append(MovingEnemy(frames, pos=(x_pos, GROUND_LEVEL + y_offset), direction=direction))

def draw():
    screen.clear()
    if STATE == "menu": draw_menu()
    elif STATE == "jogo": draw_jogo()
    elif STATE == "pause": draw_pause()
    elif STATE == "game_over": draw_game_over()
    elif STATE == "victory": draw_victory()

def update():
    global STATE, world_progress, enemies_killed
    if STATE == "jogo":
        hero.update()
        scroll_speed = 0
        if hero.right > WIDTH * 0.5 and hero.velocity_x > 0 and world_progress < WORLD_DISTANCE_TO_WIN - WIDTH:
            scroll_speed = hero.velocity_x
        elif hero.left < WIDTH * 0.25 and hero.velocity_x < 0 and world_progress > 0:
            scroll_speed = hero.velocity_x
        if scroll_speed != 0:
            world_progress += scroll_speed; hero.x -= scroll_speed
            victory_flag.x -= scroll_speed
            for obj in enemies + bombs: obj.x -= scroll_speed
        if random.randint(0, 100) > 97: spawn_new_enemy()
        for obj in enemies[:] + bombs[:]: obj.update()
        for enemy in enemies[:]:
            if hero.colliderect(enemy): hero.lose_life()
        for bomb in bombs:
            if bomb.exploded:
                for enemy in enemies[:]:
                    if bomb.colliderect(enemy): enemies.remove(enemy); enemies_killed += 1
        if hero.colliderect(victory_flag): STATE = "victory"

def draw_jogo():
    screen.fill((135, 206, 235))
    screen.draw.filled_rect(Rect(0, GROUND_LEVEL, WIDTH, HEIGHT - GROUND_LEVEL), (34, 139, 34))
    screen.draw.text(f"Inimigos Derrotados: {enemies_killed}", (20, 20), color="white", fontsize=30)
    hero.draw(); victory_flag.draw()
    for obj in bombs + enemies: obj.draw()
    for icon in life_icons: icon.draw()
    screen.draw.text("Setas: Mover | Espaco: Pular | Q: Bomba | Esc: Pausar", bottomleft=(10, HEIGHT - 10), color="white", fontsize=24)

def draw_pause():
    draw_jogo()
    screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), (0, 0, 0, 150))
    screen.draw.text("JOGO PAUSADO", center=(WIDTH/2, HEIGHT/2), fontsize=80, color="white")
    screen.draw.text("Pressione ESC para continuar", center=(WIDTH/2, HEIGHT/2 + 60), fontsize=40, color="white")

def draw_end_screen(title, title_color, bg_color):
    screen.fill(bg_color)
    screen.draw.text(title, center=(WIDTH/2, HEIGHT/2 - 50), fontsize=100, color=title_color)
    screen.draw.text("Pressione Enter para voltar ao menu", center=(WIDTH/2, HEIGHT/2 + 50), fontsize=40, color=title_color)

def draw_victory(): draw_end_screen("Vitoria", "white", (60, 179, 113))
def draw_game_over(): draw_end_screen("Derrota", "black", "red")

def draw_menu():
    try: screen.blit("tela_inicia", (0, 0))
    except: screen.fill((0,0,0))
    btn_iniciar, btn_audio, btn_sair = get_menu_buttons();
    screen.draw.filled_rect(btn_iniciar, "black"); screen.draw.text("Comecar Jogo", center=btn_iniciar.center, color="white", fontsize=40)
    screen.draw.filled_rect(btn_audio, "blue"); status = "Ligados" if sons_ligados else "Desligados"
    screen.draw.text(f"Musica/sons: {status}", center=btn_audio.center, color="white", fontsize=30)
    screen.draw.filled_rect(btn_sair, "red"); screen.draw.text("Saida", center=btn_sair.center, color="white", fontsize=40)

def get_menu_buttons():
    return (Rect(WIDTH//2-120, HEIGHT//2-120, 240, 60),
            Rect(WIDTH//2-120, HEIGHT//2, 240, 60),
            Rect(WIDTH//2-120, HEIGHT//2+120, 240, 60))

def on_mouse_down(pos):
    global STATE
    if STATE == "menu":
        btn_iniciar, btn_audio, btn_sair = get_menu_buttons()
        if btn_iniciar.collidepoint(pos): reset_game()
        elif btn_audio.collidepoint(pos): toggle_audio()
        elif btn_sair.collidepoint(pos): exit()

def toggle_audio():
    global sons_ligados
    sons_ligados = not sons_ligados
    if sons_ligados: music.unpause()
    else: music.pause()

def on_key_down(key):
    global STATE
    if STATE == "jogo":
        if key == keys.SPACE:
            if hero.on_ground: hero.jump()
            elif hero.can_double_jump: hero.double_jump()
        elif key == keys.Q:
            if sons_ligados: sounds.bomb.play()
            bombs.append(Bomb(pos=(hero.pos), direction=hero.facing_direction))
        elif key == keys.ESCAPE:
            STATE = "pause"; music.pause()
    elif STATE == "pause":
        if key == keys.ESCAPE:
            STATE = "jogo"
            if sons_ligados: music.unpause()
    elif STATE == "game_over" or STATE == "victory":
        if key == keys.RETURN or key == keys.KP_ENTER: STATE = "menu"