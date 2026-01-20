import os
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# Window Settings
window.title = 'Playing With Pet Simulator'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = False

# --- Resource Loading ---
pet_folder = 'assets/pets'
if not os.path.exists(pet_folder):
    os.makedirs(pet_folder)

# ==========================================
# KONFIGURASI MANUAL (TAMBAH HEWAN DI SINI)
# ==========================================
# Format: 'Nama': {'model': 'path/to/model.obj', 'texture': 'path/to/texture.png'}
# Jika model kosong, akan pakai kotak (cube).

pet_assets = {
    'dog': {'model': f'{pet_folder}/dog/uploads_files_5014764_Dog_Quad.obj', 'texture': f'{pet_folder}/dog/Dog_Quad_Diffuse.png', 'mouth_pos': (0, 0.8, 0.7), 'mouth_pos_giant': (0, 0.85, 0.65)},
    'cat': {'model': 'cube', 'texture': f'{pet_folder}/cat.png', 'mouth_pos': (0, 0.2, 0.5), 'mouth_pos_giant': (0, 0.2, 0.5)},
    'rabbit': {'model': 'cube', 'texture': f'{pet_folder}/rabbit.png', 'mouth_pos': (0, 0.2, 0.5), 'mouth_pos_giant': (0, 0.2, 0.5)},
    'cat1': {'model': f'{pet_folder}/cat/uploads_files_5014805_Cat_Quad.obj', 'texture': f'{pet_folder}/cat/Cat_Quad_Diffuse.png', 'mouth_pos': (0, 0.4, 0.3), 'mouth_pos_giant': (0, 0.3, 0.3)},
    'bunny1': {'model': f'{pet_folder}/bunny/uploads_files_5014646_Rabbit_Quad.obj', 'texture': f'{pet_folder}/bunny/Rabbit_Quad_Diffuse.png', 'mouth_pos': (0, 0.3, 0.3), 'mouth_pos_giant': (0, 0.2, 0.2)},
    'dragon': {'model': f'{pet_folder}/dragon/uploads_files_5784390_Huge_Red_Flying_drago_0109150800_texture.obj', 'texture': f'{pet_folder}/dragon/Huge_Red_Flying_drago_0109150800_texture.png', 'mouth_pos': (0, -0.2, 0.9), 'mouth_pos_giant': (0, -0.25, 0.75), 'preview_offset': (0, 0.5, 0), 'game_y_offset': 0, 'game_y_offset_giant': 0.7},
    # CONTOH CARA NAMBAH SENDIRI:
    # 'naga': {'model': 'assets/naga.obj', 'texture': 'assets/naga.png'},
}
# ==========================================

# Auto-scan (Opsional, akan menambahkan file yang ada di folder tapi belum ditulis di atas)
pet_files = os.listdir(pet_folder)
for f in pet_files:
    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.obj', '.gltf', '.glb')):
        name = os.path.splitext(f)[0]
        if name not in pet_assets:
            pet_assets[name] = {'model': 'cube', 'texture': None, 'mouth_pos': (0, 0.5, 0.5), 'mouth_pos_giant': (0, 0.5, 0.5), 'preview_offset': (0, 0, 0)}

# Update properti auto-scan
for name in pet_assets:
    # Cek Texture jika belum ada
    if not pet_assets[name]['texture']:
        if os.path.exists(f'{pet_folder}/{name}.png'):
            pet_assets[name]['texture'] = f'{pet_folder}/{name}.png'
        elif os.path.exists(f'{pet_folder}/{name}.jpg'):
            pet_assets[name]['texture'] = f'{pet_folder}/{name}.jpg'
            
    # Cek Model jika belum ada atau masih default 'cube' tapi ada file obj
    if pet_assets[name]['model'] == 'cube':
        if os.path.exists(f'{pet_folder}/{name}.obj'):
            pet_assets[name]['model'] = f'{pet_folder}/{name}.obj'
        elif os.path.exists(f'{pet_folder}/{name}.gltf'):
            pet_assets[name]['model'] = f'{pet_folder}/{name}.gltf'
        elif os.path.exists(f'{pet_folder}/{name}.glb'):
            pet_assets[name]['model'] = f'{pet_folder}/{name}.glb'

pet_types = sorted(list(pet_assets.keys()))

textures = {
    'grass': 'assets/park_grass.png',
    'ball': 'assets/ball_texture.png'
}

# --- Game State ---
class GameState:
    MENU = 0
    PLAYING = 1

current_state = GameState.MENU
selected_pet_index = 0

# --- Entities ---

# Menu Entities
camera.position = (0, 3, -5) # Further back and higher for 'smaller' look
camera.rotation = (15, 0, 0)
camera.fov = 40 # Force default FOV
background = Entity(parent=scene, model='quad', texture='grass', scale=(20, 10), z=1, color=color.dark_gray, double_sided=True)

# Preview Entity
current_pet_name = pet_types[0]
pet_preview = Entity(
    model=pet_assets[current_pet_name]['model'], 
    texture=pet_assets[current_pet_name]['texture'], 
    scale=(1, 1, 1), 
    position=(0, 1.5, 0), 
    rotation=(0, 180, 0)
)
# If custom model is HUGE, we might want to normalize scale, but for now trusting user assets.

# UI Entities
title_text = Text(text="PILIH HEWAN PELIHARAAN", position=(0, 0.4), origin=(0, 0), scale=1.5, color=color.white) # Scale 2 -> 1.5
desc_text = Text(text=f"{current_pet_name.capitalize()}", position=(0, -0.35), origin=(0, 0), scale=1.0, color=color.yellow, background=True) # Scale 1.2 -> 1.0

btn_prev = Button(text='Prev', position=(-0.3, 0), scale=(0.1, 0.05), on_click=lambda: change_pet(-1)) # Smaller
btn_next = Button(text='Next', position=(0.3, 0), scale=(0.1, 0.05), on_click=lambda: change_pet(1)) # Smaller
btn_start = Button(text='MULAI Bermain', position=(0, -0.2), scale=(0.25, 0.06), color=color.green, on_click=lambda: start_game()) # Smaller

# In-Game Menu UI (Hidden by default)
btn_ingame_menu = Button(text='Kembali ke Menu', position=(-0.7, 0.1), scale=(0.25, 0.08), color=color.azure, enabled=False, on_click=lambda: return_to_menu())
btn_ingame_exit = Button(text='Keluar Game', position=(-0.7, 0.0), scale=(0.25, 0.08), color=color.red, enabled=False, on_click=application.quit)

# Interaction UI
interaction_text = Text(text="[E] Ambil Bola", position=(0, -0.2), origin=(0, 0), scale=1.5, color=color.orange, enabled=False)

# Game Entities
ground = None
player = None
pet = None
ball = None
level_holder = None # Parent for level objects to easily destroy them

def change_pet(direction):
    global selected_pet_index, current_pet_name
    selected_pet_index = (selected_pet_index + direction) % len(pet_types)
    current_pet_name = pet_types[selected_pet_index]
    
    # Update Preview
    pet_preview.model = pet_assets[current_pet_name]['model']
    pet_preview.texture = pet_assets[current_pet_name]['texture']
    
    # Reset Rotation
    pet_preview.rotation = (0, 180, 0)
    
    # Apply Offset (Height/Position correction)
    base_pos = (0, 1.5, 0)
    offset = pet_assets[current_pet_name].get('preview_offset', (0, 0, 0))
    pet_preview.position = (base_pos[0] + offset[0], base_pos[1] + offset[1], base_pos[2] + offset[2])

    # Special scaling for known default shapes to look nice, user models are assumed 1.0
    if pet_assets[current_pet_name]['model'] == 'cube':
        pet_preview.scale = (1, 1, 1)
    else:
        pet_preview.scale = (1, 1, 1) # Reset scale for custom models
        
    desc_text.text = f"{current_pet_name.capitalize()}"
    
    # Simple animation
    pet_preview.animate_rotation_y(pet_preview.rotation_y + 360, duration=0.5)

def start_game():
    global current_state, ground, player, pet, level_holder
    
    # Hide Menu
    title_text.enabled = False
    desc_text.enabled = False
    btn_prev.enabled = False
    btn_next.enabled = False
    btn_start.enabled = False
    pet_preview.enabled = False
    background.enabled = False # Hide menu background
    
    # Setup Game
    current_state = GameState.PLAYING
    
    # Level Holder for easy cleanup
    level_holder = Entity()
    
    # Sky (With realistic texture)
    sky_texture = 'assets/realistic_sky.png' if os.path.exists('assets/realistic_sky.png') else None
    Sky(parent=level_holder, texture=sky_texture)
    
    # Lighting & Atmosphere
    scene.fog_density = 0.02
    scene.fog_color = color.azure
    
    # Add lights if they don't exist (simple check or re-add)
    # Ursina usually has default lights, but let's add nicer ones
    pivot = Entity(parent=level_holder)
    DirectionalLight(parent=pivot, y=2, z=3, shadows=False)
    AmbientLight(parent=level_holder, color=color.rgba(100, 100, 100, 0.5))
    
    # Check for Custom Level / Park Asset
    custom_level = None
    if os.path.exists('assets/level.obj'):
        custom_level = 'assets/level.obj'
        custom_texture = 'assets/level.png' if os.path.exists('assets/level.png') else None
    elif os.path.exists('assets/park.obj'):
        custom_level = 'assets/park.obj'
        custom_texture = 'assets/park.png' if os.path.exists('assets/park.png') else None
        
    if custom_level:
        # Load User's Custom World
        level = Entity(parent=level_holder, model=custom_level, texture=custom_texture, scale=1, collider='mesh')
        # We assume the user's model has a floor. If not, they might fall!
    else:
        # Load Default Procedural World
        
        # Ground
        # Use realistic grass if available
        grass_tex = 'assets/realistic_grass.png' if os.path.exists('assets/realistic_grass.png') else textures['grass']
        
        ground = Entity(parent=level_holder, model='plane', scale=(100, 1, 100), color=color.white, texture=grass_tex, texture_scale=(50, 50), collider='box')
        
        # Walls (Invisible boundaries)
        Entity(parent=level_holder, model='cube', scale=(100, 10, 1), position=(0, 0, 50), collider='box', visible=False)
        Entity(parent=level_holder, model='cube', scale=(100, 10, 1), position=(0, 0, -50), collider='box', visible=False)
        Entity(parent=level_holder, model='cube', scale=(1, 10, 100), position=(50, 0, 0), collider='box', visible=False)
        Entity(parent=level_holder, model='cube', scale=(1, 10, 100), position=(-50, 0, 0), collider='box', visible=False)
    
        # Decor (Simple Trees) on Perimeter
        for i in range(40):
            # Choose a random side: 0=North, 1=South, 2=East, 3=West
            side = random.randint(0, 3)
            if side == 0: # North
                x = random.uniform(-45, 45)
                z = random.uniform(35, 45)
            elif side == 1: # South
                x = random.uniform(-45, 45)
                z = random.uniform(-45, -35)
            elif side == 2: # East
                x = random.uniform(35, 45)
                z = random.uniform(-45, 45)
            else: # West
                x = random.uniform(-45, -35)
                z = random.uniform(-45, 45)
                
            Tree(position=(x, 0, z), parent=level_holder)

    # Player
    player = FirstPersonController(position=(5, 2, -10))
    player.cursor.visible = True 
    player.cursor.texture = textures['ball'] # placeholder/custom cursor
    
    # Fix initial camera clipping & height
    camera.position = (0, 0.8, 0.5)
    
    # 3D BODY CHARACTER (George)
    # Replaces BlockyHuman
    # Scale guess: 0.5? Usually these are decent size.
    player_body = Entity(
        parent=player,
        model='assets/George.obj',
        texture='assets/George_Texture.png',
        position=(0, 0, 0), # Corrected for model offset (Y~3)
        rotation=(0, 0, 0), # Face forward (Flipped per user request)
        scale=0.6, # Corrected scale for ~1m height
        double_sided=True
    )
    
    # Simple Waddle Animation Script
    player_body.walk_timer = 0
    
    def animate_george():
        if not player_body or not player: return
        
        # Check movement via player controller velocity or held keys
        moving = held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']
        
        if moving:
            player_body.walk_timer += time.dt * 10
            # Waddle: Rotate Z (side to side)
            player_body.rotation_z = math.sin(player_body.walk_timer) * 8 # Increased sway
            # Pitch: Lean forward slightly
            player_body.rotation_x = 5 
            # Bob: Move Y slightly
            player_body.y = -3.1 + abs(math.sin(player_body.walk_timer)) * 0.05
        else:
            # Return to idle
            player_body.rotation_z = lerp(player_body.rotation_z, 0, time.dt * 10)
            player_body.rotation_x = lerp(player_body.rotation_x, 0, time.dt * 10) # Reset pitch
            player_body.y = lerp(player_body.y, -3.1, time.dt * 10)

    # Pet
    pet = Pet(current_pet_name, position=(0, 1, 0))
    global mirror_pet
    mirror_pet = None

    # Input info
    Text(parent=level_holder, text="[WASD] Jalan  [L-Click] Lempar  [R-Click] Panggil  [E] Ambil  [G] Besar/Kecil  [M] Mirror  [C] Camera  [ESC] Menu", position=(-0.85, 0.45), scale=1)

def return_to_menu():
    global current_state, player, pet, ball, level_holder, mirror_pet
    
    # 1. Selamatkan Camera dulu! (Unparent)
    camera.parent = scene
    
    # 2. Destroy Game Entities
    if level_holder: destroy(level_holder)
    if player: destroy(player)
    if pet: destroy(pet)
    if mirror_pet: destroy(mirror_pet)
    if ball: destroy(ball)
    
    # Reset Globals
    player = None
    pet = None
    mirror_pet = None
    ball = None
    level_holder = None
    current_state = GameState.MENU
    
    # Restore Camera Transform
    camera.position = (0, 3, -5) # Match new init
    camera.rotation = (15, 0, 0)
    camera.fov = 40 # Reset FOV found in FirstPersonController
    
    # Reset Pet Preview
    pet_preview.position = (0, 1.5, 0)
    pet_preview.rotation = (0, 180, 0)
    
    # Restore UI
    title_text.enabled = True
    desc_text.enabled = True
    btn_prev.enabled = True
    btn_next.enabled = True
    btn_start.enabled = True
    pet_preview.enabled = True
    background.enabled = True
    
    # Hide In-Game Menu
    btn_ingame_menu.enabled = False
    btn_ingame_exit.enabled = False
    interaction_text.enabled = False
    
    mouse.locked = False
    mouse.visible = True

# --- Tree Assets ---
tree_folder = 'assets/trees'
available_trees = []
if os.path.exists(tree_folder):
    for f in os.listdir(tree_folder):
        if f.endswith('.obj'):
            available_trees.append(f'{tree_folder}/{f}')


class Tree(Entity):
    def __init__(self, position=(0,0,0), parent=scene):
        model_name = 'cube'
        texture_name = None
        color_val = color.white
        scale_val = (1, 1, 1)
        
        # Pick a random tree from assets if available
        if available_trees:
            model_name = random.choice(available_trees)
            # Random slight scale variation for realism
            s = random.uniform(0.8, 1.5)
            scale_val = (s, s, s)
            
            # Auto-assign texture based on name (since we stripped materials)
            # Path is like 'assets/trees/Pine_5.obj'
            basename = os.path.basename(model_name).lower()
            
            # Since we fixed the OBJ files with restore_materials.py, 
            # we should NOT manually force a single texture anymore. 
            # The OBJ file handles the multi-material (Bark + Leaves).
            texture_name = None 

            
        # Fallback to legacy check if no new trees found
        elif os.path.exists('assets/tree.obj'):
            model_name = 'assets/tree.obj'
            scale_val = (1, 1, 1)
            color_val = color.white
            if os.path.exists('assets/tree.png'):
                texture_name = 'assets/tree.png'
        
        # Fallback to cube if NOTHING found
        else:
             color_val = color.brown
             scale_val = (1, 4, 1)
        
        super().__init__(
            model=model_name,
            position=position,
            scale=scale_val,
            color=color_val,
            texture=texture_name,
            collider='box',
            parent=parent
        )
        
        # Only add procedural leaves if using default cube
        if model_name == 'cube':
            # Trunk Texture
            self.texture = 'assets/tree_bark.png' 
            self.color = color.white # Reset color to show texture
            
            self.leaves = Entity(
                parent=self,
                model='cube',
                position=(0, 1, 0),
                scale=(2.5, 0.5, 2.5),
                texture='assets/tree_leaves.png',
                color=color.white
            )

class Pet(Entity):
    def __init__(self, pet_type, position):
        super().__init__(
            model=pet_assets[pet_type]['model'],
            position=position,
            scale=(0.8, 0.8, 0.8),
            texture=pet_assets[pet_type]['texture'],
            collider='box',
            double_sided=True
        )
        self.pet_type = pet_type
        self.mouth_pos = pet_assets[pet_type].get('mouth_pos', (0, 0.5, 0.5))
        self.mouth_pos_giant = pet_assets[pet_type].get('mouth_pos_giant', self.mouth_pos) # Fallback to normal if not set
        self.game_y_offset = pet_assets[pet_type].get('game_y_offset', 0)
        self.game_y_offset_giant = pet_assets[pet_type].get('game_y_offset_giant', self.game_y_offset * 2.5) # Default to proprotional scaling if not set
        self.speed = 4
        self.target = None # Can be player or ball
        
        # Add a head for cuteness ONLY if it's a default cube model
        if self.model.name == 'cube':
            self.head = Entity(parent=self, model='cube', scale=(0.8, 0.8, 0.8), position=(0, 0.5, 0), texture=self.texture)
        
        # Animations
        self.is_jumping = False
        self.walk_timer = 0


    def update(self):
        if self.target:
            self.look_at_2d(self.target.position, 'y')
            dist = distance(self.position, self.target.position)
            
            # Dynamic stopping distance
            # If target is player: stop at 4m (Personal Space)
            # If target is ball: stop at 1m (Close enough to pickup)
            stop_dist = 4 if self.target == player else 1
            
            if dist > stop_dist:
                self.position += self.forward * self.speed * time.dt
                
                # PROCEDURAL ANIMATION
                self.walk_timer += time.dt * 15 # Speed of animation
                
                # Scale Height Scaling:
                # Interpolate between Normal Offset and Giant Offset
                # Normal scale = 0.8, Giant scale = 2.5
                # t = 0 when scale is 0.8, t = 1 when scale is 2.5
                t = clamp((self.scale_x - 0.8) / (2.5 - 0.8), 0, 1)
                
                current_y_offset = lerp(self.game_y_offset, self.game_y_offset_giant, t)
                
                # Hop (Y bobbing)
                # sin returns -1 to 1. Abs makes it 0 to 1 (hopping).
                self.y = 0.4 + current_y_offset + abs(math.sin(self.walk_timer)) * 0.3 
                
                # Waddle (Z rotation - rocking side to side)
                self.rotation_z = math.sin(self.walk_timer) * 8
                
                # Pitch (X rotation - lean forward slightly)
            else:
                t = clamp((self.scale_x - 0.8) / (2.5 - 0.8), 0, 1)
                current_y_offset = lerp(self.game_y_offset, self.game_y_offset_giant, t)

                self.y = 0.4 + current_y_offset
                self.rotation_z = lerp(self.rotation_z, 0, time.dt * 10) # Smoothly return to 0
                self.walk_timer = 0

                
            # Fetch mechanic
            if self.target == ball and dist < 2:
                ball.parent = self # Pick up ball
                ball.position = self.mouth_pos
                # FIX: Adjust ball scale inverse to pet scale so it doesn't grow
                # Default ball scale is 0.25 (User requested smaller)
                ball.scale = 0.25 / self.scale_x
                self.target = player # Return to player
        else:
            # Follow player by default
            self.target = player

class Ball(Entity):
    def __init__(self, position=(0,0,0), velocity=(0,0,0)):
        super().__init__(
            model='sphere',
            scale=0.25, # Smaller ball
            color=color.red,
            collider='sphere',
            texture=textures['ball'],
            position=position
        )
        self.velocity = Vec3(velocity)
        self.friction = 2.0
        self.gravity = 25

    def update(self):
        # Physics only if free (not being carried)
        if self.parent != scene:
            return

        # Apply Gravity
        self.velocity.y -= self.gravity * time.dt
        
        # Apply Velocity
        self.position += self.velocity * time.dt
        
        # Floor Collision
        if self.y < 0.25: 
            self.y = 0.25
            self.velocity.y *= -0.6 # Bounce
            
            if abs(self.velocity.y) < 1:
                self.velocity.y = 0
            
            # Ground Friction
            self.velocity.x -= self.velocity.x * self.friction * time.dt
            self.velocity.z -= self.velocity.z * self.friction * time.dt
        
        # Rolling Rotation
        self.rotation_x += self.velocity.z * 15 * time.dt * 10
        self.rotation_z -= self.velocity.x * 15 * time.dt * 10
        
        # Cleanup
        if self.y < -50:
            destroy(self)

class BlockyHuman(Entity):
    def __init__(self, parent=None, position=(0,0,0)):
        super().__init__(parent=parent, position=position)
        
        # Skin Color
        skin_color = color.rgb(255, 200, 150)
        shirt_color = color.azure
        pant_color = color.dark_gray
        
        # Head
        self.head = Entity(parent=self, model='cube', scale=(0.4, 0.4, 0.4), position=(0, 1.7, 0), color=skin_color)
        
        # Body (Torso)
        self.body = Entity(parent=self, model='cube', scale=(0.5, 0.7, 0.3), position=(0, 1.15, 0), color=shirt_color)
        
        # Arms
        self.arm_l = Entity(parent=self, model='cube', scale=(0.15, 0.7, 0.15), position=(-0.33, 1.15, 0), color=skin_color)
        self.arm_r = Entity(parent=self, model='cube', scale=(0.15, 0.7, 0.15), position=(0.33, 1.15, 0), color=skin_color)
        
        # Legs
        self.leg_l = Entity(parent=self, model='cube', scale=(0.2, 0.75, 0.2), position=(-0.15, 0.375, 0), color=pant_color)
        self.leg_r = Entity(parent=self, model='cube', scale=(0.2, 0.75, 0.2), position=(0.15, 0.375, 0), color=pant_color)



def input(key):
    global current_state, player, pet, ball, level_holder, is_paused, mirror_pet
    
    if key == 'escape':
        if current_state == GameState.PLAYING:
            mouse.locked = not mouse.locked
            mouse.visible = not mouse.locked
            
            is_paused = not mouse.locked
            btn_ingame_menu.enabled = is_paused
            btn_ingame_exit.enabled = is_paused

    if current_state == GameState.MENU:
        # Rotate preview with mouse drag (simple approximation using keys for now or scroll)
        pass

    if current_state == GameState.PLAYING:
        if key == 'left mouse down':
            # Throw ball
            if ball:
                destroy(ball) # Reset ball
                
            ball = Ball(position=camera.world_position + camera.forward * 2, velocity=camera.forward * 20 + Vec3(0, 5, 0))
            
            if pet:
                pet.target = ball

        if key == 'right mouse down':
            # Call pet
            if pet:
                pet.target = player
                if ball and ball.parent == pet:
                    # Drop ball
                    ball.parent = scene
                    ball.scale = 0.25 # Reset scale
                    ball.y = 0.5

        if key == 'e':
            if interaction_text.enabled:
                if ball: destroy(ball)
                ball = None
                interaction_text.enabled = False
                # Visual feedback?
                # print("Bola diambil")

        if key == 'c':
            # Toggle FPP/TPP
            # Check current Z position of camera to determine mode
            # Standard FPP is roughly (0,0,0) or (0,0,0) relative to pivot
            # TPP target: (0, 1, -4)
            
            if abs(camera.z) < 1: # Currently FPP
                camera.animate_position((0, 1, -4), duration=0.2, curve=curve.out_sine)
            else: # Currently TPP
                camera.animate_position((0, 0.5, 0.5), duration=0.2, curve=curve.out_sine) # High & Forward

        if key == 'g':
            # Toggle Pet Size
            if pet:
                # Check current scale (approximate)
                if pet.scale.x < 1.0:
                    # Grow to Giant
                    pet.animate_scale((2.5, 2.5, 2.5), duration=0.5, curve=curve.out_bounce)
                else:
                    # Shrink to Normal
                    pet.animate_scale((0.8, 0.8, 0.8), duration=0.5, curve=curve.out_bounce)

        if key == 'm':
            # Toggle Mirror
            if mirror_pet:
                destroy(mirror_pet)
                mirror_pet = None
            elif pet:
                # Spawn Mirror (Ghost)
                mirror_pet = Entity(
                    model=pet.model.name if hasattr(pet.model, 'name') else 'cube',
                    texture=pet.texture,
                    scale=pet.scale,
                    alpha=0.5, # Transparent
                    color=color.lime # Ghostly color
                )
                print("Mirror activated")

def update():
    global mirror_pet, pet, interaction_text

    if current_state == GameState.PLAYING:
        # Update Mirror
        if mirror_pet and pet:
            # REFLECTION MATH: x' = -x
            mirror_pet.position = (-pet.x, pet.y, pet.z)
            # REFLECTION ROTATION: y' = -y (Mirrored facing)
            mirror_pet.rotation = (pet.rotation_x, -pet.rotation_y, -pet.rotation_z)
            # Sync Scale
            mirror_pet.scale = pet.scale

        # DEBUG: Adjust Ball Position Logic
        if pet and ball and ball.parent == pet:
            # Dynamic Ball Scaling & Position Update
            target_scale_scale = 0.25 / pet.scale.x
            ball.scale = (target_scale_scale, target_scale_scale, target_scale_scale)
            
            # Determine which mode we are in
            is_giant = pet.scale.x > 1.5
            
            current_mouth_pos = pet.mouth_pos_giant if is_giant else pet.mouth_pos
            ball.position = current_mouth_pos # Snap continuously
            
            # Calibration
            speed = time.dt * 0.5 
            x, y, z = current_mouth_pos
            changed = False
            
            if held_keys['up arrow']: 
                y += speed; changed = True
            if held_keys['down arrow']: 
                y -= speed; changed = True
            if held_keys['right arrow']: 
                z += speed; changed = True
            if held_keys['left arrow']: 
                z -= speed; changed = True
            
            if changed:
                new_pos = (x, y, z)
                if is_giant:
                    pet.mouth_pos_giant = new_pos
                    print(f"ADJUSTED GIANT Mouth Pos ({pet.pet_type}): {new_pos}")
                else:
                    pet.mouth_pos = new_pos
                    print(f"ADJUSTED NORMAL Mouth Pos ({pet.pet_type}): {new_pos}")

        # Animate George
        try:
             animate_george()
        except:
             pass

        # Check interaction distance
        if pet and player and ball:
            # Show text if close AND pet has ball
            if ball.parent == pet and distance(player.position, pet.position) < 3.0:
                interaction_text.enabled = True
            else:
                interaction_text.enabled = False
        else:
            interaction_text.enabled = False

    if current_state == GameState.MENU:
        # Rotate preview if mouse held
        if mouse.left:
            pet_preview.rotation_y -= mouse.velocity.x * 200 # Invert to match drag
            pet_preview.rotation_x -= mouse.velocity.y * 200 # Re-invert per request

app.run()
