import os
import math
import random
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# --- Config & Assets ---
window.title = 'Playing With Pet Simulator'
window.borderless = False
window.exit_button.visible = False
window.fps_counter.enabled = False

PET_FOLDER = 'assets/pets'
if not os.path.exists(PET_FOLDER): os.makedirs(PET_FOLDER)

# Load Pet Configurations
pet_db = {
    'dog': {'model': f'{PET_FOLDER}/dog/uploads_files_5014764_Dog_Quad.obj', 'texture': f'{PET_FOLDER}/dog/Dog_Quad_Diffuse.png', 'mouth': (0, 0.8, 0.7), 'giant_mouth': (0, 0.85, 0.65)},
    'cat': {'model': 'cube', 'texture': f'{PET_FOLDER}/cat.png', 'mouth': (0, 0.2, 0.5), 'giant_mouth': (0, 0.2, 0.5)},
    'rabbit': {'model': 'cube', 'texture': f'{PET_FOLDER}/rabbit.png', 'mouth': (0, 0.2, 0.5), 'giant_mouth': (0, 0.2, 0.5)},
    'cat1': {'model': f'{PET_FOLDER}/cat/uploads_files_5014805_Cat_Quad.obj', 'texture': f'{PET_FOLDER}/cat/Cat_Quad_Diffuse.png', 'mouth': (0, 0.4, 0.3), 'giant_mouth': (0, 0.3, 0.3)},
    'bunny1': {'model': f'{PET_FOLDER}/bunny/uploads_files_5014646_Rabbit_Quad.obj', 'texture': f'{PET_FOLDER}/bunny/Rabbit_Quad_Diffuse.png', 'mouth': (0, 0.3, 0.3), 'giant_mouth': (0, 0.2, 0.2)},
    'dragon': {'model': f'{PET_FOLDER}/dragon/uploads_files_5784390_Huge_Red_Flying_drago_0109150800_texture.obj', 'texture': f'{PET_FOLDER}/dragon/Huge_Red_Flying_drago_0109150800_texture.png', 'mouth': (0, -0.2, 0.9), 'giant_mouth': (0, -0.25, 0.75), 'preview_offset': (0, 0.5, 0), 'fly_y': 0, 'giant_fly_y': 0.7},
}

# Auto-scan for extra assets
for f in os.listdir(PET_FOLDER):
    if f.lower().endswith(('.png', '.jpg', '.obj', '.gltf', '.glb')):
        name = os.path.splitext(f)[0]
        if name not in pet_db:
            pet_db[name] = {'model': 'cube', 'texture': None, 'mouth': (0, 0.5, 0.5), 'giant_mouth': (0, 0.5, 0.5)}

# Resolve paths
for name, data in pet_db.items():
    if not data.get('texture'):
        for ext in ['.png', '.jpg']:
            if os.path.exists(f'{PET_FOLDER}/{name}{ext}'): data['texture'] = f'{PET_FOLDER}/{name}{ext}'
    if data['model'] == 'cube':
        for ext in ['.obj', '.gltf', '.glb']:
            if os.path.exists(f'{PET_FOLDER}/{name}{ext}'): data['model'] = f'{PET_FOLDER}/{name}{ext}'

pet_names = sorted(list(pet_db.keys()))
textures = {'grass': 'assets/park_grass.png', 'ball': 'assets/ball_texture.png'}

# --- Global State ---
class GameState:
    MENU = 0
    PLAYING = 1

state = GameState.MENU
selected_idx = 0
cur_pet_name = pet_names[0]

# --- Entities & UI ---
camera.position = (0, 3, -5)
camera.rotation = (15, 0, 0)
camera.fov = 40

# 1. MENU UI (Visible at start)
menu_ui = Entity(parent=camera.ui)
bg = Entity(parent=scene, model='quad', texture='grass', scale=(20, 10), z=1, color=color.dark_gray, double_sided=True)

# Preview
preview_pet = Entity(model=pet_db[cur_pet_name]['model'], texture=pet_db[cur_pet_name]['texture'], scale=1, position=(0, 1.5, 0), rotation=(0, 180, 0))

# Menu Widgets
title = Text(parent=menu_ui, text="PILIH HEWAN PELIHARAAN", position=(0, 0.4), origin=(0, 0), scale=1.5)
desc = Text(parent=menu_ui, text=cur_pet_name.capitalize(), position=(0, -0.35), origin=(0, 0), scale=1.0, color=color.yellow, background=True)
btn_prev = Button(parent=menu_ui, text='Prev', position=(-0.3, 0), scale=(0.1, 0.05), on_click=lambda: change_pet(-1))
btn_next = Button(parent=menu_ui, text='Next', position=(0.3, 0), scale=(0.1, 0.05), on_click=lambda: change_pet(1))
btn_start = Button(parent=menu_ui, text='MULAI', position=(0, -0.2), scale=(0.25, 0.06), color=color.green, on_click=lambda: start_game())

# 2. HUD UI (Visible when playing)
hud_ui = Entity(parent=camera.ui, enabled=False)
txt_interact = Text(parent=hud_ui, text="[E] Ambil Bola", position=(0, -0.2), origin=(0, 0), scale=1.5, color=color.orange, enabled=False)
txt_help = Text(parent=hud_ui, text="[WASD] Jalan [Click] Lempar [R-Click] Panggil [E] Ambil [G] Besar [M] Mirror [C] Camera [ESC] Menu", position=(-0.85, 0.45), scale=1)

# 3. PAUSE MENU UI (Visible when paused)
pause_ui = Entity(parent=camera.ui, enabled=False)
btn_menu = Button(parent=pause_ui, text='Menu', position=(-0.7, 0.1), scale=(0.25, 0.08), color=color.azure, on_click=lambda: stop_game())
btn_exit = Button(parent=pause_ui, text='Exit', position=(-0.7, 0.0), scale=(0.25, 0.08), color=color.red, on_click=application.quit)

# Game Objects
level_root = None
player = None
pet = None
ball = None
mirror_pet = None
ground = None

# --- Logic ---
def change_pet(d):
    global selected_idx, cur_pet_name
    selected_idx = (selected_idx + d) % len(pet_names)
    cur_pet_name = pet_names[selected_idx]
    
    data = pet_db[cur_pet_name]
    preview_pet.model = data['model']
    preview_pet.texture = data['texture']
    preview_pet.rotation = (0, 180, 0)
    
    offset = data.get('preview_offset', (0,0,0))
    preview_pet.position = (offset[0], 1.5 + offset[1], offset[2])
    preview_pet.scale = 1
    
    desc.text = cur_pet_name.capitalize()
    preview_pet.animate_rotation_y(preview_pet.rotation_y + 360, duration=0.5)

def start_game():
    global state, level_root, player, pet, ground
    state = GameState.PLAYING
    
    # Toggle UIs
    menu_ui.enabled = False
    bg.enabled = False
    preview_pet.enabled = False
    hud_ui.enabled = True
    pause_ui.enabled = False
    mouse.locked = True
    
    # Environment
    level_root = Entity()
    Sky(parent=level_root, texture='assets/realistic_sky.png' if os.path.exists('assets/realistic_sky.png') else None)
    DirectionalLight(parent=level_root, y=2, z=3, shadows=False)
    AmbientLight(parent=level_root, color=color.rgba(100,100,100,0.5))
    scene.fog_density = 0.02; scene.fog_color = color.azure

    # Ground
    grass_tex = 'assets/realistic_grass.png' if os.path.exists('assets/realistic_grass.png') else textures['grass']
    ground = Entity(parent=level_root, model='plane', scale=(100, 1, 100), texture=grass_tex, texture_scale=(50,50), collider='box')
    
    # Walls
    for p in [(0,0,50), (0,0,-50), (50,0,0), (-50,0,0)]:
        Entity(parent=level_root, model='cube', scale=(100 if p[2] else 1, 10, 1 if p[2] else 100), position=p, collider='box', visible=False)

    # Trees
    for _ in range(40):
        pos = (random.choice([-1,1])*random.uniform(35,45), 0, random.uniform(-45,45)) if random.random() > 0.5 else (random.uniform(-45,45), 0, random.choice([-1,1])*random.uniform(35,45))
        Tree(position=pos, parent=level_root)

    # Player (First Person + George Model)
    player = FirstPersonController(position=(5, 2, -10))
    player.cursor.texture = textures['ball']
    camera.position = (0, 0.8, 0.5)
    
    p_body = Entity(parent=player, model='assets/player/George.obj', texture='assets/player/George_Texture.png', scale=0.6, double_sided=True)
    p_body.walk_timer = 0
    player.body_mesh = p_body # Attach for access

    # Pet
    pet = Pet(cur_pet_name, position=(0, 1, 0))

def stop_game():
    global state, level_root, player, pet, ball, mirror_pet
    state = GameState.MENU
    
    # Cleanup
    destroy(level_root); destroy(player); destroy(pet); destroy(ball); destroy(mirror_pet)
    level_root = player = pet = ball = mirror_pet = None
    
    # Restore Camera & UI
    camera.parent = scene
    camera.position = (0, 3, -5); camera.rotation = (15, 0, 0); camera.fov = 40
    
    menu_ui.enabled = True
    bg.enabled = True
    preview_pet.enabled = True
    preview_pet.position = (0, 1.5, 0); preview_pet.rotation = (0, 180, 0)
    
    hud_ui.enabled = False
    pause_ui.enabled = False
    
    mouse.locked = False
    mouse.visible = True

# --- Classes ---
class Tree(Entity):
    def __init__(self, position, parent):
        opts = [f'assets/trees/{f}' for f in os.listdir('assets/trees') if f.endswith('.obj')] if os.path.exists('assets/trees') else []
        model = random.choice(opts) if opts else 'cube'
        
        super().__init__(parent=parent, position=position, model=model, collider='box', scale=random.uniform(0.8, 1.5))
        if model == 'cube': # Fallback
            self.color = color.brown; self.scale = (1, 4, 1); self.texture = 'assets/tree_bark.png'
            Entity(parent=self, model='cube', position=(0,1,0), scale=(2.5,0.5,2.5), texture='assets/tree_leaves.png')

class Pet(Entity):
    def __init__(self, type_name, position):
        data = pet_db[type_name]
        super().__init__(model=data['model'], texture=data['texture'], position=position, scale=0.8, collider='box', double_sided=True)
        self.data = data
        self.mouth_def = data.get('mouth', (0, 0.5, 0.5))
        self.mouth_giant = data.get('giant_mouth', self.mouth_def)
        self.fly_y = data.get('fly_y', 0)
        self.fly_giant = data.get('giant_fly_y', self.fly_y * 2.5)
        
        self.speed = 4
        self.target = None
        self.anim_timer = 0
        
        if self.model.name == 'cube': # Head for cube pets
            Entity(parent=self, model='cube', scale=0.8, position=(0, 0.5, 0), texture=self.texture)

    def update(self):
        if not self.target: self.target = player
        
        dist = distance(self.position, self.target.position)
        self.look_at_2d(self.target.position, 'y')
        
        stop_range = 4 if self.target == player else 1
        if dist > stop_range:
            self.position += self.forward * self.speed * time.dt
            self.anim_timer += time.dt * 15
            
            # Procedural Animation (Bob & Waddle)
            t = clamp((self.scale_x - 0.8) / 1.7, 0, 1)
            base_y = lerp(self.fly_y, self.fly_giant, t)
            self.y = 0.4 + base_y + abs(math.sin(self.anim_timer)) * 0.3
            self.rotation_z = math.sin(self.anim_timer) * 8
        else:
            self.rotation_z = lerp(self.rotation_z, 0, time.dt * 10)
            
        # Fetch Logic
        if self.target == ball and dist < 2:
            ball.parent = self
            ball.position = self.mouth_giant if self.scale_x > 1.5 else self.mouth_def
            ball.scale = 0.25 / self.scale_x
            self.target = player

class Ball(Entity):
    def __init__(self, position, velocity):
        super().__init__(model='sphere', scale=0.25, color=color.red, collider='sphere', texture=textures['ball'], position=position)
        self.velocity = Vec3(velocity)
    
    def update(self):
        if self.parent != scene: return # Carried
        
        self.velocity.y -= 25 * time.dt # Gravity
        self.position += self.velocity * time.dt # Move
        
        if self.y < 0.25: # Bounce
            self.y = 0.25; self.velocity.y *= -0.6
            self.velocity.x *= 0.95; self.velocity.z *= 0.95 # Friction
            
        self.rotation_x += self.velocity.z * 10 * time.dt
        self.rotation_z -= self.velocity.x * 10 * time.dt
        if self.y < -50: destroy(self)

# --- Input & Loop ---
def input(key):
    global ball, mirror_pet
    
    if key == 'escape' and state == GameState.PLAYING:
        mouse.locked = not mouse.locked
        mouse.visible = not mouse.locked
        pause_ui.enabled = not mouse.locked # Toggle Pause Menu

    if state == GameState.PLAYING:
        if key == 'left mouse down': # Throw
            if ball: destroy(ball)
            ball = Ball(camera.world_position + camera.forward * 2, camera.forward * 20 + Vec3(0,5,0))
            if pet: pet.target = ball
            
        if key == 'right mouse down' and pet: # Call
            pet.target = player
            if ball and ball.parent == pet:
                ball.parent = scene; ball.scale = 0.25; ball.y = 0.5
        
        if key == 'e' and txt_interact.enabled: # Pick up
            if ball: destroy(ball); ball = None
            txt_interact.enabled = False
            
        if key == 'c': # Camera
            target = (0, 2, -7) if abs(camera.z) < 1 else (0, 0.8, 0.5)
            camera.animate_position(target, 0.2, curve=curve.out_sine)
            
        if key == 'g' and pet: # Giant
            s = 2.5 if pet.scale.x < 1 else 0.8
            pet.animate_scale((s,s,s), 0.5, curve=curve.out_bounce)
            
        if key == 'm' and pet: # Mirror
            if mirror_pet: destroy(mirror_pet); mirror_pet = None
            else: mirror_pet = Entity(model=pet.model.name if hasattr(pet.model,'name') else 'cube', texture=pet.texture, scale=pet.scale, alpha=0.5, color=color.lime)



def update():
    # Rotate Preview (Menu)
    if state == GameState.MENU and mouse.left:
        preview_pet.rotation_y -= mouse.velocity.x * 200
        preview_pet.rotation_x -= mouse.velocity.y * 200
    # Camera Collision (Prevent going under ground)
    if camera.world_position.y < 0.2:
        camera.world_position = Vec3(camera.world_position.x, 0.2, camera.world_position.z)

    # Mirror Logic
    if mirror_pet and pet:
        mirror_pet.position = (-pet.x, pet.y, pet.z)
        mirror_pet.rotation = (pet.rotation_x, -pet.rotation_y, -pet.rotation_z)
        mirror_pet.scale = pet.scale

    # Player Animation (George)
    if player and hasattr(player, 'body_mesh'):
        move = held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']
        b = player.body_mesh
        if move:
            b.walk_timer += time.dt * 10
            b.rotation_z = math.sin(b.walk_timer) * 8
            b.rotation_x = 5
            b.y = 0 + abs(math.sin(b.walk_timer)) * 0.05
        else:
            b.rotation_z = lerp(b.rotation_z, 0, time.dt*10)
            b.rotation_x = lerp(b.rotation_x, 0, time.dt*10)
            b.y = lerp(b.y, 0, time.dt * 10)

    # Interact Prompt
    if pet and player and ball and ball.parent == pet:
        txt_interact.enabled = (distance(player.position, pet.position) < 3)
    else:
        txt_interact.enabled = False
        
    # Debug Calibration
    if pet and ball and ball.parent == pet:
        if held_keys['up arrow']: pet.mouth_def = (pet.mouth_def[0], pet.mouth_def[1]+0.01, pet.mouth_def[2])
        if held_keys['down arrow']: pet.mouth_def = (pet.mouth_def[0], pet.mouth_def[1]-0.01, pet.mouth_def[2])

app.run()

