import pgzrun
import random

# WINDOW
WIDTH = 800
HEIGHT = 600

#STATES 
game_state = 'menu'
music_enabled = True
text_mute_button = 'DESATIVAR'
score = 0

# COLORS
color = {
    'white': (255,255,255),
    'blue': (100, 150, 250),
    'black': (0,0,0),
    'green': (100, 200, 50)
}
# BACKGROUND
background = Actor('background')
background.topleft = 0, 0

# SOUNDS
music.play("music") 
music.set_volume(0.4)

# BUTTONS
start_button = Rect((0, 0), (200, 50))
mute_button = Rect((0, 0), (200, 50))
exit_button = Rect((0, 0), (200, 50))

def on_mouse_down(pos):
    if start_button.collidepoint(pos):
        global game_state 
        game_state = 'gaming'
    if mute_button.collidepoint(pos):
        global music_enabled, text_mute_button
        if(music_enabled == True):
            music.stop()
            music_enabled = False
            text_mute_button = 'ATIVAR'
        else:
            music.play("music")
            music_enabled = True
            text_mute_button = 'DESATIVAR'
    if exit_button.collidepoint(pos):
        exit()

# CLASSES
class Hero:
    def __init__(self, pos):
        self.actor = Actor("hero_1_flipped", pos=pos) 
        self.vel_y = 0
        self.on_ground = False
        
        self.anim_idle_left = ["hero_1"] 
        self.anim_idle_right = ["hero_1_flipped"] 
        
        self.anim_walk_left = [f"hero_{i}" for i in range(1, 13)]
        self.anim_walk_right = [f"hero_{i}_flipped" for i in range(1, 13)]
        
        self.frame = 0
        self.timer = 0
        self.facing_right = True 
        self.alive = True

    def update(self):
        if not self.alive:
            return
        self.vel_y += 0.5
        self.actor.y += self.vel_y
        if self.actor.y >= HEIGHT - 146:
            self.actor.y = HEIGHT - 146
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        moving = False
        if keyboard.left:
            self.actor.x -= 3
            self.facing_right = False
            self.animate(self.anim_walk_left, speed=6) 
            moving = True
        elif keyboard.right:
            self.actor.x += 3
            self.facing_right = True
            self.animate(self.anim_walk_right, speed=6) 
            moving = True
        
        if not moving: 
            if self.facing_right:
                self.animate(self.anim_idle_right, speed=30) 
            else:
                self.animate(self.anim_idle_left, speed=30) 

        if self.actor.left < 0:
            self.actor.left = 0
        if self.actor.right > WIDTH:
            self.actor.right = WIDTH

        if keyboard.up and self.on_ground:
            self.vel_y = -10
            self.on_ground = False

    def animate(self, frames, speed=10):
        self.timer += 1
        if self.timer % speed == 0: 
            self.frame = (self.frame + 1) % len(frames)
            self.actor.image = frames[self.frame]

    def draw(self):
        self.actor.draw()
        
class Enemy:
    def __init__(self, pos, patrol_range):
        self.actor = Actor("frame_1_flipped", pos=pos) 
        self.start_x = pos[0]
        self.range = patrol_range
        self.direction = 1 

        self.anim_left = ["frame_1", "frame_2", "frame_3", "frame_4", "frame_5", "frame_6"]
        self.anim_right = ["frame_1_flipped", "frame_2_flipped", "frame_3_flipped", "frame_4_flipped", "frame_5_flipped", "frame_6_flipped"]
        
        self.frame = 0
        self.timer = 0

    def update(self):
        self.actor.x += self.direction * 2
        
        if self.actor.x > self.start_x + self.range: 
            self.direction = -1 
            self.frame = 0 
        elif self.actor.x < self.start_x - self.range: 
            self.direction = 1
            self.frame = 0 
        
        if self.direction == 1: 
            self.animate(self.anim_right)
        else: 
            self.animate(self.anim_left) 

    def animate(self, frames):
        self.timer += 1
        if self.timer % 8 == 0:
            self.frame = (self.frame + 1) % len(frames)
            self.actor.image = frames[self.frame]

    def draw(self):
        self.actor.draw()

    def rect(self):
        return Rect(self.actor.x - 20, self.actor.y - 20, 40, 40)

# POSITIONS
gap = 70
mute_button.center = (WIDTH / 2, HEIGHT / 2)
start_button.center = (WIDTH / 2, (HEIGHT / 2) - gap)
exit_button.center = (WIDTH / 2, (HEIGHT / 2) + gap)
hero = Hero((100, HEIGHT - 146))
enemies = [Enemy((400, HEIGHT - 146), 100), Enemy((650, HEIGHT - 146), 80)]
coins = []

def create_one_coin():
    global coins
    coin = Actor('coin')
    coin.x = random.randint(50, WIDTH - 50)
    coin.y = random.randint(350, 450)
    
    coins.append(coin)

create_one_coin()

# SCREEN
def draw():
    screen.fill(color['blue'])
    global game_state
    if(game_state == 'menu'):
        draw_menu()
    elif(game_state == 'gaming'):
        draw_game()
    elif game_state == "gameover":
        draw_game_over()
        
def update():
    global game_state, score
    if game_state == "gaming":
        hero.update()
        for e in enemies:
            e.update()
            if hero.actor.colliderect(e.rect()):
                hero.alive = False
                game_state = "gameover"

        for coin in coins[:]:
            if hero.actor.colliderect(coin):
                score += 1
                coins.remove(coin)
        
        if len(coins) == 0:
            create_one_coin()

def on_key_down(key):
    global game_state
    if game_state == "gameover":
        if key == keys.RETURN:
            reset_game()

def draw_menu():
    screen.draw.text("BOUND", midtop=(WIDTH /2,  (HEIGHT / 2) - (gap*2.5) ), color="yellow", fontsize=48)
    
    screen.draw.filled_rect(start_button, color['green']) 
    screen.draw.text("INICIAR", center=start_button.center, color=color['white'])
    
    screen.draw.filled_rect(mute_button, color['green']) 
    screen.draw.text(f"{text_mute_button} MÚSICA", center=mute_button.center, color=color['white'])

    screen.draw.filled_rect(exit_button, color['green']) 
    screen.draw.text("SAIR", center=exit_button.center, color=color['white'])
        
def draw_game_over():
    screen.draw.text("GAME OVER", center=(WIDTH / 2, HEIGHT / 2), fontsize=60, color="red")
    screen.draw.text("PRESSIONE ENTER PARA VOLTAR AO MENU", center=(WIDTH / 2, HEIGHT / 2 + 60), fontsize=30, color="white")

def reset_game():
    global hero, enemies, game_state, score
    hero = Hero((100, HEIGHT - 146))
    enemies = [Enemy((400, HEIGHT - 146), 100), Enemy((650, HEIGHT - 146), 80)]
    score = 0
    coins.clear()
    create_one_coin()
    game_state = "menu"
        
def draw_game():
    background.draw()
    hero.draw()
    for e in enemies:
        e.draw()
    for coin in coins:
        coin.draw()
    
    screen.draw.text(f"Moedas: {score}", topleft=(10, 10), color="yellow", fontsize=36)
        
    
# START GAME
pgzrun.go()