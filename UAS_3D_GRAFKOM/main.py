import os
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# --- Pengaturan Jendela Game ---
window.title = 'Playing With Pet Simulator'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = False

# --- Pemuatan Aset ---
pet_folder = 'assets/pets'
if not os.path.exists(pet_folder):
    os.makedirs(pet_folder)

# --- Konfigurasi Manual Hewan ---
# Tambahkan hewan baru di sini dengan format: 'nama': {model, texture, posisi_mulut}
pet_assets = {
    'dog': {'model': f'{pet_folder}/dog/uploads_files_5014764_Dog_Quad.obj', 'texture': f'{pet_folder}/dog/Dog_Quad_Diffuse.png', 'mouth_pos': (0, 0.8, 0.7), 'mouth_pos_giant': (0, 0.85, 0.65)},
    'cat': {'model': 'cube', 'texture': f'{pet_folder}/cat.png', 'mouth_pos': (0, 0.2, 0.5), 'mouth_pos_giant': (0, 0.2, 0.5)},
    'rabbit': {'model': 'cube', 'texture': f'{pet_folder}/rabbit.png', 'mouth_pos': (0, 0.2, 0.5), 'mouth_pos_giant': (0, 0.2, 0.5)},
    'cat1': {'model': f'{pet_folder}/cat/uploads_files_5014805_Cat_Quad.obj', 'texture': f'{pet_folder}/cat/Cat_Quad_Diffuse.png', 'mouth_pos': (0, 0.4, 0.3), 'mouth_pos_giant': (0, 0.3, 0.3)},
    'bunny1': {'model': f'{pet_folder}/bunny/uploads_files_5014646_Rabbit_Quad.obj', 'texture': f'{pet_folder}/bunny/Rabbit_Quad_Diffuse.png', 'mouth_pos': (0, 0.3, 0.3), 'mouth_pos_giant': (0, 0.2, 0.2)},
    'dragon': {'model': f'{pet_folder}/dragon/uploads_files_5784390_Huge_Red_Flying_drago_0109150800_texture.obj', 'texture': f'{pet_folder}/dragon/Huge_Red_Flying_drago_0109150800_texture.png', 'mouth_pos': (0, -0.2, 0.9), 'mouth_pos_giant': (0, -0.25, 0.75), 'preview_offset': (0, 0.5, 0), 'game_y_offset': 0, 'game_y_offset_giant': 0.7},
}

# Scan otomatis file di folder assets jika belum terdaftar
pet_files = os.listdir(pet_folder)
for f in pet_files:
    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.obj', '.gltf', '.glb')):
        name = os.path.splitext(f)[0]
        if name not in pet_assets:
            pet_assets[name] = {'model': 'cube', 'texture': None, 'mouth_pos': (0, 0.5, 0.5), 'mouth_pos_giant': (0, 0.5, 0.5), 'preview_offset': (0, 0, 0)}

# Lengkapi tekstur dan model hasil scan otomatis
for name in pet_assets:
    if not pet_assets[name]['texture']:
        if os.path.exists(f'{pet_folder}/{name}.png'): pet_assets[name]['texture'] = f'{pet_folder}/{name}.png'
        elif os.path.exists(f'{pet_folder}/{name}.jpg'): pet_assets[name]['texture'] = f'{pet_folder}/{name}.jpg'
            
    if pet_assets[name]['model'] == 'cube':
        if os.path.exists(f'{pet_folder}/{name}.obj'): pet_assets[name]['model'] = f'{pet_folder}/{name}.obj'
        elif os.path.exists(f'{pet_folder}/{name}.gltf'): pet_assets[name]['model'] = f'{pet_folder}/{name}.gltf'
        elif os.path.exists(f'{pet_folder}/{name}.glb'): pet_assets[name]['model'] = f'{pet_folder}/{name}.glb'

pet_types = sorted(list(pet_assets.keys()))
textures = {'grass': 'assets/park_grass.png', 'ball': 'assets/ball_texture.png'}

# --- Status Game ---
class GameState:
    MENU = 0
    PLAYING = 1

current_state = GameState.MENU
selected_pet_index = 0

# --- Objek Menu Utama ---
camera.position = (0, 3, -5)
camera.rotation = (15, 0, 0)
camera.fov = 40
background = Entity(parent=scene, model='quad', texture='grass', scale=(20, 10), z=1, color=color.dark_gray, double_sided=True)

# Preview Hewan di Menu
current_pet_name = pet_types[0]
pet_preview = Entity(
    model=pet_assets[current_pet_name]['model'], 
    texture=pet_assets[current_pet_name]['texture'], 
    scale=(1, 1, 1), position=(0, 1.5, 0), rotation=(0, 180, 0)
)

# UI Menu
title_text = Text(text="PILIH HEWAN PELIHARAAN", position=(0, 0.4), origin=(0, 0), scale=1.5, color=color.white)
desc_text = Text(text=f"{current_pet_name.capitalize()}", position=(0, -0.35), origin=(0, 0), scale=1.0, color=color.yellow, background=True)

btn_prev = Button(text='Prev', position=(-0.3, 0), scale=(0.1, 0.05), on_click=lambda: change_pet(-1))
btn_next = Button(text='Next', position=(0.3, 0), scale=(0.1, 0.05), on_click=lambda: change_pet(1))
btn_start = Button(text='MULAI Bermain', position=(0, -0.2), scale=(0.25, 0.06), color=color.green, on_click=lambda: start_game())

# UI Saat Bermain
btn_ingame_menu = Button(text='Kembali ke Menu', position=(-0.7, 0.1), scale=(0.25, 0.08), color=color.azure, enabled=False, on_click=lambda: return_to_menu())
btn_ingame_exit = Button(text='Keluar Game', position=(-0.7, 0.0), scale=(0.25, 0.08), color=color.red, enabled=False, on_click=application.quit)
interaction_text = Text(text="[E] Ambil Bola", position=(0, -0.2), origin=(0, 0), scale=1.5, color=color.orange, enabled=False)

# Variabel Global Game
ground = None
player = None
pet = None
ball = None
level_holder = None
mirror_pet = None

# --- Fungsi Kendali Menu ---
def change_pet(direction):
    global selected_pet_index, current_pet_name
    selected_pet_index = (selected_pet_index + direction) % len(pet_types)
    current_pet_name = pet_types[selected_pet_index]
    
    pet_preview.model = pet_assets[current_pet_name]['model']
    pet_preview.texture = pet_assets[current_pet_name]['texture']
    pet_preview.rotation = (0, 180, 0)
    
    base_pos = (0, 1.5, 0)
    offset = pet_assets[current_pet_name].get('preview_offset', (0, 0, 0))
    pet_preview.position = (base_pos[0] + offset[0], base_pos[1] + offset[1], base_pos[2] + offset[2])
    pet_preview.scale = (1, 1, 1)
        
    desc_text.text = f"{current_pet_name.capitalize()}"
    pet_preview.animate_rotation_y(pet_preview.rotation_y + 360, duration=0.5)

def start_game():
    global current_state, ground, player, pet, level_holder
    
    # Sembunyikan Menu
    title_text.enabled = desc_text.enabled = btn_prev.enabled = btn_next.enabled = btn_start.enabled = pet_preview.enabled = background.enabled = False
    
    current_state = GameState.PLAYING
    level_holder = Entity()
    
    # Langit & Cahaya
    sky_texture = 'assets/realistic_sky.png' if os.path.exists('assets/realistic_sky.png') else None
    Sky(parent=level_holder, texture=sky_texture)
    scene.fog_density = 0.02
    scene.fog_color = color.azure
    
    pivot = Entity(parent=level_holder)
    DirectionalLight(parent=pivot, y=2, z=3, shadows=False)
    AmbientLight(parent=level_holder, color=color.rgba(100, 100, 100, 0.5))
    
    # Buat Dunia (Darat & Pohon)
    custom_level = None
    if os.path.exists('assets/level.obj'): custom_level = 'assets/level.obj'
    elif os.path.exists('assets/park.obj'): custom_level = 'assets/park.obj'
        
    if custom_level:
        level = Entity(parent=level_holder, model=custom_level, texture='assets/level.png', scale=1, collider='mesh')
    else:
        grass_tex = 'assets/realistic_grass.png' if os.path.exists('assets/realistic_grass.png') else textures['grass']
        ground = Entity(parent=level_holder, model='plane', scale=(100, 1, 100), color=color.white, texture=grass_tex, texture_scale=(50, 50), collider='box')
        
        # Pembatas Dunia
        Entity(parent=level_holder, model='cube', scale=(100, 10, 1), position=(0, 0, 50), collider='box', visible=False)
        Entity(parent=level_holder, model='cube', scale=(100, 10, 1), position=(0, 0, -50), collider='box', visible=False)
        Entity(parent=level_holder, model='cube', scale=(1, 10, 100), position=(50, 0, 0), collider='box', visible=False)
        Entity(parent=level_holder, model='cube', scale=(1, 10, 100), position=(-50, 0, 0), collider='box', visible=False)
    
        for i in range(40):
            side = random.randint(0, 3)
            x = random.uniform(-45, 45) if side < 2 else (35 if side == 2 else -35)
            z = random.uniform(35, 45) if side == 0 else (random.uniform(-45, -35) if side == 1 else random.uniform(-45, 45))
            Tree(position=(x, 0, z), parent=level_holder)

    # Pemain (George)
    player = FirstPersonController(position=(5, 2, -10))
    player.cursor.visible = True 
    player.cursor.texture = textures['ball']
    camera.position = (0, 0.8, 0.5)
    
    player_body = Entity(
        parent=player, model='assets/George.obj', texture='assets/George_Texture.png',
        position=(0, 0, 0), scale=0.6, double_sided=True
    )
    player_body.walk_timer = 0
    
    # Fungsi Animasi Jalan George
    def animate_george():
        if not player_body or not player: return
        moving = any(held_keys[k] for k in ('w', 'a', 's', 'd'))
        if moving:
            player_body.walk_timer += time.dt * 10
            player_body.rotation_z = math.sin(player_body.walk_timer) * 8
            player_body.rotation_x = 5 
            player_body.y = -3.1 + abs(math.sin(player_body.walk_timer)) * 0.05
        else:
            player_body.rotation_z = lerp(player_body.rotation_z, 0, time.dt * 10)
            player_body.rotation_x = lerp(player_body.rotation_x, 0, time.dt * 10)
            player_body.y = lerp(player_body.y, -3.1, time.dt * 10)

    # Simpan fungsi animasi ke player_body agar bisa dipanggil di update
    player.animate_george = animate_george

    # Munculkan Hewan
    pet = Pet(current_pet_name, position=(0, 1, 0))
    Text(parent=level_holder, text="[WASD] Jalan  [L-Click] Lempar  [R-Click] Panggil  [E] Ambil  [G] Besar/Kecil  [M] Mirror  [C] Camera  [ESC] Menu", position=(-0.85, 0.45), scale=1)

def return_to_menu():
    global current_state, player, pet, ball, level_holder, mirror_pet
    camera.parent = scene
    if level_holder: destroy(level_holder)
    if player: destroy(player)
    if pet: destroy(pet)
    if mirror_pet: destroy(mirror_pet)
    if ball: destroy(ball)
    
    player = pet = mirror_pet = ball = level_holder = None
    current_state = GameState.MENU
    
    camera.position, camera.rotation, camera.fov = (0, 3, -5), (15, 0, 0), 40
    pet_preview.position, pet_preview.rotation = (0, 1.5, 0), (0, 180, 0)
    
    title_text.enabled = desc_text.enabled = btn_prev.enabled = btn_next.enabled = btn_start.enabled = pet_preview.enabled = background.enabled = True
    btn_ingame_menu.enabled = btn_ingame_exit.enabled = interaction_text.enabled = False
    mouse.locked, mouse.visible = False, True

# --- Kelas Objek Game (Tree, Pet, Ball) ---
tree_folder = 'assets/trees'
available_trees = [f'{tree_folder}/{f}' for f in os.listdir(tree_folder) if f.endswith('.obj')] if os.path.exists(tree_folder) else []

class Tree(Entity):
    def __init__(self, position=(0,0,0), parent=scene):
        model_name, texture_name, scale_val = 'cube', None, (1, 1, 1)
        if available_trees:
            model_name = random.choice(available_trees)
            s = random.uniform(0.8, 1.5)
            scale_val = (s, s, s)
        elif os.path.exists('assets/tree.obj'):
            model_name = 'assets/tree.obj'
            texture_name = 'assets/tree.png' if os.path.exists('assets/tree.png') else None
        
        super().__init__(model=model_name, position=position, scale=scale_val, texture=texture_name, collider='box', parent=parent)
        if model_name == 'cube':
            self.texture, self.color = 'assets/tree_bark.png', color.white
            self.leaves = Entity(parent=self, model='cube', position=(0, 1, 0), scale=(2.5, 0.5, 2.5), texture='assets/tree_leaves.png')

class Pet(Entity):
    def __init__(self, pet_type, position):
        super().__init__(
            model=pet_assets[pet_type]['model'], position=position, scale=(0.8, 0.8, 0.8),
            texture=pet_assets[pet_type]['texture'], collider='box', double_sided=True
        )
        self.pet_type = pet_type
        self.mouth_pos = pet_assets[pet_type].get('mouth_pos', (0, 0.5, 0.5))
        self.mouth_pos_giant = pet_assets[pet_type].get('mouth_pos_giant', self.mouth_pos)
        self.game_y_offset = pet_assets[pet_type].get('game_y_offset', 0)
        self.game_y_offset_giant = pet_assets[pet_type].get('game_y_offset_giant', self.game_y_offset * 2.5)
        self.speed, self.target, self.walk_timer = 4, None, 0
        if self.model.name == 'cube':
            Entity(parent=self, model='cube', scale=(0.8, 0.8, 0.8), position=(0, 0.5, 0), texture=self.texture)

    def update(self):
        if self.target:
            self.look_at_2d(self.target.position, 'y')
            dist = distance(self.position, self.target.position)
            stop_dist = 4 if self.target == player else 1
            
            t = clamp((self.scale_x - 0.8) / (2.5 - 0.8), 0, 1)
            current_y_offset = lerp(self.game_y_offset, self.game_y_offset_giant, t)

            if dist > stop_dist:
                self.position += self.forward * self.speed * time.dt
                self.walk_timer += time.dt * 15
                self.y = 0.4 + current_y_offset + abs(math.sin(self.walk_timer)) * 0.3 
                self.rotation_z = math.sin(self.walk_timer) * 8
            else:
                self.y, self.rotation_z, self.walk_timer = 0.4 + current_y_offset, lerp(self.rotation_z, 0, time.dt * 10), 0
                
            if self.target == ball and dist < 2:
                ball.parent = self
                ball.position = self.mouth_pos
                ball.scale = 0.25 / self.scale_x
                self.target = player
        else:
            self.target = player

class Ball(Entity):
    def __init__(self, position=(0,0,0), velocity=(0,0,0)):
        super().__init__(model='sphere', scale=0.25, color=color.red, collider='sphere', texture=textures['ball'], position=position)
        self.velocity, self.friction, self.gravity = Vec3(velocity), 2.0, 25

    def update(self):
        if self.parent != scene: return
        self.velocity.y -= self.gravity * time.dt
        self.position += self.velocity * time.dt
        
        if self.y < 0.25: 
            self.y, self.velocity.y = 0.25, self.velocity.y * -0.6
            if abs(self.velocity.y) < 1: self.velocity.y = 0
            self.velocity.x -= self.velocity.x * self.friction * time.dt
            self.velocity.z -= self.velocity.z * self.friction * time.dt
        
        self.rotation_x += self.velocity.z * 150 * time.dt
        self.rotation_z -= self.velocity.x * 150 * time.dt
        if self.y < -50: destroy(self)

# --- Sistem Input (Keyboard & Mouse) ---
def input(key):
    global current_state, player, pet, ball, level_holder, mirror_pet
    
    if key == 'escape' and current_state == GameState.PLAYING:
        mouse.locked = not mouse.locked
        mouse.visible = not mouse.locked
        btn_ingame_menu.enabled = btn_ingame_exit.enabled = not mouse.locked

    if current_state == GameState.PLAYING:
        if key == 'left mouse down':
            if ball: destroy(ball)
            ball = Ball(position=camera.world_position + camera.forward * 2, velocity=camera.forward * 20 + Vec3(0, 5, 0))
            if pet: pet.target = ball

        if key == 'right mouse down' and pet:
            pet.target = player
            if ball and ball.parent == pet:
                ball.parent, ball.scale, ball.y = scene, 0.25, 0.5

        if key == 'e' and interaction_text.enabled:
            if ball: destroy(ball)
            ball = None
            interaction_text.enabled = False

        if key == 'c': # Toggle Kamera FPP/TPP
            target_pos = (0, 1, -4) if abs(camera.z) < 1 else (0, 0.5, 0.5)
            camera.animate_position(target_pos, duration=0.2, curve=curve.out_sine)

        if key == 'g' and pet: # Toggle Ukuran
            new_scale = (2.5, 2.5, 2.5) if pet.scale.x < 1.0 else (0.8, 0.8, 0.8)
            pet.animate_scale(new_scale, duration=0.5, curve=curve.out_bounce)

        if key == 'm' and pet: # Toggle Mirror
            if mirror_pet:
                destroy(mirror_pet)
                mirror_pet = None
            else:
                mirror_pet = Entity(model=pet.model.name if hasattr(pet.model, 'name') else 'cube', texture=pet.texture, scale=pet.scale, alpha=0.5, color=color.lime)

# --- Loop Update Utama ---
def update():
    global mirror_pet, pet, interaction_text
    if current_state == GameState.PLAYING:
        # Update Mirror
        if mirror_pet and pet:
            mirror_pet.position = (-pet.x, pet.y, pet.z)
            mirror_pet.rotation = (pet.rotation_x, -pet.rotation_y, -pet.rotation_z)
            mirror_pet.scale = pet.scale

        # Logika Bola di Mulut & Kalibrasi
        if pet and ball and ball.parent == pet:
            ball.scale = (0.25 / pet.scale.x,) * 3
            is_giant = pet.scale.x > 1.5
            current_mouth_pos = list(pet.mouth_pos_giant if is_giant else pet.mouth_pos)
            
            # Kalibrasi posisi mulut dengan tombol Panah (Arrow Keys)
            speed = time.dt * 0.5
            if held_keys['up arrow']: current_mouth_pos[1] += speed
            if held_keys['down arrow']: current_mouth_pos[1] -= speed
            if held_keys['right arrow']: current_mouth_pos[2] += speed
            if held_keys['left arrow']: current_mouth_pos[2] -= speed
            
            new_pos = tuple(current_mouth_pos)
            if is_giant: pet.mouth_pos_giant = new_pos
            else: pet.mouth_pos = new_pos
            ball.position = new_pos

        # Animasi George
        if hasattr(player, 'animate_george'): player.animate_george()

        # Cek Jarak Interaksi Ambil Bola
        if pet and player and ball and ball.parent == pet and distance(player.position, pet.position) < 3.0:
            interaction_text.enabled = True
        else:
            interaction_text.enabled = False

    elif current_state == GameState.MENU:
        if mouse.left: # Putar pratinjau hewan
            pet_preview.rotation_y -= mouse.velocity.x * 200
            pet_preview.rotation_x -= mouse.velocity.y * 200

app.run()
