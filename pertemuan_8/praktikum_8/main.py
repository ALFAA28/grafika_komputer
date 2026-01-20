from ursina import *
# from ursina.prefabs.trail_renderer import TrailRenderer  <-- HAPUS INI KARENA SUDAH TIDAK DIPAKAI
import random

app = Ursina()

# --- 1. SETUP WINDOW ---
window.title = "Tony's Valorant - No Trail"
window.borderless = False
window.exit_button.visible = False
window.fps_counter.enabled = True
window.fullscreen = False

# --- 2. CROSSHAIR ---
mouse.visible = False
crosshair = Entity(parent=camera.ui, model='circle', scale=0.005, color=color.red)

# --- 3. MAP / LINGKUNGAN ---
ground = Entity(
    model='plane',
    scale=200,
    texture='white_cube',
    texture_scale=(100, 100),
    color=color.rgb(50, 50, 60),
    collider='box',
    position=(0, 0, 0),
    name='ground',
    ignore_collision=False 
)

mouse.traverse_target = ground

def create_walls_and_props():
    wall_color = color.rgb(200, 210, 220)       
    radianite_color = color.rgb(0, 255, 150)    
    wood_color = color.rgb(255, 140, 50)        
    dark_cover = color.rgb(40, 40, 50)          

    map_objects = []

    # --- A. BATAS LUAR ---
    map_objects.extend([
        Entity(model='cube', scale=(100, 20, 2), position=(0, 10, 50), color=wall_color, collider='box', texture='white_cube'),
        Entity(model='cube', scale=(100, 20, 2), position=(0, 10, -50), color=wall_color, collider='box', texture='white_cube'),
        Entity(model='cube', scale=(2, 20, 100), position=(50, 10, 0), color=wall_color, collider='box', texture='white_cube'),
        Entity(model='cube', scale=(2, 20, 100), position=(-50, 10, 0), color=wall_color, collider='box', texture='white_cube'),
    ])

    # --- B. AREA TENGAH ---
    map_objects.append(Entity(model='cube', position=(0, 5, 0), scale=(10, 10, 10), color=dark_cover, texture='white_cube', collider='box'))
    map_objects.append(Entity(model='cube', position=(-15, 4, 0), scale=(2, 8, 20), color=wall_color, texture='white_cube', collider='box'))

    # --- C. LORONG KIRI ---
    map_objects.extend([
        Entity(model='cube', position=(-35, 4, 20), scale=(15, 8, 2), color=wall_color, texture='white_cube', collider='box'),
        Entity(model='cube', position=(-35, 4, -20), scale=(15, 8, 2), color=wall_color, texture='white_cube', collider='box'),
        Entity(model='cube', position=(-40, 2, 0), scale=(4, 4, 4), color=radianite_color, texture='white_cube', collider='box'),
        Entity(model='cube', position=(-40, 6, 0), scale=(3.8, 4, 3.8), color=radianite_color, texture='white_cube', collider='box'), 
    ])

    # --- D. LORONG KANAN ---
    map_objects.extend([
        Entity(model='cube', position=(30, 2.5, 10), scale=(4, 5, 15), color=wood_color, texture='white_cube', collider='box'),
        Entity(model='cube', position=(35, 4, -20), scale=(2, 8, 15), color=wall_color, texture='white_cube', collider='box'),
        Entity(model='cube', position=(28, 4, -27), scale=(15, 8, 2), color=wall_color, texture='white_cube', collider='box'),
    ])

    # --- E. AREA SPAWN MUSUH ---
    map_objects.extend([
        Entity(model='cube', position=(10, 3, 40), scale=(15, 6, 2), color=wall_color, texture='white_cube', collider='box'),
        Entity(model='cube', position=(-10, 3, 40), scale=(15, 6, 2), color=wall_color, texture='white_cube', collider='box'),
        Entity(model='cube', position=(0, 2, 35), scale=(5, 4, 2), color=wood_color, texture='white_cube', collider='box'),
    ])

    Sky(color=color.rgb(135, 206, 235))

create_walls_and_props()

# --- 4. PLAYER (TONY) ---
tony = Entity(
    model='George.obj', 
    texture='George_Texture.png',
    scale=(1, 2, 1), 
    y=1,
    collider='box',
    name='tony',
    position=(0, 1, -40) 
)
tony.hp = 100
tony.fire_rate = 0.15 
tony.fire_cooldown = 0
tony.speed = 15 

# Senjata 
gun = Entity(
    parent=tony,
    model='pmx_obj.obj',
    texture='pmx_BaseColor.png',
    scale=(5), 
    position=(-7.5, 3, 1.5),
    rotation=(0, 180, 0),
    name='gun'
)

# --- 5. KAMERA (Edit di sini) ---
# Vec3(Kanan/Kiri, Tinggi, Maju/Mundur)
camera_offset = Vec3(0, 30, -35)  # Lebih rendah dan lebih dekat
camera.position = tony.position + camera_offset
camera.rotation = (30, 0, 0)     # Menunduk 45 derajat (sebelumnya 55)

# --- 6. MUSUH ---
enemies = []
def spawn_bot(pos):
    bot = Entity(
        model='Mike.obj', 
        texture='Mike_Texture.png',
        scale=(1, 2, 1),
        position=pos,
        name='enemy'
    )
    
    # --- PERBAIKAN HITBOX MENYELURUH ---
    # 1. Kita tentukan ukuran kotak (size) agar tinggi sesuai scale (2)
    # 2. Kita naikkan pusat kotak (center) ke arah Y agar menutupi kepala
    # size=(lebar_x, tinggi_y, lebar_z)
    # center=(0, tinggi_y/2, 0) -> Jika pivot Mike ada di kaki
    
    hitbox_size = (10, 30, 10) # Membuat hitbox sedikit lebih lebar & tinggi dari visual
    hitbox_center = (0, 1.25, 0)  # Menggeser kotak ke atas agar menutupi seluruh badan
    
    bot.collider = BoxCollider(bot, center=hitbox_center, size=hitbox_size)
    
    # Visual indikator darah
    bot.hp = 50
    bot.health_bar = Entity(
        parent=bot, 
        model='quad', 
        color=color.green, 
        width=1, 
        height=0.1, 
        y=2.5, # Naikkan sedikit agar tidak menempel di kepala
        billboard=True
    )
    enemies.append(bot)
    
spawn_bot((-40, 1, 40)) 
spawn_bot((40, 1, 40))  
spawn_bot((0, 1, 25))   
spawn_bot((35, 1, 0))   
spawn_bot((-30, 1, 0))  

# --- 7. UI ---
info_text = Text(text='', position=(-0.85, 0.45), scale=1.5, background=True)

# --- 8. SISTEM PELURU (TANPA BAYANGAN/TRAIL) ---
class Bullet(Entity):
    def __init__(self, position, direction):
        super().__init__(
            model='sphere',
            scale=0.4,          # Besar
            color=color.red,    # Merah
            position=position,
            collider=None 
        )
        self.direction = direction
        self.speed = 100 
        self.destroy_after = 2 
        self.lt = 0 
        # self.frames_alive = 0  <-- Tidak butuh ini lagi
        # self.trail = None      <-- Tidak butuh trail lagi
        self.safe_time = 0.05 

    def update(self):
        self.lt += time.dt
        # self.frames_alive += 1 <-- Hapus logika trail
        
        # BAGIAN TRAIL RENDERER SUDAH DIHAPUS

        dist = self.speed * time.dt
        
        if self.lt > self.safe_time:
            hit_info = raycast(self.position, self.direction, distance=dist, ignore=(self, tony, gun))
            
            if hit_info.hit:
                self.position = hit_info.world_point 
                
                if hit_info.entity in enemies:
                    bot = hit_info.entity
                    bot.hp -= 25
                    bot.blink(color.red, duration=0.1)
                    if bot.hp > 0:
                        bot.health_bar.scale_x = bot.hp / 50
                    else:
                        if bot in enemies: enemies.remove(bot)
                        destroy(bot)
                
                destroy(self) 
                return

        self.position += self.direction * dist
        
        if self.lt > self.destroy_after:
            destroy(self)

# --- 9. FUNGSI SHOOT ---
def shoot():
    if tony.fire_cooldown > 0:
        return

    # 1. Hitung Posisi Moncong (Sesuai settingan offset Anda)
    offset_maju  = -0.1
    offset_kanan = -1.9
    offset_atas  = 0.1

    muzzle_pos = (gun.world_position 
                  + (gun.forward * offset_maju) 
                  + (gun.right   * offset_kanan) 
                  + (gun.up      * offset_atas))

    # 2. Logika Penentuan Arah Peluru (PENTING)
    if mouse.world_point:
        # Peluru akan mengarah tepat ke titik kursor di tanah/objek
        direction = (mouse.world_point - muzzle_pos).normalized()
    else:
        # Jika mouse tidak menyentuh objek (mengarahkan ke langit), gunakan arah hadap laras
        direction = gun.forward

    # 3. Spawn Peluru
    Bullet(position=muzzle_pos, direction=direction)
    
    camera.shake(duration=0.02, magnitude=0.02)
    tony.fire_cooldown = tony.fire_rate

# --- 10. GAME LOOP ---
def update():
    dx = (held_keys['d'] - held_keys['a']) * time.dt * tony.speed
    dz = (held_keys['w'] - held_keys['s']) * time.dt * tony.speed
    
    if dx != 0:
        direction_x = Vec3(dx, 0, 0).normalized()
        hit_x = raycast(tony.position + Vec3(0, 0.5, 0), direction_x, distance=0.6 + abs(dx), ignore=(tony, gun, ground))
        if not hit_x.hit: tony.x += dx

    if dz != 0:
        direction_z = Vec3(0, 0, dz).normalized()
        hit_z = raycast(tony.position + Vec3(0, 0.5, 0), direction_z, distance=0.6 + abs(dz), ignore=(tony, gun, ground))
        if not hit_z.hit: tony.z += dz

    if mouse.world_point:
        target_point = mouse.world_point
        target_point.y = tony.y 
        tony.look_at(target_point)

    camera.position = lerp(camera.position, tony.position + camera_offset, time.dt * 10)

    if tony.fire_cooldown > 0:
        tony.fire_cooldown -= time.dt

    if held_keys['left mouse']:
        shoot()

    status = "WINNER!" if len(enemies) == 0 else f"Bots Left: {len(enemies)}"
    info_text.text = f'HP: {tony.hp} | {status}'
    info_text.color = color.green if len(enemies) == 0 else color.white
    
    if mouse.position:
        crosshair.position = mouse.position

app.run()