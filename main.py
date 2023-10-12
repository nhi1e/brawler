import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

#game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("monster vs skull")

#set framerate
clock = pygame.time.Clock()
FPS = 60

#COLORS
GREEN = (27,50,51)
LIGHT_GREEN = (153,175,166)

#define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0,0] #[p1, p2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

#define fighter variables
MONSTER_SIZE = 64 #50x50px
MONSTER_SCALE = 4
MONSTER_OFFSET = [20, 4]
MONSTER_DATA = [MONSTER_SIZE, MONSTER_SCALE, MONSTER_OFFSET]
SKULL_SIZE = 64  #64x64px
SKULL_SCALE = 4
SKULL_OFFSET = [20, 11] #[20, 14.5]
SKULL_DATA = [SKULL_SIZE, SKULL_SCALE, SKULL_OFFSET]

#load music and sounds
monster_attack_fx = pygame.mixer.Sound("assets/monster_attack.mp3")
monster_attack_fx.set_volume(0.5)
skull_attack_fx = pygame.mixer.Sound("assets/skull_attack.mp3")
skull_attack_fx.set_volume(0.5)
monster_jump_fx = pygame.mixer.Sound("assets/monster_jump.mp3")
monster_jump_fx.set_volume(0.5)
skull_jump_fx = pygame.mixer.Sound("assets/skull_jump.mp3")
skull_jump_fx.set_volume(0.5)
victory_fx = pygame.mixer.Sound("assets/victory.mp3")
victory_fx.set_volume(0.75)

#load background image
bg_image = pygame.image.load("assets/background.png").convert_alpha()
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_image2 = pygame.image.load("assets/background2.png").convert_alpha()
bg_image2 = pygame.transform.scale(bg_image2, (SCREEN_WIDTH, SCREEN_HEIGHT))


#load sprite sheet
monster_sheet = pygame.image.load("assets/monster.png").convert_alpha()
skull_sheet = pygame.image.load("assets/skull.png").convert_alpha()
#define number of steps in each animation
MONSTER_ANIMATION_STEPS = [4, 5, 6, 8, 0, 8]
SKULL_ANIMATION_STEPS = [4, 4, 4, 8, 0, 7]

#define font
count_font = pygame.font.Font("assets/rainyhearts.ttf", 80)
score_font = pygame.font.Font("assets/rainyhearts.ttf", 30)

#function for drawing text
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    img_rect = img.get_rect(center = (x, y))
    screen.blit(img, img_rect)

#function for drawing background
def draw_bg(img):
    screen.blit(img, (0,0))

#function for drawing health bars
def draw_health_bar(health, x, y):
    ratio = health/100
    pygame.draw.rect(screen, (229,235,222), (x-1, y-1, 404, 34))
    pygame.draw.rect(screen, LIGHT_GREEN, (x, y, 400, 30)) #health
    pygame.draw.rect(screen, GREEN, (x, y, 400*ratio, 30))

#create 2 instances of fighters
fighter_1 = Fighter(1, 200, 310, False, MONSTER_DATA, monster_sheet, MONSTER_ANIMATION_STEPS, monster_attack_fx, monster_jump_fx)
fighter_2 = Fighter(2, 700, 310, True, SKULL_DATA, skull_sheet, SKULL_ANIMATION_STEPS, skull_attack_fx, skull_jump_fx)


############### INTRO PAGE SETUP ###########################
text_surface = count_font.render('Street Fighter', False, 'White') 
text_rect = text_surface.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/4))

start_button_text = score_font.render('START', False, 'BLACK')
home_button_text = score_font.render('HOME', False, 'BLACK')
summary_button_text = score_font.render('END GAME', False, 'BLACK')


class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x,y)
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        #check mouse over  button
        if self.rect.collidepoint(pos):
            #print('hover')
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                self.clicked=True
                print('clicked')
                action = True
        
        if pygame.mouse.get_pressed()[0]==0:
            self.clicked=False

        pygame.draw.rect(screen, ("GRAY"), self.rect) #color of button
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

# INSTRUCTION TYPING ANIMATION
messages = ['',
            'p1 controls: a,d,w,r',
           'p2 controls: <- -> ^ p',
           'Press Start to play']
message_surface = score_font.render('', True, 'white')
counter = 0
speed = 4
message_index = 0
message = messages[message_index]
message_done = False


enter_text_surface = score_font.render('Press Enter to read instructions', False, 'light gray') 
enter_text_rect = enter_text_surface.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/3+80))


#game loop
game_active = False
intro_screen = True
summary_screen = False


while True:
    clock.tick(FPS)
                
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #game_active=False
            pygame.quit()
            exit()
        if event.type==pygame.KEYDOWN: #animate text for intro screen
            if event.key == pygame.K_RETURN and message_done and message_index<len(messages)-1:
                message_index+=1
                done=False
                message=messages[message_index]
                counter=0

    if intro_screen:
        screen.fill(GREEN)
        screen.blit(text_surface, text_rect)

        if counter<speed*len(message):
            counter+=1
        elif counter>=speed*len(message):
            message_done=True
            
        #instruction message
        message_surface = score_font.render(message[0:counter//speed], True, 'white')
        message_rect = message_surface.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/3+120))
        #pygame.draw.rect(screen, 'white', message_rect) #highlight
        screen.blit(message_surface, message_rect)
        screen.blit(enter_text_surface, enter_text_rect)

        #draw start button
        start_btn = Button(SCREEN_WIDTH/2,SCREEN_HEIGHT/3+320, start_button_text, 1)
        if start_btn.draw(): #start button clicked, reset game
            intro_screen = False
            game_active=True
            round_over = False
            intro_count = 4
            message_index = 0
            count = 0
            fighter_1 = Fighter(1, 200, 310, False, MONSTER_DATA, monster_sheet, MONSTER_ANIMATION_STEPS, monster_attack_fx, monster_jump_fx)
            fighter_2 = Fighter(2, 700, 310, True, SKULL_DATA, skull_sheet, SKULL_ANIMATION_STEPS, skull_attack_fx, skull_jump_fx)
 
    elif game_active:
        
        #draw background
        draw_bg(bg_image)

        #show player health
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)
        draw_text("MONSTER: " + str(score[0]), score_font, "WHITE", 95, 70)
        draw_text("SKULL: " + str(score[1]), score_font, "WHITE", 630, 70)

        #update countdown
        if intro_count <= 0:
            #move fighters
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
        else:
            #display countdown
            draw_text(str(intro_count), count_font, "WHITE", SCREEN_WIDTH/2, SCREEN_HEIGHT/3+80)
            #update countdown timer
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()
                

        #animate
        fighter_1.update()
        fighter_2.update()

        #draw fighter
        fighter_1.draw(screen)
        fighter_2.draw(screen)

        #check for player defeat
        if round_over == False:
            if fighter_1.alive == False:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
                fighter_2.jump == True
            elif fighter_2.alive == False:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
                fighter_1.jump == True
        else:
            # option for another round
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN: 
                    if event.key == pygame.K_SPACE: 
                        intro_screen = False
                        game_active=True
                        round_over = False
                        intro_count = 4
                        fighter_1 = Fighter(1, 200, 310, False, MONSTER_DATA, monster_sheet, MONSTER_ANIMATION_STEPS, monster_attack_fx, monster_jump_fx)
                        fighter_2 = Fighter(2, 700, 310, True, SKULL_DATA, skull_sheet, SKULL_ANIMATION_STEPS, skull_attack_fx, skull_jump_fx)



            draw_text("VICTORY!", count_font, "WHITE", SCREEN_WIDTH/2, SCREEN_HEIGHT/3)
            victory_fx.play()

            #after cooldown, display options
            if pygame.time.get_ticks() - round_over_time>ROUND_OVER_COOLDOWN:
                home_btn = Button(SCREEN_WIDTH/2,SCREEN_HEIGHT/3+380, home_button_text, 1)
                summary_btn = Button(SCREEN_WIDTH/2,SCREEN_HEIGHT/3+340, summary_button_text, 1)
                draw_text("press space for another round", score_font, "RED", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-40)


                if home_btn.draw(): #home button clicked
                    game_active=False
                    round_over = True
                    score = [0,0] #[p1, p2]
                    message_index = 0
                    counter = 0
                    intro_screen = True
                    

                elif summary_btn.draw():
                    intro_screen = False
                    game_active= False
                    final_score_p1 = score[0]
                    final_score_p2 = score[1]
                    round_over = False
                    summary_screen = True

    elif summary_screen:
        draw_bg(bg_image2)
        draw_text("MONSTER: " + str(final_score_p1), count_font, "WHITE", SCREEN_WIDTH/4, 60)
        draw_text("SKULL: " + str(final_score_p2), count_font, "WHITE", SCREEN_WIDTH*3/4, 60)
        if final_score_p2>final_score_p1: 
            draw_text("SKULL WINS !", count_font, "WHITE", SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        elif final_score_p2<final_score_p1: 
            draw_text("MONSTER WINS !", count_font, "WHITE", SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        else:
            draw_text("IT'S A TIE !", count_font, "WHITE", SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
            
        if home_btn.draw(): 
                #whenever home button clicked, reset values
                game_active=False
                round_over = True
                score = [0,0] #[p1, p2]
                message_index = 0
                counter = 0
                intro_screen = True
   

    #update display
    pygame.display.update()