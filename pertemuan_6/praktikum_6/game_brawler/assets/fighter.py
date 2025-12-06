import pygame

class Fighter():
    # Menerima data: [size, scale, offset, damage, cooldown]
    def __init__(self, x, y, flip, data, sprite_source, animation_steps):
        # Data Karakter
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.base_damage = data[3] 
        self.base_cooldown = data[4] 
        
        # Atribut Skala Dinamis (Teknik Membesar)
        self.base_rect_width = 80    
        self.base_rect_height = 180  
        self.current_scale_multiplier = 1.0 
        self.is_enlarged = False 
        
        # State Animasi
        self.flip = flip
        self.animation_list = self.load_images(sprite_source, animation_steps)
        self.action = 0 # 0:diam, 1:lari, 2:loncat, 3:serang1, 4:serang2, 5:terkena, 6:mati
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()  
        
        # Atribut Fisika & Pygame
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect((x, y, self.base_rect_width, self.base_rect_height)) 
        self.vel_y = 0
        self.jump = False
        self.running = False 
        
        # Atribut Pertarungan
        self.attacking = False
        self.attack_cooldown = 0
        self.attack_type = 0
        self.health = 100
        self.hit = False 
        self.alive = True 
        
    def load_images(self, list_of_sheets, animation_steps):
        animation_list = []
        for y, sheet in enumerate(list_of_sheets):
            animation = animation_steps[y] 
            temp_img_list = []
            frame_width = sheet.get_width() // animation 
            
            for x in range(animation):
                temp_img = sheet.subsurface(x * frame_width, 0, frame_width, sheet.get_height())
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
                
            animation_list.append(temp_img_list)
        return animation_list

    # Perbarui hitbox (Rect)
    def update_rect(self):
        old_center_x = self.rect.centerx
        old_bottom = self.rect.bottom
        
        new_width = int(self.base_rect_width * self.current_scale_multiplier)
        new_height = int(self.base_rect_height * self.current_scale_multiplier)
        
        # Pertahankan posisi bawah dan tengah
        self.rect = pygame.Rect(old_center_x - new_width // 2, old_bottom - new_height, new_width, new_height)
        
    # Ubah skala internal
    def change_scale(self, scale_multiplier):
        if scale_multiplier != self.current_scale_multiplier:
            self.current_scale_multiplier = scale_multiplier
            self.update_rect() 

    # Toggle Teknik Membesar
    def toggle_enlarge(self):
        # Hanya bisa toggle jika hidup dan bebas aksi
        if self.alive and self.hit == False and self.attacking == False:
            self.is_enlarged = not self.is_enlarged
            
            new_scale = 1.5 if self.is_enlarged else 1.0 
            self.change_scale(new_scale)
    
    # -------------------------------------------------------------------------------------
    
    def update(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        
        # Update frame
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            
        # Handle akhir animasi
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3 or self.action == 4: # Serangan selesai
                self.attacking = False
                self.frame_index = 0 
                self.set_action(0) 
            elif self.action == 5: # Animasi Hit selesai
                self.hit = False
                self.frame_index = 0
                if self.health <= 0:
                    self.set_action(6) # Mati
                else:
                    self.set_action(0) # Kembali Idle
            elif self.action == 6: # Animasi Mati
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
        
        # Kurangi cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def set_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            
    # -------------------------------------------------------------------------------------

    def move(self, screen_width, screen_height, surface, target, controls=None): 
        
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False 
        self.attack_type = 0 
        
        SPEED = 10
        if controls is None: # Kecepatan BOT
            SPEED = 2 
        
        if self.alive and self.hit == False:
            
            # Logika BOT (Fighter 2)
            if controls is None:
                distance = target.rect.centerx - self.rect.centerx
                
                if abs(distance) > 100: # Bergerak
                    dx = SPEED if distance > 0 else -SPEED
                    self.running = True
                    self.flip = distance < 0
                elif abs(distance) < 110: # Serang
                    self.attack_type = 1 
                    if self.attack_cooldown == 0:
                        self.attack(surface, target)
                        
            # Logika PEMAIN (Fighter 1)
            else: 
                key = pygame.key.get_pressed()
                
                if self.attacking == False: 
                    
                    # Pergerakan
                    if key[controls['left']]:
                        dx = -SPEED
                        self.running = True
                        self.flip = True 
                    if key[controls['right']]:
                        dx = SPEED
                        self.running = True
                        self.flip = False 
                    
                    # Lompat
                    if key[controls['jump']] and self.jump == False:
                        self.vel_y = -35
                        self.jump = True
                
                # Serangan
                if (key[controls['attack1']] or key[controls['attack2']]):
                    if self.attack_cooldown == 0:
                        self.attack_type = 1 if key[controls['attack1']] else 2
                        self.attack(surface, target) 
                
            # Penentuan Animasi
            if self.attacking:
                pass 
            elif self.jump:
                self.set_action(2) 
            elif self.running:
                self.set_action(1) 
            else:
                self.set_action(0) 
        elif self.alive == False:
            self.set_action(6) 
            dx = 0 
                    
        # Terapkan gravitasi dan batasan
        self.vel_y += GRAVITY
        dy += self.vel_y
        
        floor_level = screen_height - 110 
        if self.rect.bottom + dy > floor_level:
            self.vel_y = 0
            self.jump = False
            dy = floor_level - self.rect.bottom 
            if self.action == 2:
                self.set_action(0)
        
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        
        if dx == 0 and self.alive == True and controls is None:
            self.flip = target.rect.centerx < self.rect.centerx
            
        self.rect.x += dx
        self.rect.y += dy
            
    # -------------------------------------------------------------------------------------

    def attack(self, surface, target):
        
        damage_base = self.base_damage
        cooldown_base = self.base_cooldown 
        
        is_player_commander = hasattr(self, 'is_enlarged') and self.base_cooldown == 15 

        if self.attack_type == 1:
            self.set_action(3)
            
            if is_player_commander == False: # P2 (BOT)
                damage_dealt = damage_base 
                cooldown_time = cooldown_base 
            else: # P1
                # Tingkatkan damage jika Membesar aktif
                scale = self.current_scale_multiplier if self.is_enlarged else 1.0
                damage_dealt = int(damage_base * scale) 
                cooldown_time = cooldown_base 
            
        elif self.attack_type == 2:
            self.set_action(4)
            damage_dealt = damage_base 
            cooldown_time = cooldown_base 
        else:
            return

        self.attacking = True
        self.attack_cooldown = cooldown_time 
        
        # Hitbox serangan
        scale = self.current_scale_multiplier if is_player_commander else 1.0
        attack_width = int(2 * self.base_rect_width * scale)
        
        if self.flip == False: # Menghadap kanan
            attacking_rect = pygame.Rect(self.rect.right, self.rect.y, attack_width, self.rect.height)
        else: # Menghadap kiri
            attacking_rect = pygame.Rect(self.rect.left - attack_width, self.rect.y, attack_width, self.rect.height)
        
        # Cek tabrakan
        if attacking_rect.colliderect(target.rect):
            if target.hit == False: 
                target.health -= damage_dealt 
                
                if target.health <= 0:
                    target.health = 0 
                    target.alive = False
                    target.set_action(6) 
                else:
                    target.hit = True 
                    target.set_action(5) 
            
    # -------------------------------------------------------------------------------------

    def draw(self, surface):
        # Tentukan skala gambar dan offset
        scale = self.current_scale_multiplier if hasattr(self, 'current_scale_multiplier') else 1.0
        final_scale = self.image_scale * scale
        
        x_pos = self.rect.x - (self.offset[0] * final_scale)
        y_pos = self.rect.y - (self.offset[1] * final_scale)
        
        # Skala dan flip gambar
        scaled_image = pygame.transform.scale(self.image, 
                                              (self.size * final_scale, self.size * final_scale))
        img = pygame.transform.flip(scaled_image, self.flip, False)
        
        surface.blit(img, (x_pos, y_pos))