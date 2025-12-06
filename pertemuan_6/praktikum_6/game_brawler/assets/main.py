import pygame
from fighter import Fighter

pygame.init()

#create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Duel Katana") 

#set framerate
clock = pygame.time.Clock()
FPS = 90

#define colours
GREEN = (0, 255, 0)
RED = (255, 0 ,0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0) 

# Inisialisasi Font Kemenangan
pygame.font.init()
VICTORY_FONT = pygame.font.Font(None, 80) 

#define fighter variables
# Komandan Samurai (P1 - Kontrol Pemain)
RONIN_SIZE = 250
RONIN_SCALE = 1
RONIN_OFFSET = [72, 56]
RONIN_DAMAGE = 30 
RONIN_COOLDOWN = 15 
RONIN_DATA = [RONIN_SIZE, RONIN_SCALE, RONIN_OFFSET, RONIN_DAMAGE, RONIN_COOLDOWN] 

# Ronin (P2 - BOT)
SENSEI_SIZE = 250
SENSEI_SCALE = 1
SENSEI_OFFSET = [112, 56]
SENSEI_DAMAGE = 1 
SENSEI_COOLDOWN = 270 
SENSEI_DATA = [SENSEI_SIZE, SENSEI_SCALE, SENSEI_OFFSET, SENSEI_DAMAGE, SENSEI_COOLDOWN] 


# --- KEY MAPPINGS UNTUK PEMAIN 1 (Komandan Samurai) ---
PLAYER1_CONTROLS = {
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'jump': pygame.K_UP,
    'attack1': pygame.K_r, 
    'attack2': pygame.K_t, 
    'enlarge': pygame.K_e 
}

# --- DEFINISI PATH FILE SPRITE (Disesuaikan dengan input terakhir) ---
# Asumsi Komandan Samurai (P1)
RONIN_SHEET_PATHS = [
    "images/samurai/Sprites/Idle.png", "images/samurai/Sprites/Run.png", "images/samurai/Sprites/Jump.png",
    "images/samurai/Sprites/Attack_1.png", "images/samurai/Sprites/Attack_2.png", 
    "images/samurai/Sprites/Hurt.png", "images/samurai/Sprites/Dead.png"
]
RONIN_ANIMATION_STEPS = [5, 8, 7, 4, 5, 2, 6] 

# Asumsi Ronin (P2)
SENSEI_SHEET_PATHS = [
    "images/rounin/Sprites/Idle.png", "images/rounin/Sprites/Run.png", "images/rounin/Sprites/Jump.png",
    "images/rounin/Sprites/Attack_1.png", "images/rounin/Sprites/Attack_2.png", 
    "images/rounin/Sprites/Hurt.png", "images/rounin/Sprites/Dead.png"
]
SENSEI_ANIMATION_STEPS = [6, 8, 9, 4, 5, 3, 6] 

list_of_ronin_sheets = []
list_of_sensei_sheets = []

#load background image & sheets
try:
    bg_image = pygame.image.load("images/background/background.jpg").convert_alpha()
    
    # 🚨 BARU: Muat gambar WINS
    WINS_IMAGE = pygame.image.load("images/icons/victory.png").convert_alpha() 
    # Resize gambar WINS
    WINS_IMAGE = pygame.transform.scale(WINS_IMAGE, (200, 100))
    
    # Muat sheet Komandan Samurai (P1)
    for path in RONIN_SHEET_PATHS:
        sheet = pygame.image.load(path).convert_alpha()
        list_of_ronin_sheets.append(sheet)

    # Muat sheet Ronin (P2)
    for path in SENSEI_SHEET_PATHS:
        sheet = pygame.image.load(path).convert_alpha()
        list_of_sensei_sheets.append(sheet)

except pygame.error as e:
    print(f"Error loading assets: {e}. MOHON CEK KEMBALI PATH FILE ANDA!")
    # Fallback jika pemuatan gagal
    bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_image.fill((100, 100, 100))
    # Fallback untuk WINS_IMAGE
    WINS_IMAGE = pygame.Surface((200, 100))
    WINS_IMAGE.fill(RED)
    
    list_of_ronin_sheets = [pygame.Surface((1, 1))] * len(RONIN_SHEET_PATHS)
    list_of_sensei_sheets = [pygame.Surface((1, 1))] * len(SENSEI_SHEET_PATHS)


#function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))
    
#function for drawing fighter health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))
    
#function for drawing victory text
def draw_victory_text(text):
    img = VICTORY_FONT.render(text, True, YELLOW)
    rect = img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    
    # 🚨 Tampilkan Ikon WINS di atas teks kemenangan
    wins_rect = WINS_IMAGE.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 80))
    screen.blit(WINS_IMAGE, wins_rect)
    
    screen.blit(img, rect)
    
# create two instances of figters
fighter_1 = Fighter(200, 310, False, RONIN_DATA, list_of_ronin_sheets, RONIN_ANIMATION_STEPS) # Komandan Samurai (P1)
fighter_2 = Fighter(700, 310, True, SENSEI_DATA, list_of_sensei_sheets, SENSEI_ANIMATION_STEPS) # Ronin (P2 - BOT)

# Game Control State
game_over = False

#game loop
run = True
while run:
    
    clock.tick(FPS)
    
    #draw background
    draw_bg()
    
    #show player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    
    # LOGIKA PERGERAKAN, UPDATE, DAN GAME FLOW
    if game_over == False:
        
        # Fighter 1 (Komandan Samurai) Move (Pemain 1)
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, PLAYER1_CONTROLS) 
        
        # Fighter 2 (Ronin) Move (BOT)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1)
        
        # Update fighters
        fighter_1.update()
        fighter_2.update()
        
        # Cek status game over setelah update (untuk deteksi death)
        if fighter_1.alive == False or fighter_2.alive == False:
             game_over = True
    
    # Jika game over, update hanya untuk menahan frame death
    elif game_over == True:
        fighter_1.update()
        fighter_2.update()
    
    #draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)
    
    # LOGIKA NOTIFIKASI KEMENANGAN
    if game_over == True:
        if fighter_1.alive == True and fighter_2.alive == False:
            draw_victory_text("KOMANDAN SAMURAI WINS!") 
        elif fighter_2.alive == True and fighter_1.alive == False:
            draw_victory_text("RONIN WINS!") 
            
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        # IMPLEMENTASI TOGGLE MEMBESAR/MENGEcil (Tombol E)
        if event.type == pygame.KEYDOWN:
            if event.key == PLAYER1_CONTROLS.get('enlarge'):
                fighter_1.toggle_enlarge()
            
    #update display
    pygame.display.update()
            
#exit pygame
pygame.quit()