import pygame
import random
import math
from pygame import mixer

        ############### THIS GAME DOESN'T NEED A WIN WINDOW BECAUSE IS IMPOSSIBLE TO WIN #######################
pygame.init()
screen = pygame.display.set_mode((800, 600))

#Icon, title and background img
pygame.display.set_caption("Man VS Villacidro")
icon = pygame.image.load("./images/man.png")
pygame.display.set_icon(icon)
background = pygame.image.load("./images/start-background.jpg")

#Start background sound
mixer.music.load('./music/Shuffle_or_Boogie.mp3')
mixer.music.play(-1)


                        ########## DEFINE ALL THE VARIABLES AND LISTS ############# 

player_img = pygame.image.load('./images/man.png')
player_x = 370
player_y = 530
player_x_change = 0

enemy_img_choice = ['./images/mosquito.png', './images/alien.png', './images/goblin.png', './images/moth.png']
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 7

for i in range(num_of_enemies) :
    enemy_img.append(pygame.image.load(random.choice(enemy_img_choice)))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 130))
    enemy_x_change.append(2)
    enemy_y_change.append(40)

bullet_img = pygame.image.load('./images/bullet.png')
bullet_x = 0
bullet_y = 500
bullet_x_change = 0
bullet_y_change = 4 
bullet_state = 'ready'

level_value = 1
score_value = 0

velocity_level = [[0, 15, 2], [15, 30, 3], [30, 45, 4], [45, 60, 6], [60, 75, 8]] #enemy's speed depends on the current lv
list_levels = [[0, './music/laguna-theme.mp3', "./images/level-1.jpg", 1],
               [15, './music/Ff7_Battle_Theme.mp3', './images/level-2.jpg', 2], 
               [30, './music/force-your-way.mp3', './images/level-3.jpg', 3], 
               [45, './music/ff9-battle.mp3', './images/level-4.jpg', 4], 
               [60, './music/Jechts_Theme.mp3', './images/level-5.jpg', 5 ]]
    

                    ################ DEFINE ALL THE FUNCTIONS #####################

def show_score() :
    font = pygame.font.Font('freesansbold.ttf', 30)
    score = font.render("Score: " + str(score_value), True, (0,0,0))
    screen.blit(score, (10, 10))


def show_level() :
    level_font = pygame.font.Font('freesansbold.ttf', 30)
    level = level_font.render("Level: " + str(level_value), True, (0,0,0))
    screen.blit(level, (10, 40))

def change_difficulty(score, i, x_change, prev_score_limit, next_score_limit, new_speed) :
    if score >= prev_score_limit and score < next_score_limit :
        x_change[i] = new_speed

def player(x, y) :
    screen.blit(player_img, (x, y))

def enemy(x, y, i) :
    screen.blit(enemy_img[i], (x, y))

def fire_bullet(x, y,) :
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x , y - 10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y) :
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 35 :
        return True       
    return False

def game_over_text() :
    over_font = pygame.font.Font('freesansbold.ttf', 60)
    over_text = over_font.render("GAME OVER", True, (0,0,0))
    screen.blit(over_text, (200, 250))

def change_music(music) :
    global score_value
    score_value += 1
    mixer.music.load(music)
    mixer.music.play(-1)


                            ############# MAIN FUNCTION #############

running = False
while not running :
    screen.blit(background, (0,0))
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            exit()
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_SPACE :
                running = True
                break
    pygame.display.update()

#start game
while running :
    screen.fill((0,0,0))
    screen.blit(background, (0,0)) #the background may slow the movements

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False
        
        #Player and bullet movements  
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_LEFT :
                player_x_change = -2
                player_img = pygame.image.load('./images/man.png')
            if event.key == pygame.K_RIGHT :
                player_x_change = 2
            if event.key == pygame.K_SPACE :
                if bullet_state == 'ready' :
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP :
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                player_x_change = 0

    
    player_x += player_x_change
    
    #Keep the player inside the window
    if player_x <= 0 :
        player_x = 0
    elif player_x >= 736 :
        player_x = 736
    
    #Game over
    for i in range(num_of_enemies) :
    
        if enemy_y[i] > 480 :
            for j in range(num_of_enemies) :
                enemy_y[j] = 2000
            game_over_text()
            background = pygame.image.load('./images/game-over.jpg')

            break
        
        enemy_x[i] += enemy_x_change[i]
        
        #Change directions of enemy when touching the sides
        if enemy_x[i] <= 0 :
            
            #Depends on the score the enemy goes faster
            for j in velocity_level :
                change_difficulty(score_value, i, enemy_x_change, j[0], j[1], j[2])
            
            enemy_y[i] += enemy_y_change[i]
        
        elif enemy_x[i] >= 736 :
            
            #Depends on the score the enemy goes faster            
            for j in velocity_level :
                change_difficulty(score_value, i, enemy_x_change, j[0], j[1], -j[2])

            enemy_y[i] += enemy_y_change[i]

        #Detect a collision, remove bullet and respawn enemy
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            bullet_y = 500
            bullet_state = 'ready'
            score_value += 1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 130)

        enemy(enemy_x[i], enemy_y[i], i)
    
    #The bullet disappear after reaching 50 px on y
    if bullet_y <= 50 :
        bullet_y = 500
        bullet_state = 'ready'
    
    if bullet_state == 'fire' :
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
    
    #Call the array that has the level information and change level when needed
    for w in list_levels :
        if score_value == w[0] :
            change_music(w[1])
            background = pygame.image.load(w[2])
            level_value = w[3]


    player(player_x, player_y)
    show_score()
    show_level()
    pygame.display.update()

 