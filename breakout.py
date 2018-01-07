import pygame, sys, os
from pygame.locals import *
from pygame import gfxdraw
from random import choice,randint

DARKGRAY = (50,50,50)
LIGHTGRAY = (150,150,150)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)
ORANGE = (255,128,0)
WHITE = (255,255,255)
PURPLE = (128,0,128)

BGCOLOR = DARKGRAY
PADDLECOLOR = BLUE
BALLCOLOR = LIGHTGRAY

PADDLEY = 350
SPAWNCHANCE = 35 # the odds that a ball will spawn another ball on contact
def setup():
    global DISPLAYSURF,font,FPSCLOCK,FPS,paddleX,balls,lives,score,callback,renderMode
    
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    pygame.mixer.music.load('bounce.wav')

    # centers pygame screen in window
    # note - must be done before creating pygame window
    os.environ["SDL_VIDEO_CENTERED"] = "1"

    DISPLAYSURF = pygame.display.set_mode((800,400))
    pygame.display.set_caption("Breakout")
    font = pygame.font.Font('Roboto-Medium.ttf', 30)

    FPSCLOCK = pygame.time.Clock()
    FPS = 150 # wow

    mousex,mousey = pygame.mouse.get_pos()
    paddleX = mousex
    
    reset()
    
    lives = 3
    score = 0
    
    build() # # setup the bricks

    # this 2d list contains callbacks - just to keep track
    # of what has to happen
    # in many occasions, there are short pauses before the game does something
    # so, instead of time.sleep(), we are keeping track of frames
    # when something needs to be done, the function is kept in the list along
    # with the number of frames from now it has to be done
    # when the main loop runs, it decrements the frames, until 0 - when it calls it
    callback = []

    # we also keep track of what we are rendering
    renderMode = 1


# setup the bricks
def build():
    global bricks
    bricks = []
    # each brick has this info: color,x,y,width,height,speed when touched by ball,
    # points scored when broken, and spawns another ball or not when broken
    bricks.extend((RED,x,100,50,10,1,50,randint(0,SPAWNCHANCE)) for x in range(0,800,50))
    bricks.extend((ORANGE,x,110,50,10,1,50,randint(0,SPAWNCHANCE)) for x in range(0,800,50))
    bricks.extend((YELLOW,x,120,50,10,1,40,randint(0,SPAWNCHANCE)) for x in range(0,800,50))
    bricks.extend((GREEN,x,130,50,10,1,30,randint(0,SPAWNCHANCE)) for x in range(0,800,50))
    bricks.extend((BLUE,x,140,50,10,1,20,randint(0,SPAWNCHANCE)) for x in range(0,800,50))
    bricks.extend((PURPLE,x,150,50,10,1,10,randint(0,SPAWNCHANCE)) for x in range(0,800,50))

def reset():
    global balls,paddleX,PADDLEY,renderMode
    PADDLEY = 350

    # there are multiple balls
    # we start out with one
    # the ball contains centerX,centerY,velocity X, and velocity Y
    balls = [[200,200,1,-1]]

    renderMode = 1
    
def sign(n):
    if n > 0:
        return 1
    else:
        return -1

def render(mode):
    if not DISPLAYSURF:
        return
    DISPLAYSURF.fill(BGCOLOR)   # first clear the screen
    
    # finished(breakout) render mode - draw the rainbow, score, lives, and breakout text
    if mode == 0:
        # draw the rainbow
        pygame.draw.rect(DISPLAYSURF,RED,(0,100,800,10))
        pygame.draw.rect(DISPLAYSURF,ORANGE,(0,110,800,10))
        pygame.draw.rect(DISPLAYSURF,YELLOW,(0,120,800,10))
        pygame.draw.rect(DISPLAYSURF,GREEN,(0,130,800,10))
        pygame.draw.rect(DISPLAYSURF,BLUE,(0,140,800,10))
        pygame.draw.rect(DISPLAYSURF,PURPLE,(0,150,800,10))

        # display lives text
        livesSurface = font.render("LIVES: " + str(lives), True, WHITE)
        DISPLAYSURF.blit(livesSurface,(650,10))

        # display breakout text
        breakoutSurfaceSize = font.size("BREAKOUT!")
        breakoutSurface = font.render("BREAKOUT!", True, WHITE)
        DISPLAYSURF.blit(breakoutSurface,(400-breakoutSurfaceSize[0]/2,200-breakoutSurfaceSize[1]/2))

        # display the score
        scoreSurface = font.render(str(score), True, WHITE)
        DISPLAYSURF.blit(scoreSurface,(10,10))
    
    # regular render mode - draw the bricks, paddle, and all the balls
    elif mode == 1:
        # draw the paddle
        pygame.draw.rect(DISPLAYSURF,PADDLECOLOR,(paddleX,PADDLEY,150,10))

        # draw the balls
        for ball in balls:
            # pygame.draw.circle(DISPLAYSURF,BALLCOLOR,(int(ball[0]),int(ball[1])),8)
            gfxdraw.filled_circle(DISPLAYSURF, int(ball[0]), int(ball[1]), 8, BALLCOLOR)
            gfxdraw.aacircle(DISPLAYSURF, int(ball[0]), int(ball[1]), 8, BALLCOLOR)
            

        # display lives text
        livesSurface = font.render("LIVES: " + str(lives), True, WHITE)
        DISPLAYSURF.blit(livesSurface,(650,10))

        # display the score text
        scoreSurface = font.render(str(score), True, WHITE)
        DISPLAYSURF.blit(scoreSurface,(10,10))

        # draw the bricks
        for brick in bricks:
            pygame.draw.rect(DISPLAYSURF,brick[0],(brick[1],brick[2],brick[3],brick[4]))

    # game over mode - draw game over text and score
    elif mode == 2:
        # display the game over text
        gameOverSurfaceSize = font.size("GAME OVER")
        gameOverSurface = font.render("GAME OVER", True, WHITE)
        DISPLAYSURF.blit(gameOverSurface,(400-gameOverSurfaceSize[0]/2,200-gameOverSurfaceSize[1]/2))
                    
        # display the score text
        scoreText = "SCORE: " + str(score)
        scoreSurfaceSize = font.size(scoreText)
        scoreSurface = font.render(scoreText, False, WHITE)
        DISPLAYSURF.blit(scoreSurface,(400-scoreSurfaceSize[0]/2,250-scoreSurfaceSize[1]/2))
        
    pygame.display.update()

# quit the program  
def terminate():
    terminated = True
    pygame.quit()
    sys.exit()
    
# check for ball contact with the paddle
def contactPaddle(i):
    if balls[i][1] == PADDLEY - 8 and balls[i][0] >= paddleX and balls[i][0] <= paddleX + 150:
        pygame.mixer.music.play(0)
        balls[i][3] *= -1
    elif (balls[i][0] == paddleX - 8 or balls[i][0] == paddleX + 8) and balls[i][1] >= PADDLEY and balls[i][1] <= PADDLEY + 10:
        pygame.mixer.music.play(0)
        balls[i][2] *= -1

# check for ball contact with the 3 walls - right, left, and top
def contactWall(i):
    if balls[i][0] <= 8 or balls[i][0] >= 792:
        pygame.mixer.music.play(0)
        balls[i][2] *= -1
    if balls[i][1] <= 8:
        pygame.mixer.music.play(0)
        balls[i][3] *= -1

# check for ball contact with a brick
def contactBricks(i):
    global bricks,balls,score
    for brick in bricks:
        if balls[i][0] >= brick[1] and balls[i][0] <= brick[1] + brick[3] and (balls[i][1] == brick[2] - 8 or balls[i][1] == brick[2] + brick[4]+8):
            pygame.mixer.music.play(0)
            balls[i][2] = sign(balls[i][2]) * brick[5]
            balls[i][3] = sign(balls[i][3]) * brick[5] * -1
            score += brick[6]
            if not brick[7]:
                balls.append([balls[i][0],balls[i][1],sign(balls[i][2])*0.5*-1,sign(balls[i][3])*0.5])
            bricks.remove(brick)
        elif balls[i][1] >= brick[2] and balls[i][1] <= brick[2] + brick[4] and (balls[i][1] == brick[1] - 8 or balls[i][0] == brick[1] + brick[3] + 8):
            pygame.mixer.music.play(0)
            balls[i][2] = sign(balls[i][2]) * brick[5] * -1
            balls[i][3] = sign(balls[i][3]) * brick[5]
            score += brick[6]
            if not brick[7]:
                balls.append([balls[i][0],balls[i][1],balls[i][2]*-1,balls[i][3]])
            bricks.remove(brick)
            
# check for ball contact with void at bottom, which means death of that ball
def contactVoid(i):
    if balls[i][1] > 408:
        balls.pop(i)

# check for all balls are dead, which means reset or gameover  
def checkDead():
    global callback,renderMode,lives
    
    if len(balls) == 0:
        if lives > 1:
            lives -= 1
            callback.append([reset,300]) # in 300 frames - @ 150 fps, that's 2 seconds
        else:
            renderMode = 2
            callback.append([terminate,300]) # in 300 frames - @ 150 fps, that's 2 seconds

# update position of ball
def updatePos(i):
    balls[i][0] += balls[i][2]
    balls[i][1] += balls[i][3]
        
def updateBalls():
    for i in range(0,len(balls)):
        # we are trying all of this - this ball index may not exist if it is deleted during this function
        try:
            updatePos(i)
            contactPaddle(i)
            contactWall(i)
            contactBricks(i)
            contactVoid(i)
            checkDead()
        except:
            pass

def main():
    global paddleX,renderMode,balls,score
    setup()

    # main game loop   
    while True:
        
        # update ball positions
        updateBalls()

        # check for completion of game
        if len(bricks) == 0 and not any(terminate in sublist for sublist in callback):
            renderMode = 0
            balls = []
            score += lives * 1000
            callback.append([terminate,300]) # in 300 frames - @ 150 fps, that's 2 seconds

        # display the screen
        render(renderMode)

        # event handler - check for 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex,mousey = pygame.mouse.get_pos()
                if mousex < 650:
                    paddleX = mousex

        # random cheat   
        pressed = pygame.key.get_pressed()
        if pressed[K_LEFT] and paddleX > 0:
            paddleX -= 2
        elif pressed[K_RIGHT] and paddleX < 650:
            paddleX += 2
        if pressed[K_RALT] and pressed[K_LSHIFT] and pressed[K_LCTRL] and pressed[K_d] and len(bricks) > 0:
            bricks.remove(choice(bricks))

        # finally, update/execute callbacks
        for cb in callback:
            try:
                if cb[1] <= 0:
                    cb[0]()
                    callback.remove(cb)
                else:
                    cb[1] -= 1
            # one possible function called in callback is terminate(), which
            # calls sys.exit(). This raises a SystemExit by default,
            # which must handled - we just ignore and call it again
            except SystemExit:
                sys.exit()
            except:
                pass

        FPSCLOCK.tick(FPS)


if __name__ == "__main__":
    main()
