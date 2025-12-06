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

# Inisialisasi Font
pygame.font.init()
VICTORY_FONT = pygame.font.Font(None, 80) 

# Data Karakter (Komandan Samurai/P1)
RONIN_SIZE = 250
RONIN_SCALE = 1
RONIN_OFFSET = [72, 56]
RONIN_DAMAGE = 30
RONIN_COOLDOWN = 15
RONIN_DATA = [RONIN_SIZE, RONIN_SCALE, RONIN_OFFSET, RONIN_DAMAGE, RONIN_COOLDOWN] 

# Data Karakter (Ronin/P2 - BOT)
SENSEI_SIZE = 250
SENSEI_SCALE = 1
SENSEI_OFFSET = [112, 56]
SENSEI_DAMAGE = 1
SENSEI_COOLDOWN = 270
SENSEI_DATA = [SENSEI_SIZE, SENSEI_SCALE, SENSEI_OFFSET, SENSEI_DAMAGE, SENSEI_COOLDOWN] 


# Kontrol Pemain 1
PLAYER1_CONTROLS = {
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'jump': pygame.K_UP,
    'attack1': pygame.K_r, 
    'attack2': pygame.K_t, 
    'enlarge': pygame.K_e 
}

# Path Sprite
RONIN_SHEET_PATHS = [
    "images/samurai/Sprites/Idle.png", "images/samurai/Sprites/Run.png", "images/samurai/Sprites/Jump.png",
    "images/samurai/Sprites/Attack_1.png", "images/samurai/Sprites/Attack_2.png", 
    "images/samurai/Sprites/Hurt.png", "images/samurai/Sprites/Dead.png"
]
RONIN_ANIMATION_STEPS = [5, 8, 7, 4, 5, 2, 6] 

SENSEI_SHEET_PATHS = [
    "images/rounin/Sprites/Idle.png", "images/rounin/Sprites/Run.png", "images/rounin/Sprites/Jump.png",
    "images/rounin/Sprites/Attack_1.png", "images/rounin/Sprites/Attack_2.png", 
    "images/rounin/Sprites/Hurt.png", "images/rounin/Sprites/Dead.png"
]
SENSEI_ANIMATION_STEPS = [6, 8, 9, 4, 5, 3, 6] 

list_of_ronin_sheets = []
list_of_sensei_sheets = []

# Muat Aset
try:
    bg_image = pygame.image.load("images/background/background.jpg").convert_alpha()
    
    # Muat gambar WINS
    WINS_IMAGE = pygame.image.load("images/icons/victory.png").convert_alpha() 
    WINS_IMAGE = pygame.transform.scale(WINS_IMAGE, (200, 100))
    
    # Muat sheet karakter
    for path in RONIN_SHEET_PATHS:
        list_of_ronin_sheets.append(pygame.image.load(path).convert_alpha())

    for path in SENSEI_SHEET_PATHS:
        list_of_sensei_sheets.append(pygame.image.load(path).convert_alpha())

except pygame.error as e:
    print(f"Error loading assets: {e}. MOHON CEK KEMBALI PATH FILE ANDA!")
    # Fallback
    bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_image.fill((100, 100, 100))
    WINS_IMAGE = pygame.Surface((200, 100))
    WINS_IMAGE.fill(RED)
    
    list_of_ronin_sheets = [pygame.Surface((1, 1))] * len(RONIN_SHEET_PATHS)
    list_of_sensei_sheets = [pygame.Surface((1, 1))] * len(SENSEI_SHEET_PATHS)


# Fungsi untuk menggambar background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))
    
# Fungsi untuk menggambar health bar
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))
    
# Fungsi untuk menggambar teks dan ikon kemenangan
def draw_victory_text(text):
    # Teks
    img = VICTORY_FONT.render(text, True, YELLOW)
    rect = img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    
    # Ikon WINS
    wins_rect = WINS_IMAGE.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 80))
    screen.blit(WINS_IMAGE, wins_rect)
    
    screen.blit(img, rect)
    
# Inisialisasi Fighter
fighter_1 = Fighter(200, 310, False, RONIN_DATA, list_of_ronin_sheets, RONIN_ANIMATION_STEPS) # Komandan Samurai (P1)
fighter_2 = Fighter(700, 310, True, SENSEI_DATA, list_of_sensei_sheets, SENSEI_ANIMATION_STEPS) # Ronin (P2 - BOT)

game_over = False

# Game Loop
run = True
while run:
    
    clock.tick(FPS)
    
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
        if fighter_1.alive == True and fighter_2.alive == False:
            draw_victory_text("KOMANDAN SAMURAI WINS!") 
        elif fighter_2.alive == True and fighter_1.alive == False:
            draw_victory_text("RONIN WINS!") 
            
    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        # Toggle Teknik Membesar (Tombol E)
        if event.type == pygame.KEYDOWN:
            if event.key == PLAYER1_CONTROLS.get('enlarge'):
                fighter_1.toggle_enlarge()
            
    # Update Display
    pygame.display.update()
            
pygame.quit()