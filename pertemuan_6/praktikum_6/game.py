import turtle
import math
import numpy as np
import os 
import time 

# -----------------------------------------------------
# KONSTANTA & INISIALISASI STATUS GAME
# -----------------------------------------------------
# --- PASTIKAN FILE INI ADA DI FOLDER YANG SAMA ---
IMAGE_NORMAL = "__Idle.gif"
IMAGE_MIRROR = "mirror__Idle.gif"
IMAGE_SCALED = "scale__Idle.gif"
IMAGE_SCALED_MIRROR = "mirror_scale__Idle.gif" 
IMAGE_SWORD = "sword.gif" # FILE GIF PEDANG
# -------------------------------------------------

P_global = np.array([0.0, 0.0, 1.0])
DASH_DISTANCE = 15.0
SCALE_FACTOR = 1.5
ROTATION_AMOUNT = 60.0 # Jumlah rotasi per toggle

# Asumsi Tinggi: Nilai ini HARUS disesuaikan
BASE_HEIGHT = 30.0 
SCALE_Y_OFFSET = (BASE_HEIGHT * SCALE_FACTOR - BASE_HEIGHT) / 2 

# Pedang
SWORD_LENGTH = 40 
SWORD_OFFSET_X = 5 
PLAYER_HAND_OFFSET_Y = -10.0 

# Karena kita menggunakan GIF, kita perlu tahu tinggi pedang GIF
SWORD_GIF_HEIGHT = 40 
SWORD_HANDLE_TO_CENTER = -SWORD_GIF_HEIGHT / 2 

# -----------------------------------------------------
# FUNGSI TRANSFORMASI MATRIKS HOMOGEN (3x3)
# -----------------------------------------------------

def transform_point(M, P):
    """Menerapkan transformasi matriks M pada titik P (Homogen)."""
    P_new = M @ P
    return P_new

def get_translation_matrix(tx, ty):
    return np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])

def get_rotation_matrix(angle_deg):
    """Mendapatkan Matriks Rotasi Z (2D) - Sesuai gambar"""
    angle_rad = math.radians(angle_deg)
    c, s = math.cos(angle_rad), math.sin(angle_rad)
    return np.array([
        [c, -s, 0], 
        [s, c, 0], 
        [0, 0, 1]
    ])

def get_reflection_y_matrix():
    """Matriks Refleksi terhadap sumbu Y (Flip Horizontal)"""
    return np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])

# -----------------------------------------------------
# KELAS SWORD
# -----------------------------------------------------

class Sword:
    def __init__(self, screen, player_t):
        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.speed(0)
        self.t.color("gray", "lightgray")
        self.t.pensize(2)
        
        try:
            self.t.shape(IMAGE_SWORD) 
        except turtle.TurtleGraphicsError:
            self.t.shape("square")
            self.t.shapesize(stretch_wid=SWORD_LENGTH/20, stretch_len=1)
        
        self.t.setheading(0)
        self.player_t = player_t
        
    def follow_player(self, player_pos, is_mirrored):
        """
        Memposisikan pedang relatif terhadap pemain, menempatkan pusat rotasi 
        (pegangan pedang) di samping karakter.
        Pedang akan mengikuti rotasi karakter (player_t.heading()).
        """
        
        self.t.setheading(self.player_t.heading()) 
        
        SWORD_HANDLE_TO_CENTER = -SWORD_GIF_HEIGHT / 2
        
        if is_mirrored:
            offset_x = -SWORD_OFFSET_X
            P_relative_local = np.array([offset_x, PLAYER_HAND_OFFSET_Y + SWORD_HANDLE_TO_CENTER, 1]) 
            # Penyesuaian heading: -90 derajat agar pedang mengarah ke depan saat dicerminkan
            sword_heading_adjustment = -90 
        else:
            offset_x = SWORD_OFFSET_X
            P_relative_local = np.array([offset_x, PLAYER_HAND_OFFSET_Y + SWORD_HANDLE_TO_CENTER, 1]) 
            # Penyesuaian heading: +90 derajat agar pedang mengarah ke depan saat normal
            sword_heading_adjustment = 90
        
        self.t.penup()
        
        # Transformasi posisi: Translasi (Posisi Karakter) * Rotasi (Sudut Karakter) * Posisi Relatif
        M_T = get_translation_matrix(player_pos[0], player_pos[1]) 
        M_R = get_rotation_matrix(self.player_t.heading()) # Menggunakan matriks untuk Rotasi
        
        # Rotasi (M_R) harus di tengah, tetapi karena kita hanya peduli posisi relatif, 
        # kita anggap titik pivot adalah posisi karakter.
        # Jika angle=0, M_R adalah matriks identitas.
        # P_world = transform_point(M_T @ M_R, P_relative_local) 
        
        # Mengingat posisi karakter sudah dirotasi di do_rotate(), kita hanya perlu Translasi dan Rotasi Heading.
        # Kita hanya memerlukan Translasi ke posisi karakter, dan posisi relatif P_relative_local
        # sudah dihitung relatif terhadap pusat karakter.
        
        # Cara sederhana untuk menghitung posisi dunia P_world:
        # P_world = M_T * R_heading * P_relative_local
        # Karena karakter adalah satu entitas dan sudah di-rotate, kita hanya perlu menempatkan pedang
        # di posisi yang benar *setelah* karakter dirotasi
        
        # Transformasi posisi: Rotasi (Sudut Karakter) * Posisi Relatif, lalu Translasi
        P_rotated_relative = transform_point(M_R, P_relative_local)
        P_world = transform_point(M_T, P_rotated_relative) 
        
        self.t.goto(P_world[0], P_world[1])
        
        # Sudut akhir pedang = Sudut Karakter + Penyesuaian Lokal
        sword_heading = self.player_t.heading() + sword_heading_adjustment
        self.t.setheading(sword_heading)
        self.t.showturtle()
        
    def hide(self):
        self.t.hideturtle()


# -----------------------------------------------------
# KELAS PLAYER (Menggunakan Gambar)
# -----------------------------------------------------

class Player:
    def __init__(self, t, screen):
        self.t = t
        self.screen = screen
        self.pos = np.array([0.0, 0.0, 1.0])
        self.current_image = IMAGE_NORMAL
        self.angle = 0.0 
        self.is_mirrored = False 
        self.is_scaled = False   
        
        self._load_images() # Memuat gambar SEBELUM membuat instance Sword
        self.sword = Sword(screen, t) 
        
        self.is_rotated_60 = False 
        self.base_angle = 0.0 
        
        self.pivot_marker = turtle.Turtle()
        self.pivot_marker.shape("circle")
        self.pivot_marker.color("red")
        self.pivot_marker.shapesize(0.3)
        self.pivot_marker.penup()
        self.pivot_marker.hideturtle()
        
        
    def _load_images(self):
        """Memuat gambar .gif ke dalam Turtle Screen."""
        all_images = {IMAGE_NORMAL, IMAGE_MIRROR, IMAGE_SCALED, IMAGE_SCALED_MIRROR, IMAGE_SWORD}
        
        if "square" not in self.screen.getshapes():
            self.screen.addshape("square")
            
        for img in all_images: 
            if os.path.exists(img):
                # Ini memastikan IMAGE_SWORD dimuat ke dalam Screen
                self.screen.addshape(img) 
            else:
                print(f"ERROR: File gambar '{img}' tidak ditemukan.")
                
                if img == IMAGE_SWORD:
                    print(f"PERINGATAN: File '{IMAGE_SWORD}' tidak ditemukan. Sword akan menggunakan shape 'square' default.")
                else:
                    print("Program dihentikan karena gambar karakter utama tidak ditemukan.")
                    self.screen.bye()
                    raise FileNotFoundError(f"File {img} tidak ditemukan.")

    def redraw(self):
        """Menggambar ulang karakter dengan gambar, posisi, dan pedang yang sesuai."""
        
        self.t.clear()
        
        if self.is_scaled and self.is_mirrored:
            img_to_use = IMAGE_SCALED_MIRROR
        elif self.is_scaled:
            img_to_use = IMAGE_SCALED
        elif self.is_mirrored:
            img_to_use = IMAGE_MIRROR
        else:
            img_to_use = IMAGE_NORMAL
            
        self.t.setheading(self.angle)
        self.t.shape(img_to_use)
        
        self.t.penup()
        self.t.goto(self.pos[0], self.pos[1])
        self.t.showturtle()
        
        # Gambar Pedang (Menimpa Karakter)
        self.sword.follow_player(self.pos, self.is_mirrored) 
        
        # Gambar Marker & Info
        self.pivot_marker.goto(self.pos[0], self.pos[1])
        self.pivot_marker.showturtle()
        
        self.t.penup()
        self.t.goto(self.pos[0] - 40, self.pos[1] + 30)
        self.t.pencolor("black")
        self.t.write(f"Pos: ({round(self.pos[0], 1)}, {round(self.pos[1], 1)}) | Rot: {round(self.angle)}° | Scaled: {self.is_scaled} | Mirrored: {self.is_mirrored}", 
                                 font=("Arial", 8, "bold"))
        
        self.screen.update()

# -----------------------------------------------------
# FUNGSI INTERAKTIF (EVENT HANDLERS)
# -----------------------------------------------------

# === 1. TRANSLASI (DASH) ===
def do_dash(dx, dy):
    T_dash = get_translation_matrix(dx, dy)
    player.pos = transform_point(T_dash, player.pos)
    player.redraw()
    print(f"DASH ({dx}, {dy}): Posisi baru {player.pos[:2]}")

def dash_right(): do_dash(DASH_DISTANCE, 0)
def dash_left(): do_dash(-DASH_DISTANCE, 0)
def dash_up(): do_dash(0, DASH_DISTANCE)
def dash_down(): do_dash(0, -DASH_DISTANCE)

# === 2. ROTASI KARAKTER (TOGGLE 60 DERAJAT) - MENGGUNAKAN MATRIKS UNTUK POSISI ===
def do_rotate():
    """ROTASI: Memutar posisi karakter dan sudut karakter sebesar 60 derajat terhadap (0,0)."""
    
    if not player.is_rotated_60:
        rotation_angle = ROTATION_AMOUNT # 60.0 derajat
        player.base_angle = player.angle
        player.angle += rotation_angle
        player.is_rotated_60 = True
    else:
        rotation_angle = -ROTATION_AMOUNT # -60.0 derajat
        player.angle = player.base_angle
        player.is_rotated_60 = False
        
    player.angle %= 360
    
    # --- PERUBAHAN UTAMA: Rotasi Posisi Menggunakan Matriks ---
    # 1. Dapatkan Matriks Rotasi R
    M_R = get_rotation_matrix(rotation_angle)
    
    # 2. Terapkan Rotasi pada posisi karakter P
    player.pos = transform_point(M_R, player.pos)
    # ---------------------------------------------------------
    
    player.redraw()
    print(f"ROTASI TOGGLE: Pindah ke {player.angle}° | Posisi baru {player.pos[:2]}")


# === 3. SCALING (ITEM KEKUATAN) ===
def do_scale():
    """SCALING: Mengganti gambar dengan versi skala dan menggeser ke atas/bawah."""
    
    scale_offset = (BASE_HEIGHT * SCALE_FACTOR - BASE_HEIGHT) / 2
    
    if not player.is_scaled:
        dy_compensation = scale_offset
    else:
        dy_compensation = -scale_offset

    T_compensation = get_translation_matrix(0, dy_compensation)
    player.pos = transform_point(T_compensation, player.pos)
    
    player.is_scaled = not player.is_scaled
    
    player.redraw()
    print(f"SCALE: Status skala: {player.is_scaled}. Posisi Y baru: {player.pos[1]}")


# === 4. REFLEKSI (CERMIN DUNIA) ===
def do_mirror():
    """REFLEKSI: Mengganti gambar dengan versi cermin dan membalik koordinat X."""
    M_mirror = get_reflection_y_matrix()
    
    player.pos = transform_point(M_mirror, player.pos)
    
    player.is_mirrored = not player.is_mirrored
        
    player.redraw()
    print(f"REFLEKSI: Posisi baru {player.pos[:2]}, Gambar dicerminkan: {player.is_mirrored}")


# -----------------------------------------------------
# MAIN GAME LOOP SETUP
# -----------------------------------------------------
screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.title("Transformasi 2D: Game Demo (Translasi, Rotasi Posisi, Skala, Refleksi)")
screen.tracer(0) 

t = turtle.Turtle()
t.hideturtle()
t.speed(0)

# Inisialisasi Player
try:
    player = Player(t, screen)
    
    player.redraw()
    print("Game Dimulai. Tekan tombol untuk transformasi.")

    # Pasang Event Keyboard
    screen.listen() 
    screen.onkey(dash_right, "Right")
    screen.onkey(dash_left, "Left")
    screen.onkey(dash_up, "Up")
    screen.onkey(dash_down, "Down")
    screen.onkey(do_rotate, "r") # Rotasi Karakter (Toggle 60 Derajat)
    screen.onkey(do_scale, "s")  # Scaling
    screen.onkey(do_mirror, "m") # Refleksi

    screen.mainloop()
    
except FileNotFoundError:
    print("Program dihentikan karena file gambar tidak ditemukan.")