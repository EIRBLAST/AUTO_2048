import pygame
import numpy
import random
import copy

from typing import List

#GOD DAMN WHY IS THERE NO ACTUAL FORMULA FOR THIS
colors = {
    0:(204, 192, 179),
    2:(238, 228, 218),
    4:(237, 224, 200),
    8:(242, 177, 121),
    16:(245, 149, 99),
    32:(246, 124, 95),
    64:(246, 94, 59),
    128:(237, 207, 114),
    256:(237, 204, 97),
    512:(237, 200, 80),
    1024:(237, 197, 63),
    2048:(237, 194, 46),
}


# Initialization of the Game
pygame.init()
pygame.font.init()
pygame.font.get_init()
pygame.key.set_repeat()
width = 1300
height = 700
gameBoard = 600
window = pygame.display.set_mode((width, height)) # Width by Height
score = 0

# Window Initialization
pygame.display.set_caption('2048')
icon = pygame.image.load('favicon.ico')
pygame.display.set_icon(icon)


# Suite of operation on m to make it so that every collapse is like collapsing upward
# undoMatrixOperation(matrixOperations(m)) = m
def matrixOperations(m:numpy.matrix,vector:List[int]):
    move = 1
    if vector[1] == 0:
        m = m.transpose()
        move = 0
    if vector[move] > 0:
        m = numpy.flip(m,axis=0)
        m = numpy.flip(m,axis=1)
    return m
def undoMatrixOperation(m:numpy.matrix,vector:List[int],move):
    if vector[move] > 0:
        m = numpy.flip(m,axis=1)
        m = numpy.flip(m,axis=0)
    if move == 0:
        m = m.transpose()
    return m

# Handle all game operations
class Game:
    def __init__(self, size=4):
        self.board :numpy.matrix = numpy.matrix(numpy.zeros((size,size)))
        self.game_on = True
        self.size = size
        self.score = 0
        self.previous_board = copy.deepcopy(self.board)
    def is_on(self)->bool:
        return self.game_on
    def end(self)->None:
        self.game_on = False
    def draw(self):
        # We draw the board
        line_tickness = 15
        boardSize = gameBoard + line_tickness * (self.size)
        BoardXcoord,BoardYcoord = (width-boardSize)/2,(height - boardSize)/2
        pygame.draw.rect(window,(255,187,51),(BoardXcoord,BoardYcoord,boardSize,boardSize))
        for i in range(self.size+1):
            pygame.draw.rect(window,(127,127,127),(BoardXcoord + (i/(self.size))*boardSize,BoardYcoord,line_tickness,boardSize))
            pygame.draw.rect(window,(127,127,127),(BoardXcoord,BoardYcoord + (i/(self.size))*boardSize,boardSize+line_tickness,line_tickness))
        
        # We draw the tiles
        for x in range(self.size):
            for y in range(self.size):
                
                value = self.board[x, y]
                color = colors.get(value,(0,0,0))
                if color == (0,0,0):
                    text_color = (255,255,255)
                else:
                    text_color = (0,0,0)
                if value != 0:
                    font = pygame.font.SysFont('ClearSans-Bold.ttf', 50)
                    text = font.render(f'{int(value)}', True, text_color)
                    text_rect = text.get_rect()
                
                dx = x/(self.size)*boardSize
                dy = y/(self.size)*boardSize
                
                tile = pygame.Rect(BoardXcoord+dx +line_tickness,BoardYcoord+dy+line_tickness,(boardSize/self.size) - line_tickness,(boardSize/self.size) - line_tickness)
                if value != 0:
                    text_rect.center = tile.center
                pygame.draw.rect(window,color,tile)
                if value != 0:
                    window.blit(text,text_rect)
        # Display the score
        text1 = font.render('Score:', True, text_color)
        text2 = font.render(f'{int(score)}', True, text_color)
        text_rect1 = text1.get_rect()
        text_rect2 = text2.get_rect()
        text_rect1.center = (BoardXcoord/2,BoardYcoord + (boardSize/2))
        text_rect2.center = (BoardXcoord/2,BoardYcoord + 50 + (boardSize/2))
        window.blit(text1,text_rect1)
        window.blit(text2,text_rect2)
    def update(self, x_move, y_move):
        self.previous_board = copy.deepcopy(self.board)
        # We draw what needs to be drawn to the screen
        self.draw()
        # We do nothing if we have no moovement input
        if [x_move, y_move] == [0, 0]:
            return
        # We check if we can moove in this direction
        if not self.can_move([x_move, y_move]):
            return
        # We merge What can be merged
        self.board = self.merge([x_move, y_move])
        # We add a new tile after merging and end the game if we can't
        if (self.previous_board != self.board).any():
            self.add_new_tile()
    def merge(self, vector: List[int])->numpy.matrix:
        global score
        calcboard = copy.deepcopy(self.board)
        #Mat Operation normalize the grid to the disired moovement
        calcboard = matrixOperations(calcboard,vector)
        #At this point all operations are normalized to collapsing upward
        
        #We collapse every tile at the top
        for x in range(self.size):
            for y in range(1,self.size):
                i = y
                while i > 0:
                    if calcboard[x,i-1] == 0:
                        calcboard[x, i-1], calcboard[x, i] = calcboard[x, i], calcboard[x, i-1]
                    else:
                        break
                    i -= 1
        #We merge the needed tile
        for x in range(self.size):
            for y in range(1,self.size):
                if calcboard[x,y] == calcboard[x, y-1]:
                    calcboard[x, y-1] = 2*calcboard[x,y]
                    score += 2*calcboard[x,y]
                    if y == self.size -1:
                        calcboard[x,y] = 0
                    else:
                        calcboard[x, y]  = calcboard[x ,y+1]
                        calcboard[x, y+1] = 0
        # We collapse again
        for x in range(self.size):
            for y in range(1,self.size):
                i = y
                while i > 0:
                    if calcboard[x,i-1] == 0:
                        calcboard[x, i-1], calcboard[x, i] = calcboard[x, i], calcboard[x, i-1]
                    else:
                        break
                    i -= 1
        calcboard = undoMatrixOperation(calcboard,vector,not(vector[0] | 0))
        return calcboard
    def can_move(self, vector: List[int])->bool:
        calcboard = copy.deepcopy(self.board)
        calcboard = matrixOperations(calcboard,vector)
        for x in range(self.size):
            for y in range(1,self.size):
                if (calcboard[x, y-1] == 0 and calcboard[x, y] != 0) or calcboard[x, y-1] == calcboard[x, y]:
                    return True
        return False
    def add_new_tile(self)->bool:
        # New tile are either 4 or 2
        value = random.choices([2.0, 4.0], [0.9, 0.1])[0]
        positions = []
        # We add free spaces into a list
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x, y] == 0:
                    positions.append([x, y])
        # If there are no free tile the game has ended
        if positions == []:
            self.end()
            return False
        # Add the new tile
        position = random.choices(positions)[0]
        self.board[position[0], position[1]] = value
        return True


game = Game(size=4)
game.add_new_tile()
game.add_new_tile()
while game.is_on():
    window.fill((255, 225, 255))
    vector = [0, 0]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.end()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                vector = [0, -1]
            elif event.key == pygame.K_DOWN:
                vector = [0, 1]
            elif event.key == pygame.K_RIGHT:
                vector = [1, 0]
            elif event.key == pygame.K_LEFT:
                vector = [-1, 0]
            elif event.key == pygame.K_ESCAPE:
                game.end()
            elif event.key == pygame.K_r:
                game.board = numpy.matrix(numpy.zeros((game.size,game.size)))
                score = 0
                game.add_new_tile()
                game.add_new_tile()
    
    game.update(vector[0], vector[1])
    pygame.display.update()
