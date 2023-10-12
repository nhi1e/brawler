import pygame

class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, attack_sound, jump_sound): #x,y is location of fighter on screen
        self.player = player
        self.size = data[0] #size of img
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0: idle, 1: move, 2: attack, 3:dead, 4:none, 5:jump
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180)) 
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_sound = attack_sound
        self.jump_sound = jump_sound
        self.attack_cooldown = 0
        self.hit = False
        self.health = 100
        self.alive = True

    def load_images(self, sprite_sheet, animation_steps):
        #extract images from sprite sheet
        animation_list = []
        for y, animation in enumerate (animation_steps): #down the sprite sheet
            temp_img_list = [] 
            for x in range(animation): #right along the sprite sheet
                temp_img = sprite_sheet.subsurface(x*self.size, y*self.size, self.size, self.size) #square
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list
    
    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 7 #10
        GRAVITY = 1.75 
        dx = 0 #change in x coord
        dy = 0 #change in y coord (0=stationary)
        self.running = False
        
        #get keypress
        key = pygame.key.get_pressed()

        #can only perform other actions if not currently attacking
        if (self.attacking == False) and (self.alive == True) and round_over == False:
            #check player 1 controls
            if self.player == 1:
                #movement
                #LEFT
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                #RIGHT
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                #JUMP
                if key[pygame.K_w] and self.jump == False: #dont allow double jump
                    self.vel_y = -30
                    self.jump = True
                    self.jump_sound.play()
                #ATTACK
                if key[pygame.K_r]: 
                    self.attack(target)

            #check player 2 controls
            if self.player == 2:
                #movement
                #LEFT
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                #RIGHT
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                #JUMP
                if key[pygame.K_UP] and self.jump == False: #dont allow double jump
                    self.vel_y = -30
                    self.jump = True
                    self.jump_sound.play()
                #ATTACK
                if key[pygame.K_p]:
                    self.attack(target)
             


        #apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y 

        #make sure player stays on screen
        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left #=0 as far as left edge
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right 
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False #on the ground
            dy = screen_height - 110 - self.rect.bottom

        #ensure players face each other
        if self.rect.centerx >= target.rect.centerx:
            self.flip = True
        else:
            self.flip = False

        #apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        #update player position
        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        #check current action of player

        if self.health <= 0:
            self.health = 0 #health bar doesnt go off the scale
            self.alive = False
            self.update_action(3)
        elif self.jump == True:
            self.update_action(5)
        elif self.hit == True:
            self.update_action(3)
        elif self.attacking == True:
            self.update_action(2)
        elif self.running == True:
            self.update_action(1) #move
        else: 
            self.update_action(0) #idle

        animation_cooldown = 80
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #check if animatin finished
        if self.frame_index >= len(self.animation_list[self.action]):
            #if player dead, end animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action])-1
            else:
                self.frame_index = 0
                #check if an attack was made
                if self.action == 2:
                    self.attacking = False
                    self.attack_cooldown = 30
                #check if hurt
                if self.action == 3:
                    self.hit = False
                    #if player was in middle of attack, attack is stopped
                    self.attacking = False
                    self.attack_cooldown = 30

    def attack(self, target):
        if self.attack_cooldown == 0:
            #execute attack
            self.attacking = True 
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (1.0 * self.rect.width * self.flip), self.rect.y, 1.0*self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10    
                target.hit = True



    def update_action(self, new_action):
        #check if if new action has more/less frames then current
        if new_action != self.action:
            self.action = new_action
            #update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        flipped_img = pygame.transform.flip(self.image, self.flip, False)
        #pygame.draw.rect(surface, ("YELLOW"), self.rect)
        surface.blit(flipped_img, (self.rect.x -(self.offset[0]*self.image_scale), self.rect.y-(self.offset[1]*self.image_scale)))