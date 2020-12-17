import pygame

RED = (255,0,0)
BLACK = (0,0,0)


def get_square_under_mouse(gameboard):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    x, y = [int(v // 80) for v in mouse_pos]
    # print(x, y)
    try:
        if x >= 0 and y >= 0: return (gameboard[x][y], x, y)
    except IndexError:
        pass
    return None, None, None


class Piece:
    def __init__(self, colour, name):
        self.name = name
        self.position = None
        self.colour = colour

    def getname(self):
        return self.name

    def getcolour(self):
        if self.colour == RED:
            return 255, 0, 0
        else:
            return 0, 0, 0

class Empty(Piece):
    def move(self, x, y, nx, ny):
        return True

class General(Piece):
    def move(self, x, y, nx, ny):
        return True

class Advisor(Piece):
    def move(self, x, y, nx, ny):
        return True


class Elephant(Piece):
    def move(self, x, y, nx, ny):
        distx = abs(nx - x)
        disty = abs(ny - y)
        print(distx, disty)
        if distx == 2 and disty == 2:
            return True

        return False


class Horse(Piece):
    def move(self, x, y, nx, ny):
        distx = abs(nx - x)
        disty = abs(ny - y)
        destPiece = gameboard[nx][ny]
        print(destPiece,destPiece.colour)
        print("horse")
        print(distx, disty)
        if (distx == 2 and disty == 1) or (distx == 1 and disty == 2):
            print(destPiece)
            if destPiece.colour != self.colour:
                return True

        return False


class Chariot(Piece):
    def move(self, x, y, nx, ny):
        return True


class Cannon(Piece):
    def move(self, x, y, nx, ny):
        return True

class Soldier(Piece):
    def __init__(self, colour, name, direction):
        self.name = name
        self.colour = colour
        # of course, the smallest piece is the hardest to code. direction should be either 1 or -1, should be -1 if the pawn is traveling "backwards"
        self.direction = direction

    def move(self, x, y, nx, ny):
        distx = nx - x
        disty = ny - y
        destPiece = gameboard[nx][ny]
        if self.colour == RED:
            if y < 5:
                if distx == 0 and disty == 1:
                    return True
            else:
                if (distx == 1 or distx == -1) and disty == 0:
                    return True
                elif distx == 0 and (disty == 1 or disty == -1):
                    return True
        else:
            if y > 4:
                if distx == 0 and disty == -1:
                    return True
            else:
                if (distx == 1 or distx == -1) and disty == 0:
                    return True
                elif distx == 0 and (disty == 1 or disty == -1):
                    return True
        return False


class Game:
    def __init__(self):
        self.playersturn = BLACK
        # self.gameboard = {}
        self.placepiece()

    def getBoard(self):
        return self.gameboard

    def placepiece(self):
        w, h = 10, 10;
        self.gameboard = [[Empty((0,255,0), "Empty") for x in range(w)] for y in range(h)]
        for i in range(0, 9):
            if i % 2 == 0:
                self.gameboard[i][3] = Soldier(RED, uniDict[RED][Soldier], 1)
                self.gameboard[i][6] = Soldier(BLACK, uniDict[BLACK][Soldier], -1)

        self.gameboard[1][2] = Cannon(RED, uniDict[RED][Cannon])
        self.gameboard[7][2] = Cannon(RED, uniDict[RED][Cannon])
        self.gameboard[1][7] = Cannon(BLACK, uniDict[RED][Cannon])
        self.gameboard[7][7] = Cannon(BLACK, uniDict[RED][Cannon])

        pieces = [Chariot, Horse, Elephant, Advisor, General, Advisor, Elephant, Horse, Chariot]

        for i in range(0, 9):
            self.gameboard[i][0] = pieces[i](RED, uniDict[RED][pieces[i]])
            self.gameboard[i][9] = pieces[i](BLACK, uniDict[BLACK][pieces[i]])

    def drawboard(self):
        for i in range(0, 9):
            for j in range(0, 10):
                if self.gameboard[i][j].name != "Empty":
                    k = 45 + 80 * i
                    l = 30 + 80 * j
                    item = self.gameboard[i][j]
                    name = item.name
                    colour = item.colour
                    text = font.render(name, True, colour)
                    textRect = text.get_rect()
                    textRect.center = (k, l)
                    pygame.draw.circle(screen, (245, 188, 66), (k, l), 30)
                    screen.blit(text, textRect)

    def mouseselect(self):
        # print("selected")
        # print(i, j)
        if self.gameboard[i][j].name != "Empty":
            pygame.draw.circle(screen, (3, 140, 252), ((x), (y)), 34, width=5)
            # screen.blit(selectscreen, ((45 + 80 * x) - 40, (30 + 80 * y) - 40))
        # self.gameboard[i][j], self.gameboard[0][0] = self.gameboard[0][0], self.gameboard[i][j] //swap code

    def swappiece(self, piece, i, j, a, b):
        print(i, j, a, b)

        try:
            if piece.move(i, j, a, b):
                self.gameboard[i][j], self.gameboard[a][b] = Empty((0,255,0),"Empty"), self.gameboard[i][j]
        except AttributeError:
            pass

    def canmove(self, temppiece, i, j, a, b):
        return temppiece.move(i, j, a, b)

    def dragselect(self, screen, board, selectedPiece):

        if selectedPiece:
            item, ox, oy = selectedPiece
            npiece, nx, ny = get_square_under_mouse(gameboard)
            print(nx,ny)
            if nx != None:
                if item.move(ox // 80, oy // 80, nx, ny):
                    pygame.draw.circle(screen, (0, 128, 0), (45 + nx * 80, 30 + ny * 80), 34, width=5)
                else:
                    pygame.draw.circle(screen, (128, 0, 0), (45 + nx * 80, 30 + ny * 80), 34, width=5)

            if item != 0:
                color = item.colour
                name = item.name
                s1 = font.render(name, True, pygame.Color(color))
                s2 = font.render(name, True, pygame.Color('darkgrey'))
                pos = pygame.Vector2(pygame.mouse.get_pos())
                screen.blit(s2, s2.get_rect(center=pos + (1, 1)))
                screen.blit(s1, s1.get_rect(center=pos))
            # selected_rect = pygame.Rect(x, y, 80, 80)
            # pygame.draw.line(screen, pygame.Color('red'), selected_rect.center, pos)
            return nx, ny


uniDict = {RED: {General: "帅", Advisor: "仕", Elephant: "相", Horse: "傌", Chariot: "俥", Cannon: "炮", Soldier: "兵"},
           BLACK: {General: "将", Advisor: "士", Elephant: "象", Horse: "馬", Chariot: "車", Cannon: "砲", Soldier: "卒"}}

pygame.init()
pygame.font.init()

font = pygame.font.Font("Cyberbit.ttf", 32)
font.bold = True
screen = pygame.display.set_mode((729, 780))
clock = pygame.time.Clock()

bg_surface = pygame.image.load('bg.png').convert()
selectscreen = pygame.Surface([80, 80], pygame.SRCALPHA)
gamescreen = pygame.Surface([729, 780], pygame.SRCALPHA)
gap = 80

game = Game()
gameboard = Game.getBoard(game)
selectedPiece = None
dropPos = None
while True:
    pygame.event.pump()
    piece, i, j = get_square_under_mouse(gameboard)
    location = pygame.mouse.get_pos()
    # i = int(location[0] / 80)
    # j = int(location[1] / 80)
    x = 45 + 80 * i
    y = 30 + 80 * j
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                selectedPiece = piece, x, y
                npiece, nx, ny = get_square_under_mouse(gameboard)
        if event.type == pygame.MOUSEBUTTONUP:
            if dropPos:
                piece, oldx, oldy = selectedPiece
                newx, newy = dropPos
                # piece, old_x, old_y = selectedPiec
                # gameboard[old_x//80][old_y//80] = 0
                # new_x, new_y = dropPos
                # gameboard[new_x//80][new_y//80] = piece
                game.swappiece(piece, oldx // 80, oldy // 80, newx, newy)
            selectedPiece = None
            dropPos = None
    # selectscreen.fill((255, 255, 255))
    screen.blit(bg_surface, (0, 0))
    game.mouseselect()
    game.drawboard()
    screen.blit(gamescreen, (0, 0))
    dropPos = game.dragselect(screen, gameboard, selectedPiece)
    pygame.display.flip()

    # pygame.display.update()
    clock.tick(60)
