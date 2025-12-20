import tkinter as tk
import math
import random
from PIL import Image, ImageTk

class DinoSpriteUTS:
    def __init__(self, root):
        self.root = root
        self.root.title("UTS Grafika Komputer - 2D Game Engine")
        self.canvas = tk.Canvas(root, width=800, height=400, bg="white")
        self.canvas.pack()

        # --- MATERI 3: DATA POLIGON (REPRESENTASI OBJEK) ---
        self.obs_polygon_data = {
            1: [(-5, 0), (5, 0), (5, -40), (-5, -40)],  # Segi empat (Kaktus)
            2: [(-8, 0), (8, 0), (8, -30), (0, -35), (-8, -30)], # Poligon lancip
            3: [(-15, 0), (0, 5), (15, 0), (0, -5)] # Poligon datar (Duri)
        }

        self.raw_sprites = {}
        self.load_sprites_raw()
        self.current_frame = 0
        self.state = "RUN"
        self.anim_counter = 0

        # --- MATERI 4: TRANSFORMASI GEOMETRIS 2D ---
        self.base_height = 80            # Tinggi dasar untuk perhitungan Skala
        self.pos_x, self.pos_y = 100, 310 # Translasi posisi awal
        self.angle = 0                   # Rotasi awal
        self.scale_factor = 1.0          # Skala awal
        self.is_flipped = False          # Refleksi (Pencerminan)

        # LOGIKA KECEPATAN (AKSELERASI)
        self.game_speed = 7.0        
        self.max_speed = 25.0        
        self.acceleration = 0.010    # Kecepatan meningkat 0.01 setiap frame
        
        self.vel_y = 0
        self.is_jumping = False
        self.space_pressed = False
        self.move_speed = 6
        self.game_over = False
        self.distance_traveled = 0.0
        self.item_score = 0
        
        self.active_obstacles = []
        self.spawn_obstacle_group()
        self.item_x, self.item_y = 1200, 250
        self.item_radius = 12

        # Input Bindings
        self.root.bind("<KeyPress-space>", self.on_space_press)
        self.root.bind("<KeyRelease-space>", self.on_space_release)
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<s>", self.toggle_scale)
        
        self.game_loop()

    def load_sprites_raw(self):
        paths = {
            "RUN":  {"path": "images/Sprites/Run.png",  "steps": 8},
            "JUMP": {"path": "images/Sprites/Jump.png", "steps": 9}
        }
        try:
            for state, info in paths.items():
                full_img = Image.open(info["path"]).convert("RGBA")
                sw, sh = full_img.size
                w = sw // info["steps"]
                self.raw_sprites[state] = [full_img.crop((i*w, 0, (i+1)*w, sh)) for i in range(info["steps"])]
        except:
            print("Peringatan: Folder/File gambar tidak ditemukan. Gunakan placeholder.")
            self.raw_sprites = None

    def apply_transformations(self, pil_image):
        """Implementasi Materi 4: Transformasi (Scale, Rotate, Flip)"""
        img = pil_image
        # 1. Skala
        new_size = (int(self.base_height * self.scale_factor), int(self.base_height * self.scale_factor))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        # 2. Rotasi
        if self.angle != 0: 
            img = img.rotate(self.angle, expand=True)
        # 3. Refleksi
        if self.is_flipped: 
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        return ImageTk.PhotoImage(img)

    def on_space_press(self, event):
        if not self.is_jumping:
            self.vel_y, self.is_jumping, self.state, self.current_frame = -14, True, "JUMP", 0
        self.space_pressed = True

    def on_space_release(self, event): self.space_pressed = False

    def move_left(self, event):
        self.pos_x -= self.move_speed
        self.is_flipped = True # Refleksi ke kiri

    def move_right(self, event):
        self.pos_x += self.move_speed
        self.is_flipped = False # Refleksi ke kanan (normal)

    def toggle_scale(self, event):
        self.scale_factor = 1.5 if self.scale_factor == 1.0 else 1.0

    # --- MATERI 1: ALGORITMA BRESENHAM (GARIS) ---
    def draw_line(self, x0, y0, x1, y1, color):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx - dy
        while True:
            self.canvas.create_line(x0, y0, x0+1, y0, fill=color)
            if x0 == x1 and y0 == y1: break
            e2 = 2 * err
            if e2 > -dy: err -= dy; x0 += sx
            if e2 < dx: err += dx; y0 += sy

    # --- MATERI 2: ALGORITMA MIDPOINT (LINGKARAN) ---
    def draw_midpoint_circle(self, xc, yc, r, color):
        if r <= 0: return
        x, y, p = 0, r, 1 - r
        while x <= y:
            # Menggambar 8 titik simetris
            pts = [(xc+x, yc+y), (xc-x, yc+y), (xc+x, yc-y), (xc-x, yc-y),
                   (xc+y, yc+x), (xc-y, yc+x), (xc+y, yc-x), (xc-y, yc-x)]
            for px, py in pts:
                self.canvas.create_line(px, py, px+1, py, fill=color)
            x += 1
            if p < 0: p = p + 2*x + 1
            else: y -= 1; p = p + 2*(x - y) + 1

    def draw_enhanced_coin(self, xc, yc, r):
        self.draw_midpoint_circle(xc, yc, r, "#DAA520") # Outer
        self.draw_midpoint_circle(xc, yc, r-2, "#FFD700") # Inner
        self.draw_midpoint_circle(xc, yc, 2, "white") # Shine

    def spawn_obstacle_group(self):
        for i in range(random.randint(1, 2)):
            self.active_obstacles.append([900 + (i * random.randint(150, 300)), random.randint(1, 3)])

    def game_loop(self):
        if self.game_over:
            total_score = int(self.distance_traveled) + self.item_score
            self.canvas.create_text(400, 200, text=f"GAME OVER\nSkor: {total_score}", 
                                   font=("Arial", 25, "bold"), fill="red", justify="center")
            return

        self.canvas.delete("all")

        # Update Kecepatan (Makin lama makin cepat)
        if self.game_speed < self.max_speed: 
            self.game_speed += self.acceleration
            
        self.distance_traveled += self.game_speed / 10
        self.draw_line(0, 350, 800, 350, "black") # Tanah (Bresenham)

        # --- LOGIKA ANCHOR BAWAH (Agar tidak tenggelam saat membesar) ---
        current_height = self.base_height * self.scale_factor
        offset_y = (current_height - self.base_height) / 2
        render_y = self.pos_y - offset_y

        # Update Lonjakan (Translasi Y)
        if self.is_jumping:
            gravity = 0.6 if self.space_pressed and self.vel_y < 0 else 1.2
            self.pos_y += self.vel_y
            self.vel_y += gravity
            self.angle = (self.angle + 8) % 360 # Rotasi saat melompat
            if self.pos_y >= 310:
                self.pos_y, self.is_jumping, self.state, self.angle = 310, False, "RUN", 0

        # Animasi Sprite
        if self.raw_sprites:
            self.anim_counter += 1
            anim_delay = max(1, 6 - int(self.game_speed // 4)) 
            if self.anim_counter % anim_delay == 0:
                self.current_frame = (self.current_frame + 1) % len(self.raw_sprites[self.state])
            
            raw_img = self.raw_sprites[self.state][self.current_frame % len(self.raw_sprites[self.state])]
            self.tk_image = self.apply_transformations(raw_img)
            self.canvas.create_image(self.pos_x, render_y, image=self.tk_image)

        # Rintangan (Materi 3: Poligon & Materi 1: Bresenham)
        char_hit = 30 * self.scale_factor
        for obs in self.active_obstacles:
            obs[0] -= self.game_speed 
            base = self.obs_polygon_data[obs[1]]
            ty = 350 if obs[1] < 3 else 270 # Posisi y rintangan
            for i in range(len(base)):
                p1 = (base[i][0] + obs[0], base[i][1] + ty)
                p2 = (base[(i+1)%len(base)][0] + obs[0], base[(i+1)%len(base)][1] + ty)
                self.draw_line(p1[0], p1[1], p2[0], p2[1], "green")
            
            if (abs(self.pos_x - obs[0]) < char_hit) and (abs(render_y - ty + 20) < char_hit):
                self.game_over = True

        self.active_obstacles = [o for o in self.active_obstacles if o[0] > -100]
        if not self.active_obstacles: self.spawn_obstacle_group()

        # Koin (Materi 2: Midpoint)
        self.item_x -= self.game_speed
        if self.item_x < -50: 
            self.item_x, self.item_y = random.randint(900, 1500), random.randint(200, 280)
        self.draw_enhanced_coin(self.item_x, self.item_y, self.item_radius)
        
        # Hitbox (Euclidean)
        if math.sqrt((self.pos_x - self.item_x)**2 + (render_y - self.item_y)**2) < (char_hit + self.item_radius):
            self.item_score += 100
            self.item_x = -200

        # UI Overlay
        self.canvas.create_text(700, 30, text=f"Speed: {self.game_speed:.2f}", font=("Arial", 10))
        self.canvas.create_text(100, 30, text=f"Jarak: {int(self.distance_traveled)}m", font=("Arial", 10, "bold"))
        self.canvas.create_text(100, 50, text=f"Koin: {self.item_score}", font=("Arial", 10, "bold"), fill="#DAA520")

        self.root.after(20, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    game = DinoSpriteUTS(root)
    root.mainloop()