cimport pygame
from pygame import mixer
import random
import math


#initialize the pygame
pygame.init()

#create the window
screen = pygame.display.set_mode((1300,800))

#background
background = pygame.image.load('bg.png')

background = pygame.transform.scale(background, (1300, 800))

#Background music
mixer.music.load('bg.wav')
mixer.music.play(-1)

#Title and icon
pygame.display.set_caption("MJB_DBZ demo ")
icon = pygame.image.load('rocket(1).png')
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('goku1.png')
playerX = 600
playerY = 570
playerX_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 6

for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load('frieza.png'))
    enemyX.append(random.randint(0, 670))
    enemyY.append(random.randint(0, 100))
    enemyX_change.append(2)
    enemyY_change.append(40)

#Ki blast
blastImg = pygame.image.load('ki.png')
blastImg = pygame.transform.scale(blastImg, (80,80))
blastX = 0
blastY = 570
blastX_change = 0
blastY_change = 5
#ready, cannot see ki until fire
blast_state = "ready"

score = 0

#Score
score_value = 0
font = pygame.font.Font('Coda-Heavy.ttf',32)
textX = 10
textY = 10

#Game over
over_font = pygame.font.Font('Coda-Heavy.ttf', 200)

def show_score(x, y):
    score = font.render("score : " + str(score_value), True, (255,0,0))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (550,400))


def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_blast(x,y):
    global blast_state
    blast_state = "fire"
    screen.blit(blastImg, (x+16, y +10))

def isCollision(enemyX, enemyY, blastX, blastY):
    distance = math.sqrt(math.pow(enemyX - blastX,2)) + (math.pow(enemyY - blastY, 2))
    if distance < 27:
        return True
    else:
        return False


#keeps window open
running = True
while running:
    #screen color
    screen.fill((0,0,0))
    #backgroung image
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #if keystroke is pressed, check right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2

            if event.key == pygame.K_RIGHT:
                playerX_change = 2

            if event.key == pygame.K_SPACE:
                if blast_state is "ready":
                    blast_sound = mixer.Sound('blast.wav')
                    blast_sound.play()
                    #Get the current x coordinate for player
                    blastX = playerX
                    fire_blast(blastX, blastY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1
    playerX += playerX_change
    #prevent out of bounds
    if playerX <=0:
        playerX = 0
    elif playerX >= 1180:
        playerX = 1180

    #blast movement
    if blastY <= 0:
        blastY = 570
        blast_state = "ready"

    if blast_state is "fire":
        fire_blast(blastX,blastY)
        blastY -= blastY_change
    #enemy movement
    for i in range(num_of_enemy):
        #Game over
        if enemyY[i] >= 570:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 1180:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], blastX, blastY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            blastY = 570
            blast_state = "ready"
            score_value += 1

            enemyX[i] = random.randint(0, 670)
            enemyY[i] = random.randint(0, 100)
        enemy(enemyX[i], enemyY[i], i)




    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()




