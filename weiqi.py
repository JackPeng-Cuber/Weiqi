from copy import copy
from math import *

# 定义棋子状态全局常量
VOID = 0
BLACK = 1
WHITE = 2


def inrange(number, start, stop):
    try:
        return number >= start and number < stop
    except ValueError:
        return (number >= start).all() and (number < stop).all()


class Weiqi:
    def __init__(self, ways) -> None:
        if ways <= 0 or ways % 2 != 1:
            raise ValueError("围棋路数必须为正奇数")
        self.ways = ways
        self.board = [[VOID]*ways for way in range(ways)]
        self.history = [self.copy()]
        self.black = 0
        self.white = 0
        self.black_ = 0
        self.white_ = 0
        self.round = BLACK
        self.minBlacksGases = 0
        self.minWhitesGases = 0
        self.weight = 0
        self.situationProcess = 0

    # 获取目标
    def getPoint(self, position):
        x, y = position
        return self.board[x][y]

    # 设置目标
    def setPoint(self, position, color):
        x, y = position
        self.board[x][y] = color

    # 计算整块与空地
    def getPiecesAndGases(self, position):
        color = self.getPoint(position)
        if color == VOID:
            return None
        pieces = []
        gases = []
        searched = []

        def search(position):
            x, y = position
            if position in searched or not inrange(x, 0, self.ways) or not inrange(y, 0, self.ways):
                return
            searched.append(position)
            if self.getPoint(position) == VOID:
                if position not in gases:
                    gases.append(position)
            elif self.getPoint(position) == color:
                pieces.append(position)
                for direction in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                    search(direction)
        search(position)
        return pieces, gases

    # 提起所有死子
    def takeAllDeads(self, color):
        npieces = 0
        for x in range(self.ways):
            for y in range(self.ways):
                if self.getPoint((x, y)) == color:
                    piecesAndGases = self.getPiecesAndGases((x, y))
                    if len(piecesAndGases[1]) == 0:
                        for piece in piecesAndGases[0]:
                            self.setPoint(piece, VOID)
                        npieces += len(piecesAndGases[0])
        return npieces

    # 计算形势
    def getSituation(self, weight=False, board=None):
        searched = []
        if board == None:board = self.copy()
        else:board = [copy(points) for points in board]
        backup = self.new()
        situation = self.new()
        black = 0
        white = 0
        self.situationProcess = 0

        def search1(position):
            x, y = position
            if position in searched or not inrange(x, 0, self.ways) or not inrange(y, 0, self.ways):
                return
            searched.append(position)

            if self.getPoint(position) in (VOID, color):
                for direction in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                    search1(direction)
            else:
                enemies.append(position)

        def search2(position):
            x, y = position
            if position in searched or not inrange(x, 0, self.ways) or not inrange(y, 0, self.ways):
                return
            searched.append(position)

            if board[x][y] == BLACK:
                self.black_ += 1
                return []
            elif board[x][y] == WHITE:
                self.white_ += 1
                return []
            else:
                voids.append(position)
                for direction in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                    search2(direction)

        def search3(position, level=0):
            x, y = position
            if position in searched or not inrange(x, 0, self.ways) or not inrange(y, 0, self.ways):
                return
            searched.append(position)
            searching = []
            

            if board[x][y] == BLACK:
                self.weight += 1/level
            elif board[x][y] == WHITE:
                self.weight -= 1/level
            else:
                for direction in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                    if direction not in searched or inrange(x, 0, self.ways) or inrange(y, 0, self.ways):
                        searching.append(direction)
                return searching

        def split(pieces_):
            splitGases = []
            searched = []

            for piece in pieces_:
                if piece in searched:
                    continue
                try:
                    pieces, gases = self.getPiecesAndGases(piece)
                except TypeError:continue
                searched.extend(pieces)
                if getTrueEyes(piece) < 2:
                    splitGases.append(len(gases))

            return splitGases

        def getTrueEyes(position):
            gases = self.getPiecesAndGases(position)[1]
            color = self.getPoint(position)
            eyes = self.new()
            ntrueEyes = 0
            trueEyes.clear()
            voids = []
            searched = []

            def search(position):
                x, y = position
                if position in searched or not inrange(x, 0, self.ways) or not inrange(y, 0, self.ways):
                    return
                searched.append(position)

                try:
                    ngases = len(self.getPiecesAndGases(position)[1])
                except TypeError:pass
                if self.getPoint(position) == BLACK:
                    self.black_ += 1
                    if self.minBlacksGases == inf or self.minBlacksGases > ngases:
                        self.minBlacksGases = ngases
                elif self.getPoint(position) == WHITE:
                    self.white_ += 1
                    if self.minWhitesGases == inf or self.minWhitesGases > ngases:
                        self.minWhitesGases = ngases
                else:
                    voids.append(position)
                    for direction in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                        search(direction)
            for gas in gases:
                if eyes[gas[0]][gas[1]] != None:
                    self.black_, self.white_ = eyes[gas[0]][gas[1]]
                else:
                    self.black_ = 0
                    self.white_ = 0
                    self.minBlacksGases = inf
                    self.minWhitesGases = inf
                    searched.clear()
                    voids.clear()
                    search(gas)
                    for void in voids:
                        eyes[void[0]][void[1]] = (self.black_, self.white_)
                if ((color == BLACK and self.black_ > 0 and self.white_ == 0 and self.minBlacksGases >= 2) or (color == WHITE and self.white_ > 0 and self.black_ == 0 and self.minWhitesGases >= 2)) and (gas not in trueEyes):
                    ntrueEyes += 1
                    trueEyes.extend(voids)
            return ntrueEyes

        trueEyes = []
        for x in range(self.ways):
            for y in range(self.ways):
                color = self.getPoint((x, y))
                if color != VOID and backup[x][y] == None and board[x][y] != VOID:
                    pieces, gases = self.getPiecesAndGases((x, y))
                    ntrueEyes = getTrueEyes((x, y))
                    if ntrueEyes < 2:
                        enemies = []
                        searched.clear()
                        search1((x, y))
                        enemiesGases = split(enemies)
                        if len(enemiesGases) > 0:
                            minEnemiesGases = min(enemiesGases)
                        else:
                            minEnemiesGases = 0
                        if minEnemiesGases > len(gases):
                            for piece in pieces:
                                board[piece[0]][piece[1]] = VOID
                                backup[piece[0]][piece[1]] = VOID
                self.situationProcess += 1

        for x in range(self.ways):
            for y in range(self.ways):
                if situation[x][y] == None:
                    color = board[x][y]
                    if color == VOID:
                        self.black_ = 0
                        self.white_ = 0
                        searched.clear()
                        voids = []
                        search2((x, y))
                        for void in voids:
                            if self.black_ > 0 and self.white_ == 0:
                                situation[void[0]][void[1]] = BLACK
                                black += 1
                            elif self.white_ > 0 and self.black_ == 0:
                                situation[void[0]][void[1]] = WHITE
                                white += 1
                            else:
                                if weight:
                                    self.weight = 0
                                    level = 1
                                    searched.clear()
                                    searching = search3(void)
                                    while True:
                                        directions = copy(searching)
                                        searching.clear()
                                        for direction in directions:
                                            result = search3(direction, level)
                                            if result != None:
                                                searching.extend(result)
                                        if len(searching) == 0:break
                                        level += 1
                                        
                                    if self.weight > 1:
                                        situation[void[0]][void[1]] = BLACK
                                        black += 1
                                    elif self.weight < -1:
                                        situation[void[0]][void[1]] = WHITE
                                        white += 1
                                    else:
                                        situation[void[0]][void[1]] = VOID
                                else:
                                    situation[void[0]][void[1]] = VOID
                                self.situationProcess += 1
                    elif color == BLACK:
                        black += 1
                    elif color == WHITE:
                        white += 1

        return situation, black, white
    
    # 计算人工智能
    def getCalculation(self, position, color):
        def takeAllDeads(color):
            def getPiecesAndGases(position):
                x, y = position
                color = board[x][y]
                if color == VOID:
                    return None
                pieces = []
                gases = []
                searched = []

                def search(position):
                    x, y = position
                    if position in searched or not inrange(x, 0, self.ways) or not inrange(y, 0, self.ways):
                        return
                    searched.append(position)
                    if board[x][y] == VOID:
                        if position not in gases:
                            gases.append(position)
                    elif board[x][y] == color:
                        pieces.append(position)
                        for direction in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                            search(direction)
                search(position)
                return pieces, gases
            npieces = 0
            for x in range(self.ways):
                for y in range(self.ways):
                    if board[x][y] == color:
                        piecesAndGases = getPiecesAndGases((x, y))
                        if len(piecesAndGases[1]) == 0:
                            for piece in piecesAndGases[0]:
                                board[piece[0]][piece[1]] = VOID
                            npieces += len(piecesAndGases[0])
            return npieces
        x, y = position
        board = self.copy()
        board[x][y] = color
        if color == BLACK:
            takeAllDeads(WHITE)
        elif color == WHITE:
            takeAllDeads(BLACK)
        if takeAllDeads(color) != 0:return
        if board in self.history:
            return
        black, white = self.getSituation(True, board)[1:]
        if color == BLACK:
            return black - white
        elif color == WHITE:
            return white - black

    # 记录
    def record(self):
        if self.board not in self.history:
            self.history.append(self.copy())

    # 新建空棋盘
    def new(self):
        return [[None]*self.ways for way in range(self.ways)]
    
    # 复制棋盘
    def copy(self):
        return [copy(points) for points in self.board]
