import pygame
from fighter import Fighter

pygame.init()

# Setup Jendela
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Duel Katana") 

# Setup Game
clock = pygame.time.Clock()
FPS = 90

# Definisi Warna
GREEN = (0, 255, 0)
RED = (255, 0 ,0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0) 
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)

# Inisialisasi Font
pygame.font.init()
VICTORY_FONT = pygame.font.Font(None, 80)
MENU_FONT = pygame.font.Font(None, 50)
TITLE_FONT = pygame.font.Font(None, 120)

# ------------------- DATA KARAKTER -------------------

# Data Karakter Komandan Samurai (Karakter 1)
RONIN_DATA = [250, 1, [112, 56], 5, 15] 
RONIN_SHEET_PATHS = [
    "images/samurai/Sprites/Idle.png", "images/samurai/Sprites/Run.png", "images/samurai/Sprites/Jump.png",
    "images/samurai/Sprites/Attack_1.png", "images/samurai/Sprites/Attack_2.png", 
    "images/samurai/Sprites/Hurt.png", "images/samurai/Sprites/Dead.png"
]
RONIN_ANIMATION_STEPS = [5, 8, 7, 4, 5, 2, 6] 

# Data Karakter Ronin Pemberontak (Karakter 2 - BOT Default)
ROUNIN_DATA = [250, 1, [112, 56], 5, 15] 
ROUNIN_SHEET_PATHS = [
    "images/rounin/Sprites/Idle.png", "images/rounin/Sprites/Run.png", "images/rounin/Sprites/Jump.png",
    "images/rounin/Sprites/Attack_1.png", "images/rounin/Sprites/Attack_2.png", 
    "images/rounin/Sprites/Hurt.png", "images/rounin/Sprites/Dead.png"
]
ROUNIN_ANIMATION_STEPS = [6, 8, 9, 4, 5, 3, 6] 

# Data Karakter Archer
ARCHER_DATA = [250, 1, [112, 56], 6, 15] 
ARCHER_SHEET_PATHS = [
    "images/archer/Sprites/Idle.png", "images/archer/Sprites/Run.png", "images/archer/Sprites/Jump.png",
    "images/archer/Sprites/Attack_1.png", "images/archer/Sprites/Attack_2.png", 
    "images/archer/Sprites/Hurt.png", "images/archer/Sprites/Dead.png"
]
ARCHER_ANIMATION_STEPS = [9, 8, 9, 5, 5, 3, 5] 

# ------------------- KARAKTER BARU TAMBAHAN -------------------

# Data Karakter Kunoichi
KUNOICHI_DATA = [250, 1, [112, 56], 5, 12] # Cepat, Cooldown pendek
KUNOICHI_SHEET_PATHS = [
    "images/kunoichi/Sprites/Idle.png", "images/kunoichi/Sprites/Run.png", "images/kunoichi/Sprites/Jump.png",
    "images/kunoichi/Sprites/Attack_1.png", "images/kunoichi/Sprites/Attack_2.png", 
    "images/kunoichi/Sprites/Hurt.png", "images/kunoichi/Sprites/Dead.png"
]
KUNOICHI_ANIMATION_STEPS = [9, 8, 10, 6, 8, 2, 5] 

# Data Karakter Ninja Monk
NINJA_MONK_DATA = [250, 0.70, [112, -28], 7, 15] # Kuat, Cooldown lebih lama
NINJA_MONK_SHEET_PATHS = [
    "images/ninjamonk/Sprites/Idle.png", "images/ninjamonk/Sprites/Run.png", "images/ninjamonk/Sprites/Jump.png",
    "images/ninjamonk/Sprites/Attack_1.png", "images/ninjamonk/Sprites/Attack_2.png", 
    "images/ninjamonk/Sprites/Hurt.png", "images/ninjamonk/Sprites/Dead.png"
]
NINJA_MONK_ANIMATION_STEPS = [7, 8, 9, 5, 5, 4, 5] 

# Data Karakter Ninja Peasant
NINJA_PEASANT_DATA = [250, 0.70, [112, -28], 8, 15] # Dasar, Damage rendah
NINJA_PEASANT_SHEET_PATHS = [
    "images/ninjapeasant/Sprites/Idle.png", "images/ninjapeasant/Sprites/Run.png", "images/ninjapeasant/Sprites/Jump.png",
    "images/ninjapeasant/Sprites/Attack_1.png", "images/ninjapeasant/Sprites/Attack_2.png", 
    "images/ninjapeasant/Sprites/Hurt.png", "images/ninjapeasant/Sprites/Dead.png"
]
NINJA_PEASANT_ANIMATION_STEPS = [6, 6, 8, 6, 4, 2, 4]
# ------------------------------------------------------------------

# Koleksi Data Karakter
CHARACTER_DATA = {
    'KOMANDAN': {'data': RONIN_DATA, 'sheets': RONIN_SHEET_PATHS, 'steps': RONIN_ANIMATION_STEPS, 'name': 'KOMANDAN SAMURAI', 'is_default_p1': True},
    'PEMBERONTAK': {'data': ROUNIN_DATA, 'sheets': ROUNIN_SHEET_PATHS, 'steps': ROUNIN_ANIMATION_STEPS, 'name': 'RONIN PEMBERONTAK', 'is_default_p1': False},
    'ARCHER': {'data': ARCHER_DATA, 'sheets': ARCHER_SHEET_PATHS, 'steps': ARCHER_ANIMATION_STEPS, 'name': 'PEMANAH ULUNG', 'is_default_p1': False}, 
    'KUNOICHI': {'data': KUNOICHI_DATA, 'sheets': KUNOICHI_SHEET_PATHS, 'steps': KUNOICHI_ANIMATION_STEPS, 'name': 'KUNOICHI JELITA', 'is_default_p1': False}, # BARU
    'NINJA_MONK': {'data': NINJA_MONK_DATA, 'sheets': NINJA_MONK_SHEET_PATHS, 'steps': NINJA_MONK_ANIMATION_STEPS, 'name': 'NINJA BIARAWAN', 'is_default_p1': False}, # BARU
    'NINJA_PEASANT': {'data': NINJA_PEASANT_DATA, 'sheets': NINJA_PEASANT_SHEET_PATHS, 'steps': NINJA_PEASANT_ANIMATION_STEPS, 'name': 'NINJA PETANI', 'is_default_p1': False} # BARU
}

# Kontrol Pemain 1
PLAYER1_CONTROLS = {
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'jump': pygame.K_UP,
    'attack1': pygame.K_r, 
    'attack2': pygame.K_t, 
    'enlarge': pygame.K_e 
}

# Muat Aset
try:
    bg_image = pygame.image.load("images/background/background.jpg").convert_alpha()
    WINS_IMAGE = pygame.image.load("images/icons/victory.png").convert_alpha()  
    WINS_IMAGE = pygame.transform.scale(WINS_IMAGE, (200, 100))
    
    # Memuat semua sprite sheets ke dalam dictionary
    LOADED_SHEETS = {}
    for key, char_info in CHARACTER_DATA.items():
        sheets = []
        # Mengatasi error jika path tidak ditemukan dengan menggunakan try-except di dalam loop
        for path in char_info['sheets']:
            try:
                sheets.append(pygame.image.load(path).convert_alpha())
            except pygame.error:
                print(f"File sprite tidak ditemukan: {path}. Menggunakan permukaan placeholder.")
                sheets.append(pygame.Surface((1, 1))) # Placeholder
        LOADED_SHEETS[key] = sheets

except pygame.error as e:
    print(f"Error loading assets: {e}. MOHON CEK KEMBALI PATH FILE ANDA!")
    # Fallback jika aset gagal dimuat (tetap ada untuk sprite umum)
    bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_image.fill(BLACK)
    WINS_IMAGE = pygame.Surface((200, 100))
    WINS_IMAGE.fill(RED)
    # Fallback sheets (sudah ditangani di loop di atas)


# ------------------- FUNGSI UTILITAS -------------------

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))
    
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))
    
def draw_victory_text(text):
    img = VICTORY_FONT.render(text, True, YELLOW)
    rect = img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    
    wins_rect = WINS_IMAGE.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 80))
    screen.blit(WINS_IMAGE, wins_rect)
    
    screen.blit(img, rect)

# ------------------- FUNGSI GAME STATE -------------------

def reset_game(p1_char_key, p2_char_key):
    """Menginisialisasi ulang objek fighter berdasarkan pilihan karakter."""
    global fighter_1, fighter_2, game_over

    p1_info = CHARACTER_DATA[p1_char_key]
    p2_info = CHARACTER_DATA[p2_char_key]

    # Fighter 1 (Pemain, di kiri, flip=False)
    fighter_1 = Fighter(200, 310, False, p1_info['data'], LOADED_SHEETS[p1_char_key], p1_info['steps']) 
    
    # Fighter 2 (BOT, di kanan, flip=True)
    fighter_2 = Fighter(700, 310, True, p2_info['data'], LOADED_SHEETS[p2_char_key], p2_info['steps']) 
    
    game_over = False
    
    # Kembalikan state game ke "game"
    return "game"

def main_menu():
    """Menampilkan menu utama dan menangani input menu."""
    selected_option = 0 # 0: Mulai, 1: Pilih Karakter, 2: Keluar
    menu_options = ["Mulai Duel", "Pilih Karakter", "Keluar"]
    
    menu_running = True
    while menu_running:
        clock.tick(FPS)
        draw_bg()
        
        # Gambar Judul
        draw_text("DUEL KATANA", TITLE_FONT, WHITE, SCREEN_WIDTH // 2 - 270, 100)
        
        # Gambar Opsi Menu
        for i, option in enumerate(menu_options):
            color = YELLOW if i == selected_option else WHITE
            y_pos = 300 + i * 70
            
            # Hitung posisi X untuk penempatan di tengah
            text_surface = MENU_FONT.render(option, True, color)
            x_pos = SCREEN_WIDTH // 2 - text_surface.get_width() // 2
            
            screen.blit(text_surface, (x_pos, y_pos))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", None, None # Keluar dari program
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                
                if event.key == pygame.K_RETURN:
                    if selected_option == 0: # Mulai Duel (Menggunakan pilihan terakhir/default)
                        return "game", None, None 
                    if selected_option == 1: # Pilih Karakter
                        return "select_char", None, None
                    if selected_option == 2: # Keluar
                        return "quit", None, None
                        
        pygame.display.update()
        
    return "menu", None, None

def character_selection_menu():
    """Memungkinkan Pemain 1 memilih karakter."""
    char_options = list(CHARACTER_DATA.keys()) # Kini mencakup 6 karakter
    selected_index = 0
    
    selection_running = True
    while selection_running:
        clock.tick(FPS)
        draw_bg()
        
        draw_text("PILIH KARAKTERMU (P1)", MENU_FONT, WHITE, SCREEN_WIDTH // 2 - 250, 100)
        
        for i, char_key in enumerate(char_options):
            char_name = CHARACTER_DATA[char_key]['name']
            
            color = YELLOW if i == selected_index else WHITE
            y_pos = 200 + i * 60 # Disesuaikan agar muat 6 opsi
            
            text_surface = MENU_FONT.render(char_name, True, color)
            x_pos = SCREEN_WIDTH // 2 - text_surface.get_width() // 2
            
            screen.blit(text_surface, (x_pos, y_pos))
            
            # Tampilkan indikator pemilihan
            if i == selected_index:
                 draw_text("<<", MENU_FONT, YELLOW, x_pos - 70, y_pos)
                 draw_text(">>", MENU_FONT, YELLOW, x_pos + text_surface.get_width() + 40, y_pos)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", None, None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(char_options)
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(char_options)
                
                if event.key == pygame.K_RETURN:
                    p1_char_key = char_options[selected_index]
                    
                    # P2 (BOT) mengambil karakter yang TIDAK dipilih P1
                    remaining_keys = [key for key in char_options if key != p1_char_key]
                    
                    # Logika Pemilihan BOT: pilih karakter yang BUKAN P1
                    if 'PEMBERONTAK' in remaining_keys:
                        # Prioritaskan BOT default (PEMBERONTAK) jika tersedia
                        p2_char_key = 'PEMBERONTAK'
                    elif len(remaining_keys) > 0:
                        # Jika tidak, pilih karakter pertama yang tersisa
                        p2_char_key = remaining_keys[0] 
                    else:
                        # Kasus darurat (semua karakter adalah P1, tidak mungkin terjadi)
                        p2_char_key = p1_char_key
                        
                    return "game", p1_char_key, p2_char_key
                
                if event.key == pygame.K_ESCAPE:
                    return "menu", None, None # Kembali ke menu utama
                        
        pygame.display.update()
        
    return "menu", None, None

# ------------------- INISIALISASI AWAL -------------------

# State Game
game_state = "menu"
# Pilihan karakter default diubah untuk menggunakan RONIN sebagai default P1
p1_selection_key = 'KOMANDAN' 
p2_selection_key = 'PEMBERONTAK' 

# Perbarui Pilihan Default:
# Cari karakter default P1
default_p1 = next((key for key, info in CHARACTER_DATA.items() if info.get('is_default_p1', False)), 'KOMANDAN')
# Cari karakter default P2 (yang bukan P1)
default_p2 = next((key for key in CHARACTER_DATA.keys() if key != default_p1), 'PEMBERONTAK')

p1_selection_key = default_p1
p2_selection_key = default_p2

fighter_1 = None
fighter_2 = None
game_over = False

# Game Loop Utama
run = True
while run:
    
    clock.tick(FPS)
    
    if game_state == "menu":
        game_state, _, _ = main_menu()
        if game_state == "quit":
            run = False
        # Jika game_state adalah "game" dari menu utama, gunakan pilihan terakhir/default.
        elif game_state == "game":
            game_state = reset_game(p1_selection_key, p2_selection_key)
        
    elif game_state == "select_char":
        game_state, p1_key_new, p2_key_new = character_selection_menu()
        if game_state == "quit":
            run = False
        elif game_state == "game":
            p1_selection_key = p1_key_new
            p2_selection_key = p2_key_new
            game_state = reset_game(p1_selection_key, p2_selection_key)
            
    elif game_state == "game":
        
        draw_bg()
        
        # Tampilkan Health Bar
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)
        
        if game_over == False:
            
            # Gerak P1 (Pemain)
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, PLAYER1_CONTROLS) 
            
            # Gerak P2 (BOT)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1)
            
            # Update Status
            fighter_1.update()
            fighter_2.update()
            
            # Cek Game Over
            if fighter_1.alive == False or fighter_2.alive == False:
                 game_over = True
        
        elif game_over == True:
            # Tahan frame death
            fighter_1.update()
            fighter_2.update()
        
        # Gambar Fighter
        fighter_1.draw(screen)
        fighter_2.draw(screen)
        
        # Tampilkan Teks Kemenangan (Jika game over)
        if game_over == True:
            p1_name = CHARACTER_DATA[p1_selection_key]['name']
            p2_name = CHARACTER_DATA[p2_selection_key]['name']
            
            if fighter_1.alive == True and fighter_2.alive == False:
                draw_victory_text(f"{p1_name} WINS!") 
            elif fighter_2.alive == True and fighter_1.alive == False:
                draw_victory_text(f"{p2_name} WINS!") 
            
            # Tunggu input untuk kembali ke menu
            draw_text("Tekan SPACE untuk ke Menu", MENU_FONT, GRAY, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 50)
            
        # Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if game_over == False and event.type == pygame.KEYDOWN:
                # Toggle Teknik Membesar (Tombol E) - Hanya P1 (Komandan Samurai) yang memiliki kemampuan ini
                if event.key == PLAYER1_CONTROLS.get('enlarge') and p1_selection_key == 'KOMANDAN': 
                    fighter_1.toggle_enlarge(SCREEN_WIDTH)
            
            if game_over == True and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = "menu" # Kembali ke menu utama
            
        # Update Display
        pygame.display.update()
            
pygame.quit()