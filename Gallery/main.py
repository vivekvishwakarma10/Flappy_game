import random   # Randon for genrating random number
import pygame   # python game lib
from pygame.locals import *     #basic python game lib
import sys      # for exiting the game using sys exit

# generating global variable for the game

FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS  = {}
PLAYER = 'Gallery\Sprites\bird.png'
BACKGROUND = 'Gallery\Sprites\background.png'
PIPE        = 'Gallery\Sprites\pipe.png'

def welcomeScreen():
    """
    shows the welcome image on the screen
    """
    playerx     = int(SCREENWIDTH/5)
    playery     = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex    = int((SCREENWIDTH  - GAME_SPRITES['message'].get_widht())/2)
    messagey    = int(SCREENHEIGHT * 0.13) 
    basex       = 0
    while True:
        for event in pygame.event.get():
            #if user tap on escape close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            #if user tap on space or up key game wil be start
            elif event.type == KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
         
def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # This function will return true if the player is crashed
        if crashTest:
            return     

        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe
       
                

if __name__ == "_main_":
    #this is our main point where our game will start
    pygame.init() #this will initiaze the all module of pygame
    FPSCLOCK = pygame.time.Clock() # for setting time of the game
    pygame.display.set_caption('Flappy game by Vivek vishwakarma') # caption
    GAME_SPRITES['numbers'] = ( 
        pygame.image.load('Gallery\Sprites\0.png').convert_alpha(),
        pygame.image.load('Gallery\Sprites\1.png').convert_alpha(),
        pygame.image.load('Gallery\Sprites\2.png').convert_alpha(),
        pygame.image.load('Gallery\Sprites\3.png').convert_alpha(),
        pygame.image.load('Gallery\Sprites\4.png').convert_alpha(),
        pygame.image.load('Gallery\Sprites\5.png').convert_alpha(),
        pygame.image.load('Gallery\Sprites\6.png').convert_alpha(),
        pygame.image.load('Gallery\Sprites\7.png').convert_alpha(),
        pygame.image.load('Gallery\Sprites\8.png').convert_alpha(),
    )
    GAME_SPRITES['message'] = pygame.image.load('Gallery\Sprites\message.png')
    GAME_SPRITES['base']    = pygame.image.load('Gallery\Sprites\base.png')
    GAME_SPRITES['pipe']    = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )
    GAME_SPRITES['backgound'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player']    = pygame.image.load(PLAYER).convert_alpha()
    #game sounds
    GAME_SOUNDS['die']       = pygame.mixer.Sound('Gallery\Audio\die.mp3')
    GAME_SOUNDS['hit']       = pygame.mixer.Sound('Gallery\Audio\hit.mp3')
    GAME_SOUNDS['point']     = pygame.mixer.Sound('Gallery\Audio\point.mp3')
    GAME_SOUNDS['swoosh']    = pygame.mixer.Sound('Gallery\Audio\swoosh.mp3')
    GAME_SOUNDS['flowing']   = pygame.mixer.Sound('Gallery\Audio\flowing.mp3')

    while True:
        welcomeScreen() # wil show the game screen until not tapped
      #  mainGame()      # main game fnction

