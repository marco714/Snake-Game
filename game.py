from config import Config
from snake import Snake
from apple import Apple
import pygame
import sys

class Game():

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
        pygame.display.set_caption('Wormy')
        self.apple = Apple()
        self.snake = Snake()

    def drawGrid(self):

        for x in range(0, Config.WINDOW_WIDTH, Config.CELLSIZE):

            #Vertical Lines
            pygame.draw.line(self.screen, Config.DARKGRAY, (x, 0), (x, Config.WINDOW_HEIGHT))

        for y in range(0, Config.WINDOW_HEIGHT, Config.CELLSIZE):

            #Horizontal Lines
            pygame.draw.line(self.screen, Config.DARKGRAY, (0, y), (Config.WINDOW_WIDTH, y))

    def drawWorm(self):

        for coord in self.snake.wormCoords:
            
            x = coord['x'] * Config.CELLSIZE
            y = coord['y'] * Config.CELLSIZE

            wormSegmentRect = pygame.Rect(x, y, Config.CELLSIZE, Config.CELLSIZE)
            pygame.draw.rect(self.screen, Config.DARKGREEN, wormSegmentRect)

            wormInnerSegmentRect = pygame.Rect(x+4, y+4, Config.CELLSIZE - 8, Config.CELLSIZE - 8)
            pygame.draw.rect(self.screen, Config.GREEN, wormInnerSegmentRect)
    def drawApple(self):
        x = self.apple.x * Config.CELLSIZE
        y = self.apple.y * Config.CELLSIZE

        appleSegmentRect = pygame.Rect(x, y, Config.CELLSIZE, Config.CELLSIZE)

        pygame.draw.rect(self.screen, Config.RED, appleSegmentRect)
    
    def drawScore(self, score):
        scoreSurf = self.BASICFONT.render('Score: %s' % (score), True, Config.WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (Config.WINDOW_WIDTH - 120, 10)
        self.screen.blit(scoreSurf, scoreRect)
    def draw(self):

        self.screen.fill(Config.BG_COLOR)

        #in here we will draw our snake grid apple score
        self.drawGrid()
        self.drawWorm()
        self.drawApple()
        self.drawScore(len(self.snake.wormCoords) - 3)
        pygame.display.update()
        self.clock.tick(Config.FPS)

    def handleKeyEvents(self, event):
        if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.snake.direction != self.snake.RIGHT:
            self.snake.direction = self.snake.LEFT
        elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.snake.direction !=self.snake.LEFT:
            self.snake.direction = self.snake.RIGHT
        elif (event.key == pygame.K_UP or event.key == pygame.K_w) and self.snake.direction != self.snake.DOWN:
            self.snake.direction = self.snake.UP
        elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.snake.direction != self.snake.UP:
            self.snake.direction = self.snake.DOWN
        elif event.key == pygame.K_ESCAPE:
            pygame.quit()

    def resetGame(self):
        del self.snake
        del self.apple

        self.snake = Snake()
        self.apple = Apple()

        return True
    def isGameOver(self):
        if (self.snake.wormCoords[self.snake.HEAD]['x'] == -1 or self.snake.wormCoords[self.snake.HEAD]['x'] == Config.CELLWIDTH or self.snake.wormCoords[self.snake.HEAD]['y'] == -1 or self.snake.wormCoords[self.snake.HEAD]['y'] == Config.CELLHEIGHT):

            return self.resetGame()


        for wormBody in self.snake.wormCoords[1:]:

            if wormBody['x'] == self.snake.wormCoords[self.snake.HEAD]['x'] and wormBody['y'] == self.snake.wormCoords[self.snake.HEAD]['y']:
                return self.resetGame()
    def checkForKeyPress(self):

        if len(pygame.event.get(pygame.QUIT)) > 0:
            pygame.quit()
        
        keyUpEvents = pygame.event.get(pygame.KEYUP)

        if len(keyUpEvents) == 0:
            return None
        
        if keyUpEvents[0].key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
    def drawPressKeyMsg(self):
        pressKeySurf = self.BASICFONT.render('Press a key to play. ', True, Config.DARKGRAY)
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.topleft = (Config.WINDOW_WIDTH - 200, Config.WINDOW_HEIGHT -30)

        self.screen.blit(pressKeySurf,pressKeyRect)
    def displayGameOver(self):
        gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
        gameSurf = gameOverFont.render('Game', True, Config.WHITE)
        overSurf = gameOverFont.render('Over', True, Config.WHITE)

        gameRect = gameSurf.get_rect()
        overRect = overSurf.get_rect()

        gameRect.midtop = (Config.WINDOW_WIDTH / 2, 10)
        overRect.midtop = (Config.WINDOW_WIDTH / 2, gameRect.height + 10 + 25)

        self.screen.blit(gameSurf, gameRect)
        self.screen.blit(overSurf, overRect)

        self.drawPressKeyMsg()
        pygame.display.update()
        pygame.time.wait(500)

        self.checkForKeyPress()

        while True:
            if self.checkForKeyPress():
                pygame.event.get() #Cleat event queue
                return


    def run(self):

        while True:
            self.gameLoop()
            self.displayGameOver()
    def gameLoop(self):

        while True:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.handleKeyEvents(event)

            self.snake.update(self.apple)
            self.draw()

            if self.isGameOver():
                break