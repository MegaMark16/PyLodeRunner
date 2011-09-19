import pygame, sys, random
from pygame.locals import *

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# set up the window
WINDOWWIDTH = 400
WINDOWHEIGHT = 400
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Input')

# set up the colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# set up the player and food data structure
GOLD_HEIGHT = 10
GOLD_WIDTH = 20
FLOOR_HEIGHT = 5
player = pygame.Rect(300, 100, 10, 30)

def load_floors(floor_data):
    floors = []
    for floor in floor_data:
        floors.append(pygame.Rect(floor['left'], floor['top'], floor['width'], FLOOR_HEIGHT))
    return floors

floor_data = [
    { 'width' : 200, 'left' : 20, 'top' : 40 },
    { 'width' : 70, 'left' : 200, 'top' : 80 },
    { 'width' : 300, 'left' : 80, 'top' : 300 },
    { 'width' : 100, 'left' : 250, 'top' : 150 },
]

floors = load_floors(floor_data)

gold = []
for i in range(random.randint(5, 10)):
    floor = random.choice(floors)
    left = random.randint(floor.left, floor.left + floor.width)
    gold.append(pygame.Rect(left, floor.top - GOLD_HEIGHT, GOLD_WIDTH, GOLD_HEIGHT))

# set up movement variables
moveLeft = False
moveRight = False
moveUp = False
moveDown = False

MOVESPEED = 6


# run the game loop
while True:
    # check for events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            # change the keyboard variables
            if event.key == K_LEFT or event.key == ord('a'):
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == ord('d'):
                moveLeft = False
                moveRight = True
            if event.key == K_UP or event.key == ord('w'):
                moveDown = False
                moveUp = True
            if event.key == K_DOWN or event.key == ord('s'):
                moveUp = False
                moveDown = True
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == ord('a'):
                moveLeft = False
            if event.key == K_RIGHT or event.key == ord('d'):
                moveRight = False
            if event.key == K_UP or event.key == ord('w'):
                moveUp = False
            if event.key == K_DOWN or event.key == ord('s'):
                moveDown = False
            if event.key == ord('x'):
                player.top = random.randint(0, WINDOWHEIGHT - player.height)
                player.left = random.randint(0, WINDOWWIDTH - player.width)

        if event.type == MOUSEBUTTONUP:
            gold.append(pygame.Rect(event.pos[0], event.pos[1], GOLD_WIDTH, GOLD_HEIGHT))

    #if gold >= NEWFOOD:
        # add new food
        #gold.append(pygame.Rect(random.randint(0, WINDOWWIDTH - GOLD_WIDTH), random.randint(0, WINDOWHEIGHT - GOLD_HEIGHT), GOLD_WIDTH, GOLD_HEIGHT))

    # draw the black background onto the surface
    windowSurface.fill(BLACK)

    # move the player
    if moveDown and player.bottom < WINDOWHEIGHT:
        player.top += MOVESPEED
    if moveUp and player.top > 0:
        player.top -= MOVESPEED
    if moveLeft and player.left > 0:
        player.left -= MOVESPEED
    if moveRight and player.right < WINDOWWIDTH:
        player.right += MOVESPEED

    # draw the player onto the surface
    pygame.draw.rect(windowSurface, WHITE, player)

    # check if the player has intersected with any food squares.
    for brick in gold[:]:
        if player.colliderect(brick):
            gold.remove(brick)

    # draw the food
    for i in range(len(gold)):
        pygame.draw.rect(windowSurface, GREEN, gold[i])
    
    for floor in floors:
        pygame.draw.rect(windowSurface, WHITE, floor)
    
    # draw the window onto the screen
    pygame.display.update()
    mainClock.tick(40)
