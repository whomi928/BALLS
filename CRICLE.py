import pygame
import sys
import secrets
import math

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Hello")
        info = pygame.display.Info()
        self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
        self.clock=pygame.time.Clock()
        
        self.knife_image = pygame.image.load('C:\\Users\\shaur\\Desktop\\CRICLE\\knife.png').convert_alpha()
        self.knife_image = pygame.transform.scale(self.knife_image, (80, 80))
        self.gun_image = pygame.image.load('C:\\Users\\shaur\\Desktop\\CRICLE\\gun.png').convert_alpha()
        self.gun_image = pygame.transform.scale(self.gun_image, (80, 80))
        self.shortgun_image = pygame.image.load('C:\\Users\\shaur\\Desktop\\CRICLE\\shortgun.png').convert_alpha()
        self.shortgun_image = pygame.transform.scale(self.shortgun_image, (160, 160))
        self.bullet = pygame.image.load('C:\\Users\\shaur\\Desktop\\CRICLE\\bullet.png').convert()
        self.bullet = pygame.transform.scale(self.bullet, (50, 50))
        self.bullet.set_colorkey((255, 255, 255))
        self.pistal = pygame.image.load('C:\\Users\\shaur\\Desktop\\CRICLE\\pistal.png').convert_alpha()
        self.pistal = pygame.transform.scale(self.pistal, (80, 80))
        
        self.secure_num1 = secrets.randbelow(361)
        self.secure_num2 = secrets.randbelow(361)
        
        self.center_x=self.screen.get_width()//2
        self.center_y=self.screen.get_height()//2
        
        self.hit_sound = pygame.mixer.Sound("C:\\Users\\shaur\\Desktop\\CRICLE\\sound.mp3")
        self.hit_sound.set_volume(1.0)
        
        self.last = 0
        self.img = []
        self.red_ball_wep = None
        self.blue_ball_wep = None
        self.red = 10
        self.blue = 10
        self.picked_red = 0
        self.picked_blue = 0
        self.handgun_red = 0
        self.handgun_blue = 0
        
        self.red_shot = []
        self.blue_shot = []
        self.particles = []

        self.x1 = self.center_x + 50
        self.y1 = self.center_y + 50
        self.x2 = self.center_x - 50    
        self.y2 = self.center_y - 50
        
    def run(self):
        while True:
            # 1. UPDATE TIME AND CHECK EVENTS
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.red == 0 or self.blue == 0:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0,0,0))
            self.alive_blue = 0
            self.alive_red = 0
            
            # 2. DRAW ARENA & BALLS
            pygame.draw.circle(self.screen, (255, 255, 255), (self.screen.get_width()//2, self.screen.get_height()//2 + 40),
                               (self.screen.get_height()  // 20 ) * 8, width=2)
            pygame.draw.circle(self.screen, (255, 0, 0), (self.x1, self.y1), 20, width=0)
            pygame.draw.circle(self.screen, (0, 0, 255), (self.x2, self.y2), 20, width=0)
            
            # 3. MOVE BALLS
            self.x1 += 5 * math.cos(math.radians(self.secure_num1))
            self.y1 += 5 * math.sin(math.radians(self.secure_num1))
            self.x2 += 5 * math.cos(math.radians(self.secure_num2))
            self.y2 += 5 * math.sin(math.radians(self.secure_num2))
            
            # 4. WALL COLLISIONS
            big_circle_x = self.center_x
            big_circle_y = self.center_y + 40
            max_dist = (self.screen.get_height() // 20 * 8) - 20

            dist1_sq = (self.x1 - big_circle_x)**2 + (self.y1 - big_circle_y)**2
            if dist1_sq >= max_dist**2:
                dist1 = math.sqrt(dist1_sq)
                normal_angle = math.atan2(big_circle_y - self.y1, big_circle_x - self.x1)
                v_angle = math.radians(self.secure_num1)
                new_angle_rad = 2 * normal_angle - v_angle + math.pi
                self.secure_num1 = math.degrees(new_angle_rad) % 360
                overlap = dist1 - max_dist
                self.x1 += overlap * math.cos(normal_angle)
                self.y1 += overlap * math.sin(normal_angle)
                 
            dist2_sq = (self.x2 - big_circle_x)**2 + (self.y2 - big_circle_y)**2
            if dist2_sq >= max_dist**2:
                dist2 = math.sqrt(dist2_sq)
                normal_angle = math.atan2(big_circle_y - self.y2, big_circle_x - self.x2)
                v_angle = math.radians(self.secure_num2)
                new_angle_rad = 2 * normal_angle - v_angle + math.pi
                self.secure_num2 = math.degrees(new_angle_rad) % 360
                overlap = dist2 - max_dist
                self.x2 += overlap * math.cos(normal_angle)
                self.y2 += overlap * math.sin(normal_angle)
                
            # 5. BALL-TO-BALL COLLISIONS
            if (self.x1 - self.x2)**2 + (self.y1 - self.y2)**2 <= 40**2:
                dist = math.sqrt((self.x1 - self.x2)**2 + (self.y1 - self.y2)**2)
                if dist == 0: dist = 0.001 
                
                normal_angle = math.atan2(self.y2 - self.y1, self.x2 - self.x1)
                overlap = 40 - dist 
                
                self.x1 -= (overlap / 2) * math.cos(normal_angle)
                self.y1 -= (overlap / 2) * math.sin(normal_angle)
                self.x2 += (overlap / 2) * math.cos(normal_angle)
                self.y2 += (overlap / 2) * math.sin(normal_angle)
            
                v_angle1 = math.radians(self.secure_num1)
                new_angle1_rad = 2 * normal_angle - v_angle1 + math.pi
                self.secure_num1 = math.degrees(new_angle1_rad) % 360
                
                v_angle2 = math.radians(self.secure_num2)
                new_angle2_rad = 2 * normal_angle - v_angle2 + math.pi 
                self.secure_num2 = math.degrees(new_angle2_rad) % 360
                
                # Knife Damage
                if self.red_ball_wep == self.knife_image:
                    self.red_ball_wep = None
                    self.blue -= 1
                if self.blue_ball_wep == self.knife_image:
                    self.blue_ball_wep = None
                    self.red -= 1
                    
            # 6. SPAWN NEW WEAPONS
            if current_time - self.last >= 5000:
                self.last = current_time
                self.num = secrets.randbelow(13)
                rotation = secrets.randbelow(361)
                distance = secrets.randbelow((self.screen.get_height()  // 20 ) * 6)
                x_pos = self.screen.get_width() // 2 + distance * math.cos(math.radians(rotation))
                y_pos = self.screen.get_height() // 2 + 40 + distance * math.sin(math.radians(rotation))
                
                if self.num in [0, 1, 2, 3]: selected_image = self.knife_image
                elif self.num in [5, 6, 7]: selected_image = self.gun_image
                elif self.num in [4, 8, 9]: selected_image = self.shortgun_image
                elif self.num in [10, 11, 12]: selected_image = self.pistal
                self.img.append((selected_image, x_pos, y_pos))
                    
            # 7. DRAW GROUND WEAPONS
            for img in self.img:
                self.screen.blit(img[0], (img[1], img[2]))

            # 8. PICKUP LOGIC
            weapons_left_on_ground = []
            for image_data in self.img:
                weapon_surface = image_data[0]
                weapon_x = image_data[1]
                weapon_y = image_data[2]
                weapon_rect = pygame.Rect(weapon_x, weapon_y, weapon_surface.get_width(), weapon_surface.get_height())
                
                if weapon_rect.collidepoint(self.x1, self.y1):
                    self.red_ball_wep = weapon_surface
                    self.picked_red = current_time 
                    continue 
                if weapon_rect.collidepoint(self.x2, self.y2):
                    self.blue_ball_wep = weapon_surface 
                    self.picked_blue = current_time
                    continue 
                weapons_left_on_ground.append(image_data)
            self.img = weapons_left_on_ground

            # 9. SHOOTING LOGIC
            bullet_speed = 10
            
            # Red Guns
            if self.red_ball_wep == self.gun_image:
                if current_time - self.picked_red >= 2000:
                    dx = self.x2 - self.x1
                    dy = self.y2 - self.y1
                    angle_rad = math.atan2(dy, dx)
                    vx = math.cos(angle_rad) * bullet_speed
                    vy = math.sin(angle_rad) * bullet_speed
                    angle_deg = -math.degrees(angle_rad) 
                    self.red_shot.append([self.x1, self.y1, vx, vy, angle_deg])
                    # hand Gun breaks after one use
                    self.handgun_red += 1
                    if self.handgun_red >= 3:
                        self.red_ball_wep = None
                        self.handgun_red = 0
                    self.picked_red = current_time 
                    
            if self.red_ball_wep == self.pistal:
                if current_time - self.picked_red >= 2000:
                    dx = self.x2 - self.x1
                    dy = self.y2 - self.y1
                    angle_rad = math.atan2(dy, dx)
                    vx = math.cos(angle_rad) * bullet_speed
                    vy = math.sin(angle_rad) * bullet_speed
                    angle_deg = -math.degrees(angle_rad) 
                    self.red_shot.append([self.x1, self.y1, vx, vy, angle_deg])
                    self.red_ball_wep = None # Pistal breaks after one use
                    self.picked_red = current_time 
                        
            elif self.red_ball_wep == self.shortgun_image:
                if current_time - self.picked_red >= 2000:
                    dx = self.x2 - self.x1
                    dy = self.y2 - self.y1
                    base_angle_rad = math.atan2(dy, dx)
                    for offset in [-60, -30, 0, 30, 60]:
                        new_angle_rad = base_angle_rad + math.radians(offset)
                        vx = math.cos(new_angle_rad) * bullet_speed
                        vy = math.sin(new_angle_rad) * bullet_speed
                        angle_deg = -math.degrees(new_angle_rad)
                        self.red_shot.append([self.x1, self.y1, vx, vy, angle_deg])
                    self.red_ball_wep = None # Shortgun breaks after one use
                    self.picked_red = current_time 
                        
            # Blue Guns
            if  self.blue_ball_wep == self.pistal:
                if current_time - self.picked_blue >= 2000:
                    dx = self.x1 - self.x2
                    dy = self.y1 - self.y2
                    angle_rad = math.atan2(dy, dx)
                    vx = math.cos(angle_rad) * bullet_speed
                    vy = math.sin(angle_rad) * bullet_speed
                    angle_deg = -math.degrees(angle_rad) 
                    self.blue_shot.append([self.x2, self.y2, vx, vy, angle_deg])
                    self.picked_blue = current_time 
                    self.blue_ball_wep = None # Pistal breaks after one use
                    
            if self.blue_ball_wep == self.gun_image:
                if current_time - self.picked_blue >= 2000:
                    dx = self.x1 - self.x2
                    dy = self.y1 - self.y2
                    angle_rad = math.atan2(dy, dx)
                    vx = math.cos(angle_rad) * bullet_speed
                    vy = math.sin(angle_rad) * bullet_speed
                    angle_deg = -math.degrees(angle_rad) 
                    self.blue_shot.append([self.x2, self.y2, vx, vy, angle_deg])
                    self.picked_blue = current_time
                    self.handgun_blue += 1
                    if self.handgun_blue >= 3:
                        self.blue_ball_wep = None 
                        self.handgun_blue = 0
                    #Hand Gun breaks after one use
                        
            elif self.blue_ball_wep == self.shortgun_image:
                if current_time - self.picked_blue >= 2000:
                    dx = self.x1 - self.x2
                    dy = self.y1 - self.y2
                    base_angle_rad = math.atan2(dy, dx)
                    for offset in [-40, -20, 0, 20, 40]:
                        new_angle_rad = base_angle_rad + math.radians(offset)
                        vx = math.cos(new_angle_rad) * bullet_speed
                        vy = math.sin(new_angle_rad) * bullet_speed
                        angle_deg = -math.degrees(new_angle_rad)
                        self.blue_shot.append([self.x2, self.y2, vx, vy, angle_deg])
                    self.picked_blue = current_time 
                    self.blue_ball_wep = None # Shortgun breaks after one use

            # 10. DRAW HELD WEAPONS
            if self.red_ball_wep is not None:
                dx = self.x2 - self.x1
                dy = self.y2 - self.y1
                angle_rad = math.atan2(dy, dx)
                final_angle_red = -math.degrees(angle_rad)
                rotated_red = pygame.transform.rotate(self.red_ball_wep, final_angle_red)
                red_rect = rotated_red.get_rect(center=(self.x1, self.y1))
                self.screen.blit(rotated_red, red_rect.topleft)
                
            if self.blue_ball_wep is not None:
                dx = self.x1 - self.x2
                dy = self.y1 - self.y2
                angle_rad = math.atan2(dy, dx)
                final_angle_blue = -math.degrees(angle_rad)
                rotated_blue = pygame.transform.rotate(self.blue_ball_wep, final_angle_blue)
                blue_rect = rotated_blue.get_rect(center=(self.x2, self.y2))
                self.screen.blit(rotated_blue, blue_rect.topleft)

            # 11. MOVE & DRAW BULLETS
            red_bullets_to_keep = []
            for bullet in self.red_shot:
                bullet[0] += bullet[2] 
                bullet[1] += bullet[3] 
                rotated_bullet = pygame.transform.rotate(self.bullet, bullet[4])
                bullet_rect = rotated_bullet.get_rect(center=(bullet[0], bullet[1]))
                self.screen.blit(rotated_bullet, bullet_rect.topleft)
                
                if bullet_rect.collidepoint(self.x2, self.y2):
                    self.blue -= 1
                    self.alive_blue = 1
                    self.hit_sound.play()
                    for _ in range(15): # Spawn 15 fiery sparks
                        angle = math.radians(secrets.randbelow(361))
                        speed = secrets.randbelow(5) + 2
                        px = bullet_rect.centerx
                        py = bullet_rect.centery
                        pvx = math.cos(angle) * speed
                        pvy = math.sin(angle) * speed
                        pradius = secrets.randbelow(4) + 3
                        pcolor = (255, secrets.randbelow(150) + 50, 0)
                        
                        self.particles.append([px, py, pvx, pvy, pradius, pcolor])
                    continue
                if 0 <= bullet[0] <= self.screen.get_width() and 0 <= bullet[1] <= self.screen.get_height() and self.alive_blue == 0:
                    red_bullets_to_keep.append(bullet)
            self.red_shot = red_bullets_to_keep

            blue_bullets_to_keep = []
            for bullet in self.blue_shot:
                bullet[0] += bullet[2] 
                bullet[1] += bullet[3] 
                rotated_bullet = pygame.transform.rotate(self.bullet, bullet[4])
                bullet_rect = rotated_bullet.get_rect(center=(bullet[0], bullet[1]))
                self.screen.blit(rotated_bullet, bullet_rect.topleft) 
                
                if bullet_rect.collidepoint(self.x1, self.y1):
                    self.red -= 1
                    self.alive_red = 1
                    self.hit_sound.play()
                    for _ in range(15): # Spawn 15 fiery sparks
                        angle = math.radians(secrets.randbelow(361))
                        speed = secrets.randbelow(5) + 2
                        px = bullet_rect.centerx
                        py = bullet_rect.centery
                        pvx = math.cos(angle) * speed
                        pvy = math.sin(angle) * speed
                        pradius = secrets.randbelow(4) + 3
                        pcolor = (255, secrets.randbelow(150) + 50, 0) # Random red/orange/yellow
                        self.particles.append([px, py, pvx, pvy, pradius, pcolor])
                    continue 
                if 0 <= bullet[0] <= self.screen.get_width() and 0 <= bullet[1] <= self.screen.get_height() and self.alive_red == 0:
                    blue_bullets_to_keep.append(bullet)
            self.blue_shot = blue_bullets_to_keep

            # 12. DRAW HEALTH UI
            for i in range(10):
                pygame.draw.circle(self.screen, (255, 255, 255), (self.center_x - 40 * i - 100,40), 15, width=2)
                pygame.draw.circle(self.screen, (255, 255, 255), (self.center_x + 40 * i + 100,40), 15, width=2)
            for i in range(self.red):
                pygame.draw.circle(self.screen, (255, 0, 0), (self.center_x - 40 * i - 100,40), 14, width=0)
            for i in range(self.blue):
                pygame.draw.circle(self.screen, (0, 0, 255), (self.center_x + 40 * i + 100,40), 14, width=0)
                
            alive_particles = []
            for p in self.particles:
                p[0] += p[2]  
                p[1] += p[3]  
                p[4] -= 0.2   
                
                if p[4] > 0:
                    pygame.draw.circle(self.screen, p[5], (int(p[0]), int(p[1])), int(p[4]))
                    alive_particles.append(p)
                    
            self.particles = alive_particles
            
            pygame.display.update()
            self.clock.tick(60)

Game().run()