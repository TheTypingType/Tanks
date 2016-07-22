import pygame
import time
import random
import math

pygame.init()

#colors
white = (255, 255, 255)
black = (0, 0, 0)

red = (200, 0, 0)
light_red = (255, 0, 0)

green = (0, 155, 0)
light_green = (0, 255, 0)

yellow = (200, 200, 0)
light_yellow = (255, 255, 0)

sand = (191, 135, 32) #(229, 160, 41)

display_width = 800
display_height = 600

#Tankparameters
tankSize = 1
tankWidth = tankSize * 40
tankHeight = tankSize * 14

turretWidth = tankSize * 3
wheelWidth = tankSize * 5

gameDisplay = pygame.display.set_mode((display_width,display_height)) #Display size
pygame.display.set_caption("Tanks") #Title of the window
pygame.display.set_icon(pygame.image.load("TankIcon.png"))

#sounds
intro_music = pygame.mixer.Sound("BattleThemeMix.ogg")
theme_music = pygame.mixer.Sound("bensound-epic.ogg")
game_over_music = pygame.mixer.Sound("LaidBackGuitars.ogg")
fire_sound = pygame.mixer.Sound("TankFiring.ogg")
explosion_sound = pygame.mixer.Sound("Explosion.wav")
explosion_sound.set_volume(0.5)

enemy_channel0 = pygame.mixer.Channel(0)
enemy_channel1 = pygame.mixer.Channel(1)
player_channel0 = pygame.mixer.Channel(2)
player_channel1 = pygame.mixer.Channel(3)
theme_music_channel = pygame.mixer.Channel(4)

#images
background_image = pygame.image.load("BG.png")

ground_height = display_height * 0.07


clock = pygame.time.Clock()

#fonts
smallfont = pygame.font.SysFont("verdana", 25)
medfont = pygame.font.SysFont("georgia", 50)
largefont = pygame.font.SysFont("georgia", 80)

#I did not quite understand how exactly we centered the text... :(
def text_objects(text, color, size) :
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def button(msg, x, y, width, height, inactive_color, active_color, action = None, size = "small"):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    global game_status
    
    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x,y,width,height))
        if click[0] == 1:              
            if action == "quit":
                quit()
            if action == "options":
                game_status = "options"
                return True
            if action == "play":
                game_status = "loop"
                return True
                
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x,y,width,height))

    
    textSurf, textRect = text_objects(msg, black, size)
    textRect.center = (x + (width / 2), y + (height / 2))
    gameDisplay.blit(textSurf, textRect)
    return False
    

def message_to_screen(msg, color, y_displace = 0, size = "small") :
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)

def ground():
    gameDisplay.fill(sand, rect=[0,
                                  display_height - ground_height,
                                  display_width,
                                  ground_height])
def draw_background():
    gameDisplay.blit(background_image, (0, 0))

def barrier(xlocation, randomHeight, barrierWidth):
     pygame.draw.rect(gameDisplay,
                      sand,
                      [xlocation - int(barrierWidth / 2),
                       display_height - randomHeight,
                       barrierWidth,
                       randomHeight])

def tank(x,y, TurretPosition = 0):
    x = int(x)
    y = int(y)
                                                                                        #Positions:
    possibleTurrets = [(x - 20 * tankSize , y - 6 * tankSize),                          #0
                       (x - int(19.7 * tankSize) , y - int(6 + 3.47 * tankSize)),       #1
                       (x - int(18.79 * tankSize) , y - int(6 + 6.84 * tankSize)),      #2
                       (x - int(17.32 * tankSize) , y - int(6 + 10 * tankSize)),        #3
                       (x - int(15.32 * tankSize) , y - int(6 + 12.86 * tankSize)),     #4
                       (x - int(12.86 * tankSize) , y - int(6 + 15.32 * tankSize)),     #5
                       (x - int(10 * tankSize) , y - int(6 + 17.32 * tankSize)),        #6
                       (x - int(6.84 * tankSize) , y - int(6 + 18.79 * tankSize)),      #7
                       (x - int(3.47 * tankSize) , y - int(6 + 19.7 * tankSize)),       #8
                       (x, y - (6 + 20 * tankSize))]                                          #9


    #canonline
    pygame.draw.line(gameDisplay,
                     green,
                     (x, y - tankSize * 6),
                     possibleTurrets[TurretPosition],
                     turretWidth)
    #turret
    pygame.draw.circle(gameDisplay, green, (x, y), int(tankHeight/1.5))
    #tires
    startX = 15
    for a in range(7):
        pygame.draw.circle(gameDisplay, black, (x - startX, y + tankHeight), wheelWidth)
        startX -= 5
    #body
    pygame.draw.rect(gameDisplay,
                 green,
                 (int(x - (tankWidth / 2)),
                 y,
                 tankWidth,
                 tankHeight))

    return possibleTurrets[TurretPosition]


def enemy_tank(x,y, TurretPosition = 0):
    x = int(x)
    y = int(y)
    
    if enemy_level == 10:
        tank_color = black
    else:
        tank_color = red
                                                                                        #Positions:
    possibleTurrets = [(x + 20 * tankSize , y - 6 * tankSize),                          #0
                       (x + int(19.7 * tankSize) , y - int(6 + 3.47 * tankSize)),       #1
                       (x + int(18.79 * tankSize) , y - int(6 + 6.84 * tankSize)),      #2
                       (x + int(17.32 * tankSize) , y - int(6 + 10 * tankSize)),        #3
                       (x + int(15.32 * tankSize) , y - int(6 + 12.86 * tankSize)),     #4
                       (x + int(12.86 * tankSize) , y - int(6 + 15.32 * tankSize)),     #5
                       (x + int(10 * tankSize) , y - int(6 + 17.32 * tankSize)),        #6
                       (x + int(6.84 * tankSize) , y - int(6 + 18.79 * tankSize)),      #7
                       (x + int(3.47 * tankSize) , y - int(6 + 19.7 * tankSize)),       #8
                       (x, y - (6 + 20 * tankSize))]                                          #9


    pygame.draw.line(gameDisplay,
                     tank_color,
                     (x, y - tankSize * 6),
                     possibleTurrets[TurretPosition],
                     turretWidth)
    pygame.draw.circle(gameDisplay, tank_color, (x, y), int(tankHeight/1.5))
    
    startX = 15
    for a in range(7):
        pygame.draw.circle(gameDisplay, black, (x - startX, y + tankHeight), wheelWidth)
        startX -= 5
    pygame.draw.rect(gameDisplay,
                 tank_color,
                 (int(x - (tankWidth / 2)),
                 y,
                 tankWidth,
                 tankHeight))

    return possibleTurrets[TurretPosition]

def explosion(impactPos):
    """Draws an explosion at impact that yields many damage values"""
    
    explode = True

    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        

        colorChoices = [red, light_red, yellow, light_yellow]

        magnitude = 1

        #sound effect
        if not player_channel1.get_busy():
            player_channel1.play(explosion_sound)
            player_channel1.set_volume(1,0)
        elif not enemy_channel1.get_busy():
            enemy_channel1.play(explosion_sound)
            enemy_channel1.set_volume(0,1)
        else:
            pygame.mixer.Sound.play(explosion_sound)
        
        while magnitude < 50:
            exploding_bit_xy = (impactPos[0] + random.randint(-1 * magnitude, magnitude),
                                (impactPos[1]- tankHeight) + random.randint(-1 * magnitude,
                                                                            magnitude))

            power = random.randint(1,5)
            
            #drawing
            pygame.draw.circle(gameDisplay,
                               colorChoices[random.randrange(0,4)],
                               exploding_bit_xy,
                               power)
            magnitude += 1
            yield power * 0.6, exploding_bit_xy

            pygame.display.update()
            clock.tick(100)

        explode = False
    clock.tick(2)

def e_fireShell(initialPos, tankx, tanky, #turPos,
                barrier_xlocation, barrierWidth, randomHeight,
                pTankX, pTankY, pTurPos,
                pHealth, health):

    """Fires an enemy bullet that hits the player if possible.

    Also returns the landing position of the bullet."""

    foundPower = False
    if enemy_level < 5:
        turPos = 0
    else:
        turPos = 9
        
    while not foundPower:
        currentPower = 0
        if enemy_level < 5:
            if turPos == 8:
                currentPower = 100
                break
            turPos += 1
        else:
            if turPos == 0:
                currentPower = 100
                break
            turPos -= 1

        draw_background()
        initialPos = enemy_tank(tankx, tanky, turPos)

        #drawing
        tank(pTankX, pTankY, pTurPos)
        barrier(barrier_xlocation, randomHeight, barrierWidth)
        ground()
        health_bars(pHealth, health)
        power_meter()
        pygame.display.update()
        clock.tick(5)
        while currentPower < 100 and not foundPower:
            currentPower += 1
                
            fire = True

            #parameters
            velocity = currentPower
            g = 9.81
            TurretAngleRad = (10 * turPos)/(360) * 2 * math.pi
                
            Shell_Thickness = 5
            time = 0
            
            lInitialPos = list(initialPos)
            ShellPos = list(initialPos)
            
            height0 = display_height - lInitialPos[1]
            
            while fire:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p :
                            pause()

                time += 0.1
                ShellPos[0] = lInitialPos[0] + int(time * velocity * math.cos(TurretAngleRad))
                ShellPos[1] = display_height - int(height0 + velocity * math.sin(TurretAngleRad) * time
                                                -0.5 * g * time**2)

##                pygame.draw.circle(gameDisplay, red, (ShellPos[0], ShellPos[1]), Shell_Thickness)
##                pygame.display.update()
                if ((ShellPos[1] >= (display_height - ground_height))
                    or (ShellPos[0] <= barrier_xlocation + barrierWidth * 0.5
                    and ShellPos[0] >= barrier_xlocation - 0.5 * barrierWidth
                    and ShellPos[1] <= display_height
                    and ShellPos[1] >= display_height - randomHeight)
                    or ShellPos[1] >= (pTankY)
                    and ShellPos[0] >= pTankX - tankWidth/2):
                        if pTankX-tankWidth/4 < ShellPos[0] < pTankX + tankWidth/4:
                            #print(pTankX, tankWidth, ShellPos[0])
                            foundPower = True
                            clock.tick(2)
                        fire = False
    fire = True

    #parameters
    if enemy_level > 10:
        this_enemy_level = 10
    else:
        this_enemy_level = enemy_level
    randomPower = random.randint(int(currentPower * (1 - 0.025 * (10 - this_enemy_level))),
                                 int(currentPower * (1 + 0.025 * (10 - this_enemy_level))))
    velocity = randomPower
    #print(velocity, currentPower)
    g = 9.81
    TurretAngleRad = (10 * turPos)/(360) * 2 * math.pi
        
    Shell_Thickness = 5
    time = 0
    
    lInitialPos = list(initialPos)
    ShellPos = list(initialPos)
    
    height0 = display_height - lInitialPos[1]

    #Sound Effect
    #player_channel0.fadeout(5000)
    #player_channel1.fadeout(5000)
    enemy_channel0.play(fire_sound)
    enemy_channel0.set_volume(1,0)
    #print(enemy_channel0.get_volume())
    
    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused()

        pygame.draw.circle(gameDisplay, red, (ShellPos[0], ShellPos[1]), Shell_Thickness)

        time += 0.1
        ShellPos[0] = lInitialPos[0] + int(time * velocity * math.cos(TurretAngleRad))
        ShellPos[1] = display_height - int(height0 + velocity * math.sin(TurretAngleRad) * time
                                        -0.5 * g * time**2)

        if ((ShellPos[1] >= (display_height - ground_height))
            or (ShellPos[0] <= barrier_xlocation + barrierWidth * 0.5
            and ShellPos[0] >= barrier_xlocation - 0.5 * barrierWidth
            and ShellPos[1] <= display_height
            and ShellPos[1] >= display_height - randomHeight)
            or ShellPos[1] >= (pTankY)
            and pTankX + tankWidth/2 >= ShellPos[0] >= pTankX - tankWidth/2 ):
                return ShellPos
                fire = False    

        pygame.display.update()
        clock.tick(flow(velocity))

                             
def fireShell(initialPos, tankx, tanky, turPos,
              enemyTankX, enemyTankY,
              barrier_xlocation, barrierWidth, randomHeight):

    fire = True

    #parameters
    velocity = power_meter(True)
 
    g = 9.81
    TurretAngleRad = (180 - (10 * turPos))/(360) * 2 * math.pi
    Shell_Thickness = 5
    
    time = 0
    damage = 0
    
    lInitialPos = list(initialPos)
    ShellPos = list(initialPos)
    
    height0 = display_height - lInitialPos[1]

    #Sound Effect
    player_channel0.play(fire_sound)
    player_channel0.set_volume(0,1)
    #print(player_channel0.get_volume())
    
    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p :
                        pause()

        pygame.draw.circle(gameDisplay, red, (ShellPos[0], ShellPos[1]), Shell_Thickness)

        time += 0.1
        ShellPos[0] = lInitialPos[0] + int(time * velocity * math.cos(TurretAngleRad))
        ShellPos[1] = display_height - int(height0 + velocity * math.sin(TurretAngleRad) * time
                                        -0.5 * g * time**2)

        if ((ShellPos[1] >= (display_height - ground_height))
            or (ShellPos[0] <= barrier_xlocation + barrierWidth * 0.5
            and ShellPos[0] >= barrier_xlocation - 0.5 * barrierWidth
            and ShellPos[1] <= display_height
            and ShellPos[1] >= display_height - randomHeight)
            or ShellPos[1] >= (enemyTankY)
            and enemyTankX - tankWidth/2 <= ShellPos[0] <= enemyTankX + tankWidth/2):
            return ShellPos
            fire = False  

        pygame.display.update()
        clock.tick(flow(velocity))
    
def flow(velocity):
    return (velocity/3 + 60)


def power_meter(active = False):
    
    bar_length_max = display_width * 0.29
    if active:
        bar_length = random.randint(0, int(bar_length_max))
    else:
        bar_length = 0
    isIncreasing = True
    
    pygame.draw.rect(gameDisplay,
                     black,
                     (display_width * 0.35,
                      display_height * 0.08,
                      display_width * 0.3,
                      display_height * 0.1))
    pygame.draw.rect(gameDisplay,
                     white,
                     (display_width * 0.359,
                      display_height * 0.085,
                      bar_length_max,
                      display_height * 0.09))

    while active:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return ((bar_length / (bar_length_max)) * 100)
                
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        pygame.draw.rect(gameDisplay,
                     white,
                     (display_width * 0.359,
                      display_height * 0.085,
                      bar_length_max,
                      display_height * 0.09))

        #incrementing    
        if bar_length >= 1 and isIncreasing:
            bar_length += bar_length_max/100
        elif bar_length <= bar_length_max and not isIncreasing:
            bar_length -= bar_length_max/100

        #edge detection
        if bar_length < 1:
            bar_length = 1
            isIncreasing = True
        elif bar_length > bar_length_max:
            bar_length = bar_length_max
            isIncreasing = False

        #drawing the bar
        pygame.draw.rect(gameDisplay,
                         green,
                         (display_width * 0.359,
                          display_height * 0.085,
                          bar_length,
                          display_height * 0.09))

        clock.tick(100)
        pygame.display.update()

    textSurf, textRect = text_objects("Power", red, "small")
    textRect.center = (display_width * 0.35 + (display_width * 0.3 / 2),
                       display_height * 0.08 + (display_height * 0.1 / 2))
    gameDisplay.blit(textSurf, textRect)
 
    
def score(score) :
    text = smallfont.render("Score: " + str (score), True, black)
    gameDisplay.blit(text, [display_width * 0.05, display_height * 0.05])

def health_bars(player_health, enemy_health):
    '''Updates Healthbars.

    Clears and redraws the healthbars
    of both the player and the enemy tank'''

    player_health_color = white
    enemy_health_color = white
##    stopwatch = time.perf_counter()
    
    if player_health > 75:
        player_health_color = green
    elif player_health > 40:
        player_health_color = yellow
##    #blinking effect
##    elif stopwatch % 0.7 < 0.4 or player_health <= 0:
##        player_health_color = white
    elif player_health > 0:
        player_health_color = red

    if enemy_health > 75:
        enemy_health_color = green
    elif enemy_health > 40:
        enemy_health_color = yellow
##    elif stopwatch % 0.7 < 0.4 or enemy_health <= 0:
##        enemy_health_color = white
    elif player_health > 0:
        enemy_health_color = red

    #clearing with white rectangles
    pygame.draw.rect(gameDisplay, white, (display_width * 0.8,
                                          display_height * 0.1,
                                          display_width * 0.125,
                                          display_height * 0.05))
    pygame.draw.rect(gameDisplay, white, (display_width * 0.1,
                                          display_height * 0.1,
                                          display_width * 0.125,
                                          display_height * 0.05))

    #drawing health bars
    pygame.draw.rect(gameDisplay, player_health_color, (display_width * 0.8,
                                                       display_height * 0.1,
                                                       player_health,
                                                       display_height * 0.05))
    pygame.draw.rect(gameDisplay, enemy_health_color, (display_width * 0.1,
                                                      display_height * 0.1,
                                                      enemy_health,
                                                      display_height * 0.05))


def pause() :
    paused = True

    gameDisplay.fill(white)
    message_to_screen("Paused",
                      black,
                      -100,
                      size = "large")
    message_to_screen("Press C to continue or Q to quit",
                      black,
                      25)
    pygame.display.update()
    
    while paused:

        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_c :
                    paused = False
                elif event.key == pygame.K_q :
                    pygame.quit()
                    quit()

def game_Intro() :

    theme_music_channel.play(intro_music, -1)
    intro_clicked = False
    
    while not intro_clicked:

        gameDisplay.fill(white)
        message_to_screen("Welcome to Tanks",
                          green,
                          -160,
                          "large")
        message_to_screen("The objective of the game is to shoot and destroy",
                          black,
                          -60)
        message_to_screen("the enemy tank before they destroy you.",
                          black,
                          -20)
        message_to_screen("The more enemies you destroy, the harder they get.",
                          black,
                          20)
        
        intro_clicked = button("play", (display_width/2)-250, 2.8*display_height/4, 100, 50, green, light_green,
               action = "play")
        if not intro_clicked:
            intro_clicked = button("options", (display_width/2)-50, 2.8*display_height/4, 100, 50, yellow, light_yellow,
                   action = "options")
        button("quit", (display_width/2)+150, 2.8*display_height/4, 100, 50, red, light_red,
               action = "quit")

        pygame.display.update()
        clock.tick(10)


        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                quit()

def game_Options():
    clicked = False

    while not clicked:

        gameDisplay.fill(white)
        message_to_screen("Options",
                          yellow,
                          -120,
                          "large")
        message_to_screen("Fire: Spacebar",
                          black,
                          -30)
        message_to_screen("Move Turret: Up and Down arrows",
                          black,
                          10)
        message_to_screen("Move Tank: Left and Right arrows",
                          black,
                          50)
        message_to_screen("Pause: P",
                          black,
                          90)

        clicked = button("play", (display_width/2)-250, 500, 100, 50, green, light_green,
               action = "play")
        button("quit", (display_width/2)+150, 500, 100, 50, red, light_red,
               action = "quit")
       
        pygame.display.update()
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
def game_Loop() :
    
    FPS = 50
    winner = None

    #theme music
    theme_music_channel.play(theme_music, -1)
    
    #tankparameters
    mainTankX = display_width * 0.9
    mainTankY = display_height * 0.9
    tankMove = 0
    tankSpeed = 1
    turretPosition = 0
    moveDirection = None
    leftKeyPressed = False
    rightKeyPressed = False
    player_health = 100

    #enemy Tank
    enemyTankX = display_width * 0.1
    enemyTankY = display_height * 0.9
    enemyTurretPosition = 0
    enemy_health = 20 + 8 * enemy_level
    enemyStepLength = display_width * 0.00625

    #barrierparameters
    barrier_xlocation = int(display_width / 2) + random.randint(-0.2 * display_width, 0.2 * display_width)
    randomHeight = random.randint(display_height * 0.1, display_height * 0.6)
    barrierWidth = random.randint(int(display_width * 0.025), int(display_width * 0.0625))

    #first screen
    gameDisplay.fill(white)
    if enemy_level == 10:
        message_to_screen("Final Level", black, 0, "large")
    else:
        message_to_screen("Level " + str(enemy_level), black, 0, "large")
    pygame.display.update()
    clock.tick(0.5)
        
    while True :
        
        #event handling
        for event in pygame.event.get() :
            #quit event        
            if event.type == pygame.QUIT : 
                quit()

##            if event.type == pygame.MOUSEBUTTONDOWN:
##                global enemy_level
##                if event.button == 1:
##                    enemy_level += 1
##                if event.button == 3:
##                    enemy_level -= 1
##                print(enemy_level)

            if event.type == pygame.KEYDOWN :

                #left and right
                if event.key == pygame.K_LEFT: #and moveDirection == None:
                    tankMove = -tankSpeed
                    moveDirection = "left"
                    leftKeyPressed = True
                
                elif event.key == pygame.K_RIGHT: #and moveDirection == None:
                    tankMove = tankSpeed
                    moveDirection = "right"
                    rightKeyPressed = True
                    
                #up and down
                elif event.key == pygame.K_UP and turretPosition < 9:
                    turretPosition += 1

                elif event.key == pygame.K_DOWN and turretPosition > 0:
                    turretPosition -= 1

                #fire
                elif event.key == pygame.K_SPACE:
                    damage = 0 #clearing any previous damage values

                    #stop moving
                    tankMove = 0
                    moveDirection = None
                    leftKeyPressed = False
                    rightKeyPressed = False
                    
                    #player turn shoot
                    ShellPosition = fireShell(gun, mainTankX, mainTankY, turretPosition,
                              enemyTankX, enemyTankY,
                              barrier_xlocation, barrierWidth, randomHeight)
                    explosions = explosion(ShellPosition)
                    for damage, position in explosions:
                        if enemyTankX - tankWidth/2 < position[0] < enemyTankX + tankWidth/2 :
                            #print("HIT")
                            enemy_health -= damage
                            health_bars(player_health, enemy_health)
                            if enemy_health <= 0:
                                break
                    if enemy_health <= 0:
                        break
                            
                    #enemy move
                    possibleDir = ['r','l']
                    moveIndex = random.randrange(2)

                    for x in range(int(random.randrange(display_width/40)* enemyStepLength)):
                        
                        #check for collision with display edge or barrier
                        if enemyTankX - tankWidth/2 <= 0:
                            #print("changeDir")
                            moveIndex = 0
                        elif enemyTankX + tankWidth/2 >= barrier_xlocation - barrierWidth/2:
                            #print("changeDir")
                            moveIndex = 1
                        if possibleDir[moveIndex] == 'l':
                            enemyTankX -= 1
                        else:
                            enemyTankX += 1
                    
                        #drawing
                        draw_background()

                        health_bars(player_health, enemy_health)
                        tank(mainTankX, mainTankY, turretPosition)
                        enemy_gun = enemy_tank(enemyTankX, enemyTankY)
                        barrier(barrier_xlocation, randomHeight, barrierWidth)
                        ground()
                        power_meter(False)
                        pygame.display.update()
                        clock.tick(FPS*1.5)

                    #enemy turn shoot
                    enemyShellPosition = e_fireShell(enemy_gun, enemyTankX, enemyTankY, #turretPosition,
                                                     barrier_xlocation, barrierWidth, randomHeight,
                                                     mainTankX, mainTankY, turretPosition,
                                                     player_health, enemy_health)
                    explosions = explosion(enemyShellPosition)
                    for damage, position in explosions:
                        if mainTankX - tankWidth/2 < position[0] < mainTankX + tankWidth/2:#check position
                            player_health -= damage
                            if player_health <= 0:
                                break
                            health_bars(player_health, enemy_health)


            #Pause event
                elif event.key == pygame.K_p :
                    pause()
                elif event.key == pygame.K_w and wSkip:
                    return "won"
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    leftKeyPressed = False
                    if rightKeyPressed:
                        tankMove = tankSpeed
                        moveDirection = "right"
                    else:
                        tankMove = 0
                        moveDirection = None
                        
                elif event.key == pygame.K_RIGHT:
                    rightKeyPressed = False
                    if leftKeyPressed:
                        tankMove = -tankSpeed
                        moveDirection = "left"
                    else:
                        tankMove = 0
                        moveDirection = None
        
        #Logic
        if player_health <= 0:
            return "lost"
        elif enemy_health <= 0:
            return "won"
            
        mainTankX += tankMove

        if (mainTankX - (tankWidth / 2) < barrier_xlocation - (barrierWidth / 2)  < mainTankX - (tankWidth / 2) + tankWidth
            or barrier_xlocation - (barrierWidth / 2) < mainTankX - (tankWidth / 2) < barrier_xlocation - (barrierWidth / 2) + barrierWidth):
            mainTankX += 5
        if mainTankX - (tankWidth / 2) + tankWidth > display_width:
            mainTankX -= 5 

        #drawing
        gameDisplay.fill(white)
        draw_background()

        health_bars(player_health, enemy_health)
        
        gun = tank(mainTankX, mainTankY, turretPosition)
        enemy_gun = enemy_tank(enemyTankX, enemyTankY, enemyTurretPosition)

        barrier(barrier_xlocation, randomHeight, barrierWidth)
        ground()
        power_meter(False)
        pygame.display.update()
        clock.tick(FPS)

def game_Over() :
    pygame.mixer.fadeout(3000)
    theme_music_channel.queue(game_over_music)
    clicked = False
    
    while not clicked:

        if not theme_music_channel.get_busy():
            theme_music_channel.play(game_over_music, -1)

        gameDisplay.fill(white)
        message_to_screen("Game Over",
                          red,
                          -120,
                          "large")
        message_to_screen("You died.",
                          black,
                          -30)
        
        clicked = button("try again", (display_width/2)-260, 500, 120, 50, green, light_green,
               action = "play")
        if not clicked:
            clicked = button("options", (display_width/2)-50, 500, 100, 50, yellow, light_yellow,
                   action = "options")
        button("quit", (display_width/2)+150, 500, 100, 50, red, light_red,
               action = "quit")

        pygame.display.update()
        clock.tick(10)

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                quit()

def game_Won() :
    clicked = False
    
    while not clicked:

        gameDisplay.fill(white)
        message_to_screen("You Won!",
                          green,
                          -120,
                          "large")
        message_to_screen("Congratulations!",
                          black,
                          -30)
        if enemy_level == 10:
            message_to_screen("You destroyed all 10 Tanks!",
                              black,
                              30)
            if enemy_level >= 10:
                clicked = button("still too easy", (display_width/2)-300, 500, 200, 50, green, light_green,
                   action = "play")
        
        else:
            clicked = button("next level", (display_width/2)-280, 500, 160, 50, green, light_green,
               action = "play")
        if not clicked:
            clicked = button("options", (display_width/2)-50, 500, 100, 50, yellow, light_yellow,
                   action = "options")
        button("quit", (display_width/2)+150, 500, 100, 50, red, light_red,
               action = "quit")

        pygame.display.update()
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode == "\r":
                    global game_status
                    game_status = "loop" 
                    clicked = True
            if event.type == pygame.QUIT :
                pygame.quit()
                quit()


#main
game_status = "intro"

#Game Parameters
enemy_level = 1
wSkip = True #Turn this on if you want to cheat

while True:
    if game_status == "intro":
        game_Intro()
    if game_status == "options":
        game_Options()
    if game_status == "loop":
        pygame.display.set_caption("Tanks - Level " + str(enemy_level))
        game_status = game_Loop()
    if game_status == "won":
        game_Won()
        enemy_level += 1
    if game_status == "lost":
        game_Over()

