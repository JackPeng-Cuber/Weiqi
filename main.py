# 强制结束线程
def stop_thread(thread):
    import ctypes
    import inspect
    def _async_raise(tid, exctype):
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    _async_raise(thread.ident, SystemExit)

# 书写文字
def write(surface, text, position, font, size, color, background=None):
    fontSurface = font(size).render(text, True, color, background)
    surface.blit(fontSurface, fontSurface.get_rect(center=position))

if __name__ == "__main__":
    from numpy import array
    from pygame import *
    import sys
    import time
    from tkinter import Tk
    from threading import Thread
    from copy import copy
    from weiqi import Weiqi, VOID, BLACK, WHITE, inrange
    from animation import showAnimation
    from math import *
    from ui import fonts, Button
    from random import choice, randint

    # 场景常量
    MAIN = 0
    RULES = 1
    HELPS = 2
    SETTINGS = 3
    GAME = 4
    GAMESETTINGS = 5
    
    # 初始化
    init()
    tk = Tk()
    screenWidth, screenHeight = tk.winfo_screenwidth(), tk.winfo_screenheight()
    del tk
    window = display.set_mode((screenWidth*0.8, screenHeight*0.8), flags=RESIZABLE)
    icon = image.load("textures/icon.png")
    display.set_caption("围棋")
    display.set_icon(icon)
    fullscreen = False
    ways = 0
    waysError = False
    fps = 0
    FPSUpdateRate = 1
    lastframe = time.time()
    frames = []
    exit_ = False
    blackMachine = False
    whiteMachine = False
    weight = False
    stoned = False
    scene = MAIN
    gameScene = GAME
    showSituation = False
    showCalculation = False
    windowWidth, windowHeight = window.get_rect().size
    mousePressing = False
    soundsError = False
    musicOn = True
    soundOn = True

    # 颜色常量
    DEEP = "#000000"
    DEEPDEEPGRAY = "#2A2A2A"
    DEEPGRAY = "#555555"
    GRAY ="#7F7F7F"
    LIGHTGRAY = "#AAAAAA"
    LIGHTLIGHTGRAY = "#D4D4D4"
    LIGHT = "#FFFFFF"
    LIGHTRED = "#FF7F7F"
    RED = "#FF0000"
    GREEN = "#00FF00"
    RED_GREEN = [i*0x100 + 0xff0000 for i in range(0x0, 0xff+1)] + [i*0x10000 + 0x00ff00 for i in range(0x0, 0xff+1)[::-1]]

    # 按钮
    startButton = Button(window, (windowWidth/2-windowWidth/6, windowHeight*0.5-windowHeight/10), (windowWidth/3, windowHeight/5), "开始对局", fonts.STXinWei, LIGHT)
    exitButton = Button(window, (windowWidth/2-windowWidth/6, windowHeight*0.75-windowHeight/10), (windowWidth/3, windowHeight/5), "退出游戏", fonts.STXinWei, LIGHTRED)
    musicButton = Button(window, (windowWidth*0.1-windowWidth/20, windowHeight*0.8-windowHeight/20), (windowWidth/10, windowHeight/10), "开启音乐", fonts.STXinWei, LIGHT)
    soundButton = Button(window, (windowWidth*0.1-windowWidth/20, windowHeight*0.9-windowHeight/20), (windowWidth/10, windowHeight/10), "开启音效", fonts.STXinWei, LIGHT)

    blackMachineButton = Button(window, (windowWidth/2-windowWidth/10, windowHeight*0.5-windowHeight/16), (windowWidth/5, windowHeight/8), "关闭黑棋电脑", fonts.STXinWei, LIGHT)
    whiteMachineButton = Button(window, (windowWidth/2-windowWidth/10, windowHeight*0.65-windowHeight/16), (windowWidth/5, windowHeight/8), "关闭白棋电脑", fonts.STXinWei, LIGHT)
    weightSituationButton = Button(window, (windowWidth/2-windowWidth/10, windowHeight*0.8-windowHeight/16), (windowWidth/5, windowHeight/8), "关闭数子权重", fonts.STXinWei, LIGHT)
    continueButton = Button(window, (windowWidth*0.8-windowWidth/18, windowHeight*0.9-windowHeight/24), (windowWidth/9, windowHeight/12), "继续", fonts.STXinWei, LIGHT)

    situationButton = Button(window, (windowHeight+(windowWidth-windowHeight)/2-windowWidth/16, windowHeight*0.5-windowWidth/24), (windowWidth/8, windowHeight/12), "形势判断", fonts.STXinWei, LIGHT)
    calculationButton = Button(window, (windowHeight+(windowWidth-windowHeight)/2-windowWidth/16, windowHeight*0.6-windowWidth/24), (windowWidth/8, windowHeight/12), "人工智能", fonts.STXinWei, LIGHT)
    pauseButton = Button(window, (windowHeight+(windowWidth-windowHeight)/2-windowWidth/16, windowHeight*0.7-windowWidth/24), (windowWidth/8, windowHeight/12), "停一手", fonts.STXinWei, LIGHT)
    settingButton = Button(window, (windowHeight+(windowWidth-windowHeight)/2-windowWidth/16, windowHeight*0.8-windowWidth/24), (windowWidth/8, windowHeight/12), "设置", fonts.STXinWei, LIGHT)
    exitGameButton = Button(window, (windowHeight+(windowWidth-windowHeight)/2-windowWidth/16, windowHeight*0.9-windowWidth/24), (windowWidth/8, windowHeight/12), "退出游戏", fonts.STXinWei, LIGHTRED)

    blackMachineGameButton = Button(window, (windowHeight+(windowWidth-windowHeight)/2-windowWidth/16, windowHeight*0.5-windowWidth/24), (windowWidth/8, windowHeight/12), "关闭黑棋电脑", fonts.STXinWei, LIGHT)
    whiteMachineGameButton = Button(window, (windowHeight+(windowWidth-windowHeight)/2-windowWidth/16, windowHeight*0.58-windowWidth/24), (windowWidth/8, windowHeight/12), "关闭白棋电脑", fonts.STXinWei, LIGHT)
    weightSituationGameButton = Button(window, (windowHeight+(windowWidth-windowHeight)/2-windowWidth/16, windowHeight*0.66-windowWidth/24), (windowWidth/8, windowHeight/12), "关闭数子权重", fonts.STXinWei, LIGHT)
    musicGameButton = Button(window, (windowHeight+(windowWidth-windowHeight)/2-windowWidth/16, windowHeight*0.74-windowWidth/24), (windowWidth/8, windowHeight/12), "开启音乐", fonts.STXinWei, LIGHT)
    soundGameButton = Button(window, (windowHeight+(windowWidth-windowHeight)/2-windowWidth/16, windowHeight*0.82-windowWidth/24), (windowWidth/8, windowHeight/12), "开启音效", fonts.STXinWei, LIGHT)
    returnButton = Button(window, (windowHeight+(windowWidth-windowHeight)/2-windowWidth/16, windowHeight*0.9-windowWidth/24), (windowWidth/8, windowHeight/12), "返回", fonts.STXinWei, LIGHT)

    # 音效
    try:
        class sounds:
            newStone = mixer.Sound("sounds/newStone.mp3")
            eatOne = mixer.Sound("sounds/eatOne.mp3")
            eatMore = mixer.Sound("sounds/eatMore.mp3")
    except error:soundsError = True

    # 开头动画
    if not soundsError:mixer.music.load("sounds/bgm.mp3")
    if not soundsError:mixer.music.play(loops=-1)
    try:fullscreen = showAnimation(window)
    except KeyboardInterrupt as e:pass

    # 形势判断与人工智能
    def getSituation():
        global situation, situationProcess, stoned
        while True:
            if stoned:
                stoned = False
                situationProcess = 0
                try:situation, weiqi.black, weiqi.white = weiqi.getSituation(weight=weight)
                except (UnboundLocalError, TypeError):pass
                weiqi.situationProcess = ways**2*2
    
    def getCalculation():
        global max_, min_, best, calculationProcess
        best.clear()
        best_ = []
        max_ = -inf
        min_ = inf
        weiqi_ = copy(weiqi)
        calculationProcess = 0
        for x in range(ways) if weiqi.round == WHITE else range(ways):
            for y in range(ways):
                if weiqi_.getPoint((x, y)) == VOID:
                    result = weiqi_.getCalculation((x, y), weiqi.round)
                    if result == None:continue
                    calculation[x][y] = result
                    if result > max_:
                        max_ = result
                    if result < min_:
                        min_ = result
                calculationProcess += 1
        calculationProcess = ways**2
        
        for x in range(ways):
            for y in range(ways):
                if calculation[x][y] == max_:
                    best_.append((x, y))
        best = copy(best_)

    # 进入死循环
    while True:
        if sum(frames) >= FPSUpdateRate:
            fps = len(frames) / sum(frames)
            frames.clear()
        frames.append(time.time() - lastframe)
        lastframe = time.time()
        x, y = mouse.get_pos()
        if not fullscreen:
            windowWidth, windowHeight = window.get_rect().size
        else:
            windowWidth, windowHeight = screenWidth, screenHeight

        # 更新按钮的位置与大小
        startButton.position = (windowWidth/2-windowWidth/6, windowHeight*0.5-windowHeight/10)
        exitButton.position = (windowWidth/2-windowWidth /6, windowHeight*0.75-windowHeight/10)
        musicButton.position = (windowWidth*0.1-windowWidth/20, windowHeight*0.8-windowHeight/20)
        soundButton.position = (windowWidth*0.1-windowWidth/20, windowHeight*0.9-windowHeight/20)
        blackMachineButton.position = (windowWidth/2-windowWidth/10, windowHeight*0.5-windowHeight/16)
        whiteMachineButton.position = (windowWidth/2-windowWidth/10, windowHeight*0.65-windowHeight/16)
        weightSituationButton.position = (windowWidth/2-windowWidth/10, windowHeight*0.8-windowHeight/16)
        continueButton.position = (windowWidth*0.8-windowWidth/18, windowHeight*0.9-windowHeight/24)
        situationButton.position = (windowHeight+(windowWidth-windowHeight)/2-windowWidth/16, windowHeight*0.5-windowWidth/24)
        calculationButton.position = (windowHeight+(windowWidth-windowHeight)/2-windowWidth/16, windowHeight*0.6-windowWidth/24)
        pauseButton.position = (windowHeight+(windowWidth-windowHeight)/2-windowWidth/16, windowHeight*0.7-windowWidth/24)
        settingButton.position = (windowHeight+(windowWidth-windowHeight)/2-windowWidth/16, windowHeight*0.8-windowWidth/24)
        exitGameButton.position = (windowHeight+(windowWidth-windowHeight)/2-windowWidth/16, windowHeight*0.9-windowWidth/24)
        blackMachineGameButton.position = (windowHeight+(windowWidth-windowHeight)/2-windowWidth/16, windowHeight*0.5-windowWidth/24)
        whiteMachineGameButton.position = (windowHeight+(windowWidth-windowHeight)/2-windowWidth/16, windowHeight*0.58-windowWidth/24)
        weightSituationGameButton.position = (windowHeight+(windowWidth-windowHeight)/2-windowWidth/16, windowHeight*0.66-windowWidth/24)
        musicGameButton.position = (windowHeight+(windowWidth-windowHeight)/2-windowWidth/16, windowHeight*0.74-windowWidth/24)
        soundGameButton.position = (windowHeight+(windowWidth-windowHeight)/2-windowWidth/16, windowHeight*0.82-windowWidth/24)
        returnButton.position = (windowHeight+(windowWidth-windowHeight)/2-windowWidth/16, windowHeight*0.9-windowWidth/24)

        startButton.size = (windowWidth/3, windowHeight/5)
        exitButton.size = (windowWidth/3, windowHeight/5)
        musicButton.size = (windowWidth/10, windowHeight/10)
        soundButton.size = (windowWidth/10, windowHeight/10)
        blackMachineButton.size = (windowWidth/5, windowHeight/8)
        whiteMachineButton.size = (windowWidth/5, windowHeight/8)
        weightSituationButton.size = (windowWidth/5, windowHeight/8)
        continueButton.size = (windowWidth/9, windowHeight/12)
        situationButton.size = (windowWidth/8, windowHeight/12)
        calculationButton.size = (windowWidth/8, windowHeight/12)
        pauseButton.size = (windowWidth/8, windowHeight/12)
        settingButton.size = (windowWidth/8, windowHeight/12)
        exitGameButton.size = (windowWidth/8, windowHeight/12)
        blackMachineGameButton.size = (windowWidth/8, windowHeight/12)
        whiteMachineGameButton.size = (windowWidth/8, windowHeight/12)
        weightSituationGameButton.size = (windowWidth/8, windowHeight/12)
        musicGameButton.size = (windowWidth/8, windowHeight/12)
        soundGameButton.size = (windowWidth/8, windowHeight/12)
        returnButton.size = (windowWidth/8, windowHeight/12)
        
        if not soundsError:
            if musicOn:
                mixer.music.set_volume(1)
            else:
                mixer.music.set_volume(0)

        # MIAN 场景
        if scene == MAIN:
            for e in event.get():
                if e.type == QUIT:
                    try:
                        stop_thread(getSituationThread)
                        stop_thread(getCalculationThread)
                    except (NameError, ValueError):pass
                    sys.exit()
                elif e.type == KEYDOWN:
                    # F11 键切换全屏
                    if e.key == K_F11:
                        fullscreen = not fullscreen
                        if fullscreen:
                            display.set_mode(flags=FULLSCREEN)
                        else:
                            display.set_mode((screenWidth*0.8, screenHeight*0.8), flags=RESIZABLE)
                elif e.type == MOUSEBUTTONDOWN:
                    mousePressing = True
                elif e.type == MOUSEBUTTONUP:
                    mousePressing = False
            
            window.fill(DEEPGRAY)
            write(window, "围棋", (windowWidth/2, windowHeight/5), fonts.STXingKa, windowWidth/10, LIGHT)
            if soundsError:write(window, "*无法输出音效！！！", (windowWidth/2, windowHeight*0.9), fonts.STXinWei, windowHeight/3/9.5, RED)

            # 绘制按钮
            startButton.update(mousePressing)
            exitButton.update(mousePressing)
            musicButton.update(mousePressing)
            soundButton.update(mousePressing)

            startButton.draw()
            exitButton.draw()
            musicButton.draw()
            soundButton.draw()
            if startButton.isJustPress:
                if not soundsError and soundOn:sounds.newStone.play()
                mousePressing = False
                scene = RULES
            if exitButton.isJustPress:
                if not soundsError and soundOn:sounds.newStone.play()
                try:
                    stop_thread(getSituationThread)
                    stop_thread(getCalculationThread)
                except (NameError, ValueError):pass
                sys.exit()
            if musicButton.isJustPress:
                if not soundsError and soundOn:sounds.newStone.play()
                if musicOn:
                    musicOn = False
                    musicButton.text = "关闭音乐"
                    musicGameButton.text = "关闭音乐"
                else:
                    musicOn = True
                    musicButton.text = "开启音乐"
                    musicGameButton.text = "开启音乐"
            if soundButton.isJustPress:
                if not soundsError and soundOn:sounds.newStone.play()
                if soundOn:
                    soundOn = False
                    soundButton.text = "关闭音效"
                    soundGameButton.text = "关闭音效"
                else:
                    soundOn = True
                    soundButton.text = "开启音效"
                    soundGameButton.text = "开启音效"
        
        # RULES 场景
        elif scene == RULES:
            for e in event.get():
                if e.type == QUIT:
                    try:
                        stop_thread(getSituationThread)
                        stop_thread(getCalculationThread)
                    except (NameError, ValueError):pass
                    sys.exit()
                elif e.type == KEYDOWN:
                    # F11 键切换全屏
                    if e.key == K_F11:
                        fullscreen = not fullscreen
                        if fullscreen:
                            display.set_mode(flags=FULLSCREEN)
                        else:
                            display.set_mode((screenWidth*0.8, screenHeight*0.8), flags=RESIZABLE)
                elif e.type == MOUSEBUTTONDOWN:
                    mousePressing = True
                elif e.type == MOUSEBUTTONUP:
                    mousePressing = False
            
            window.fill(DEEPGRAY)
            write(window, "围棋规则", (windowWidth/2, windowHeight*0.15), fonts.STXingKa, windowWidth/12, LIGHT)
            write(window, "·围棋棋盘一般有 19×19 个交叉点，即19路棋盘，若追求快速，也可选择更小路棋盘，如 9路、13路等", (windowWidth/2, windowHeight*0.3), fonts.STXinWei, windowWidth*0.02, LIGHT)
            write(window, "·黑先，双方交替落子，落子后不得移动棋子", (windowWidth*0.245, windowHeight*0.38), fonts.STXinWei, windowWidth*0.02, LIGHT)
            write(window, "·围棋连起的棋子可看作一个整体（横纵连，不包括斜连）", (windowWidth*0.305, windowHeight*0.46), fonts.STXinWei, windowWidth*0.02, LIGHT)
            write(window, "·整体周围一圈空地叫做棋子的气", (windowWidth*0.195, windowHeight*0.54), fonts.STXinWei, windowWidth*0.02, LIGHT)
            write(window, "·棋子的气即是棋子的生命值，当棋子无气，视为死亡，提起该子", (windowWidth*0.336, windowHeight*0.62), fonts.STXinWei, windowWidth*0.02, LIGHT)
            write(window, "·围棋不得出现与过去棋局相同的局面，即打劫", (windowWidth*0.256, windowHeight*0.7), fonts.STXinWei, windowWidth*0.02, LIGHT)
            write(window, "·围棋围起的空地（包括棋子本身）即为目，终局以比较目的数量判断胜负", (windowWidth*0.377, windowHeight*0.78), fonts.STXinWei, windowWidth*0.02, LIGHT)

            continueButton.update(mousePressing)

            continueButton.draw()

            if continueButton.isJustPress:
                if not soundsError and soundOn:sounds.newStone.play()
                continueButton.text = "开始"
                mousePressing = False
                scene = SETTINGS

        # SETTINGS 场景
        elif scene == SETTINGS:
            for e in event.get():
                if e.type == QUIT:
                    try:
                        stop_thread(getSituationThread)
                        stop_thread(getCalculationThread)
                    except (NameError, ValueError):pass
                    sys.exit()
                elif e.type == KEYDOWN:
                    # F11 键切换全屏
                    if e.key == K_F11:
                        fullscreen = not fullscreen
                        if fullscreen:
                            window = display.set_mode(flags=FULLSCREEN)
                        else:
                            window = display.set_mode((screenWidth*0.8, screenHeight*0.8), flags=RESIZABLE)
                    if e.key in (K_RETURN, K_KP_ENTER):
                        if not (ways <= 0 or ways % 2 != 1):
                            if not soundsError and soundOn:sounds.eatMore.play()
                            # 实例化 围棋 类
                            weiqi = Weiqi(ways)
                            situation = [[None]*ways for way in range(ways)]
                            calculation = [[None]*ways for way in range(ways)]
                            calculationProcess = 0
                            max_ = -inf
                            min_ = inf
                            best = []

                            getSituationThread = Thread(target=getSituation)
                            getSituationThread.start()
                            first = True
                            lastround = None

                            mousePressing = False
                            scene = GAME
                        else:
                            if not soundsError and soundOn:sounds.newStone.play()
                            waysError = True
                    if e.key == K_BACKSPACE:
                        if not soundsError and soundOn:sounds.newStone.play()
                        ways //= 10
                elif e.type == MOUSEBUTTONDOWN:
                    mousePressing = True
                elif e.type == MOUSEBUTTONUP:
                    mousePressing = False
                elif e.type == TEXTINPUT:
                    if all(char in "0123456789" for char in e.text):
                        if not soundsError and soundOn:sounds.newStone.play()
                        if ways*len(e.text)*10+int(e.text) <= 99:
                            ways = ways*len(e.text)*10+int(e.text)
            
            window.fill(DEEPGRAY)
            write(window, f"{ways} 路对局", (windowWidth/2, windowHeight*0.2), fonts.STXinWei, windowWidth/3/4, LIGHT)
            if waysError and ways % 2 == 0:
                write(window, "*围棋路数必须为正奇数！！！", (windowWidth/2, windowHeight*0.3), fonts.STXinWei, windowWidth/3/13.5, RED)
            elif ways % 2 == 0 or (waysError and not weightSituationButton.onButton and not blackMachineButton.onButton and not whiteMachineButton.onButton):
                write(window, "*围棋路数必须为正奇数！！！", (windowWidth/2, windowHeight*0.3), fonts.STXinWei, windowWidth/3/13.5, LIGHTRED)
            if ways == 0:
                write(window, "*请从键盘键入数字以设置路数", (windowWidth/2, windowHeight*0.4), fonts.STXinWei, windowWidth/3/13.5, LIGHTRED)

            # 绘制按钮
            blackMachineButton.update(mousePressing)
            whiteMachineButton.update(mousePressing)
            weightSituationButton.update(mousePressing)
            continueButton.update(mousePressing)
            musicButton.update(mousePressing)
            soundButton.update(mousePressing)

            blackMachineButton.draw()
            whiteMachineButton.draw()
            weightSituationButton.draw()
            continueButton.draw()
            musicButton.draw()
            soundButton.draw()

            if blackMachineButton.isJustPress:
                if not soundsError and soundOn:sounds.newStone.play()
                blackMachine = not blackMachine
                if blackMachine:
                    blackMachineButton.text = "开启黑棋电脑"
                    blackMachineGameButton.text = "开启黑棋电脑"
                else:
                    blackMachineButton.text = "关闭黑棋电脑"
                    blackMachineGameButton.text = "关闭黑棋电脑"
            if whiteMachineButton.isJustPress:
                if not soundsError and soundOn:sounds.newStone.play()
                whiteMachine = not whiteMachine
                if whiteMachine:
                    whiteMachineButton.text = "开启白棋电脑"
                    whiteMachineGameButton.text = "开启白棋电脑"
                else:
                    whiteMachineButton.text = "关闭白棋电脑"
                    whiteMachineGameButton.text = "关闭白棋电脑"
            if weightSituationButton.isJustPress:
                if not soundsError and soundOn:sounds.newStone.play()
                weight = not weight
                if weight:
                    weightSituationButton.text = "开启数子权重"
                    weightSituationGameButton.text = "开启数子权重"
                else:
                    weightSituationButton.text = "关闭数子权重"
                    weightSituationGameButton.text = "关闭数子权重"
            if ways % 2 == 1:
                if blackMachineButton.onButton or whiteMachineButton.onButton:
                    write(window, "电脑将根据“人工智能”计算结果自动落子", (windowWidth/2, windowHeight*0.3), fonts.STXinWei, windowWidth/3/13.5, LIGHTRED)
                    write(window, "路数在 11 路以上时速度极慢！慎重开启！", (windowWidth/2, windowHeight*0.4), fonts.STXinWei, windowWidth/3/13.5, RED)
                if weightSituationButton.onButton:
                    write(window, "开启数子权重可以获取更好的数子（形势判断）效果", (windowWidth/2, windowHeight*0.3), fonts.STXinWei, windowWidth/3/13.5, LIGHTRED)
                    write(window, "计算速度较慢，慎重开启！", (windowWidth/2, windowHeight*0.4), fonts.STXinWei, windowWidth/3/13.5, LIGHTRED)
            if continueButton.isJustPress and not (ways <= 0 or ways % 2 != 1):
                if not soundsError and soundOn:sounds.eatMore.play()
                # 实例化 围棋 类
                weiqi = Weiqi(ways)
                situation = [[None]*ways for way in range(ways)]
                calculation = [[None]*ways for way in range(ways)]
                calculationProcess = 0
                max_ = -inf
                min_ = inf
                best = []
                
                getSituationThread = Thread(target=getSituation)
                getSituationThread.start()
                first = True
                lastround = None

                mousePressing = False
                scene = GAME
            elif continueButton.isJustPress:
                if not soundsError and soundOn:sounds.newStone.play()
                waysError = True
            if musicButton.isJustPress:
                if not soundsError and soundOn:sounds.newStone.play()
                if musicOn:
                    musicOn = False
                    musicButton.text = "关闭音乐"
                    musicGameButton.text = "关闭音乐"
                else:
                    musicOn = True
                    musicButton.text = "开启音乐"
                    musicGameButton.text = "开启音乐"
            if soundButton.isJustPress:
                if not soundsError and soundOn:sounds.newStone.play()
                if soundOn:
                    soundOn = False
                    soundButton.text = "关闭音效"
                    soundGameButton.text = "关闭音效"
                else:
                    soundOn = True
                    soundButton.text = "开启音效"
                    soundGameButton.text = "开启音效"
                
        # GAME 场景
        elif scene == GAME:
            for e in event.get():
                if e.type == QUIT:
                    try:
                        stop_thread(getSituationThread)
                        stop_thread(getCalculationThread)
                    except (NameError, ValueError):pass
                    sys.exit()
                elif e.type == KEYDOWN:
                    # F11 键切换全屏
                    if e.key == K_F11:
                        fullscreen = not fullscreen
                        if fullscreen:
                            window = display.set_mode(flags=FULLSCREEN)
                        else:
                            window = display.set_mode((screenWidth*0.8, screenHeight*0.8), flags=RESIZABLE)
                elif e.type == MOUSEBUTTONDOWN:
                    mousePressing = True
                    if e.button == 1:
                        if inrange(array(mouse.get_pos()), array((0, 0)), array((min(windowWidth, windowHeight),)*2)) and weiqi.getPoint((round(x/min(windowWidth, windowHeight)*ways-0.5), round(y/min(windowWidth, windowHeight)*ways-0.5))) == VOID:
                            
                            # 备份棋盘
                            backup = [copy(point) for point in weiqi.board]

                            # 落子
                            weiqi.setPoint(
                                (round(x/min(windowWidth, windowHeight)*ways-0.5),
                                round(y/min(windowWidth, windowHeight)*ways-0.5)),
                                weiqi.round
                            )

                            # 提子
                            if weiqi.round == BLACK:
                                npieces = weiqi.takeAllDeads(WHITE)
                                if weiqi.takeAllDeads(BLACK) == 0:
                                    weiqi.round = WHITE
                                else:
                                    weiqi.board = backup
                                    continue
                            else:
                                npieces = weiqi.takeAllDeads(BLACK)
                                if weiqi.takeAllDeads(WHITE) == 0:
                                    weiqi.round = BLACK
                                else:
                                    weiqi.board = backup
                                    continue

                            # 判断是否打劫
                            if weiqi.board in weiqi.history:
                                weiqi.board = backup
                                if weiqi.round == BLACK:
                                    weiqi.round = WHITE
                                else:
                                    weiqi.round = BLACK
                                continue
                            

                            # 播放落子音效
                            try:
                                if not soundsError and soundOn:sounds.newStone.play()

                                # 播放提子音效
                                if npieces == 1:
                                    if not soundsError and soundOn:sounds.eatOne.play()
                                elif npieces > 1:
                                    if not soundsError and soundOn:sounds.eatMore.play()
                            except NameError:pass

                            # 记录该回合的落子位置
                            lastround = (round(x/min(windowWidth, windowHeight)*ways-0.5),
                                        round(y/min(windowWidth, windowHeight)*ways-0.5))

                            weiqi.record()

                            try:
                                stop_thread(getCalculationThread)
                            except (NameError, ValueError):
                                pass
                            calculation = [[None]*ways for way in range(ways)]
                            getCalculationThread = Thread(target=getCalculation)
                            getCalculationThread.start()

                            showSituation = False
                            showCalculation = False
                            first = False
                            stoned = True

                elif e.type == MOUSEBUTTONUP:
                    mousePressing = False

            # 清屏
            window.fill(DEEPGRAY)
            if ((weiqi.round == BLACK and blackMachine) or (weiqi.round == WHITE and whiteMachine)) and len(best) != 0:
                choice_ = choice(best)

                # 备份棋盘
                backup = [copy(point) for point in weiqi.board]

                # 落子
                weiqi.setPoint(
                    choice_, weiqi.round
                )

                # 提子
                if weiqi.round == BLACK:
                    npieces = weiqi.takeAllDeads(WHITE)
                    if weiqi.takeAllDeads(BLACK) == 0:
                        weiqi.round = WHITE
                    else:
                        weiqi.board = backup
                        continue
                else:
                    npieces = weiqi.takeAllDeads(BLACK)
                    if weiqi.takeAllDeads(WHITE) == 0:
                        weiqi.round = BLACK
                    else:
                        weiqi.board = backup
                        continue

                # 判断是否打劫
                if weiqi.board in weiqi.history:
                    weiqi.board = backup
                    if weiqi.round == BLACK:
                        weiqi.round = WHITE
                    else:
                        weiqi.round = BLACK
                    continue

                # 播放落子音效
                try:
                    if not soundsError and soundOn:sounds.newStone.play()

                    # 播放提子音效
                    if npieces == 1:
                        if not soundsError and soundOn:sounds.eatOne.play()
                    elif npieces > 1:
                        if not soundsError and soundOn:sounds.eatMore.play()
                except NameError:pass

                # 记录该回合的落子位置
                lastround = choice_

                weiqi.record()

                try:
                    stop_thread(getCalculationThread)
                except (NameError, ValueError):
                    pass
                calculation = [[None]*ways for way in range(ways)]
                getCalculationThread = Thread(target=getCalculation)
                getCalculationThread.start()
                stoned = True

            elif first and blackMachine:
                choice_ = (randint(0, ways-1), randint(0, ways-1))
                weiqi.setPoint(
                    choice_, weiqi.round
                )

                # 播放落子音效
                try:
                    if not soundsError and soundOn:sounds.newStone.play()
                except NameError:pass

                # 记录该回合的落子位置
                lastround = choice_

                weiqi.record()

                if weiqi.round == BLACK:
                    weiqi.round = WHITE
                else:
                    weiqi.round = BLACK

                try:
                    stop_thread(getCalculationThread)
                except (NameError, ValueError):
                    pass
                calculation = [[None]*ways for way in range(ways)]
                getCalculationThread = Thread(target=getCalculation)
                getCalculationThread.start()
                first = False
                stoned = True

            write(window, f"黑占目数：{weiqi.black}目", (windowHeight+(windowWidth-windowHeight)/2, windowHeight*0.1+(windowWidth-windowHeight)/3/7.5), fonts.STXinWei, (windowWidth-windowHeight)/3/7.5, LIGHT)
            write(window, f"白占目数：{weiqi.white}目", (windowHeight+(windowWidth-windowHeight)/2, windowHeight*0.1+(windowWidth-windowHeight)/3/7.5*2.5), fonts.STXinWei, (windowWidth-windowHeight)/3/7.5, LIGHT)
            write(window, f"公共目数：{weiqi.ways**2-weiqi.black-weiqi.white}目", (windowHeight+(windowWidth-windowHeight)/2, windowHeight*0.1+(windowWidth-windowHeight)/3/7.5*4.5), fonts.STXinWei, (windowWidth-windowHeight)/3/7.5, LIGHT)

            if gameScene == GAME:
                # 绘制按钮
                situationButton.update(mousePressing)
                calculationButton.update(mousePressing)
                pauseButton.update(mousePressing)
                settingButton.update(mousePressing)
                exitGameButton.update(mousePressing)

                situationButton.draw()
                calculationButton.draw()
                pauseButton.draw()
                settingButton.draw()
                exitGameButton.draw()

                if situationButton.isJustPress:
                    if not soundsError and soundOn:sounds.newStone.play()
                    showSituation = not showSituation
                    if showSituation:
                        showCalculation = False
                if calculationButton.isJustPress:
                    if not soundsError and soundOn:sounds.newStone.play()
                    showCalculation = not showCalculation
                    if showCalculation:
                        showSituation = False
                if pauseButton.isJustPress:
                    if not soundsError and soundOn:sounds.newStone.play()
                    if weiqi.round == BLACK:
                        weiqi.round = WHITE
                    else:
                        weiqi.round = BLACK

                    try:
                        stop_thread(getCalculationThread)
                    except (NameError, ValueError):
                        pass
                    calculation = [[None]*ways for way in range(ways)]
                    getCalculationThread = Thread(target=getCalculation)
                    getCalculationThread.start()
                    stoned = True
                if settingButton.isJustPress:
                    if not soundsError and soundOn:sounds.newStone.play()
                    mousePressing = False
                    gameScene = GAMESETTINGS
                if exitGameButton.isJustPress:
                    if not soundsError and soundOn:sounds.eatMore.play()
                    try:
                        stop_thread(getSituationThread)
                        stop_thread(getCalculationThread)
                    except (NameError, ValueError):pass
                    sys.exit()
                if situationButton.onButton:
                    write(window, f"形势判断进度：{weiqi.situationProcess*100/(ways**2*2):.1f}%", (windowHeight+(windowWidth-windowHeight)/2, windowHeight*0.1+(windowWidth-windowHeight)/3/7.5*7), fonts.STXinWei, (windowWidth-windowHeight)/3/7.5, LIGHT)
                if calculationButton.onButton:
                    write(window, f"人工智能进度：{calculationProcess*100/(ways**2):.1f}%", (windowHeight+(windowWidth-windowHeight)/2, windowHeight*0.1+(windowWidth-windowHeight)/3/7.5*7), fonts.STXinWei, (windowWidth-windowHeight)/3/7.5, LIGHT)
                if not situationButton.onButton and not calculationButton.onButton:
                    if weiqi.round == BLACK:
                        write(window, "现在是黑方回合", (windowHeight+(windowWidth-windowHeight)/2, windowHeight*0.1+(windowWidth-windowHeight)/3/7.5*7), fonts.STXinWei, (windowWidth-windowHeight)/3/7.5, LIGHT)
                    else:
                        write(window, "现在是白方回合", (windowHeight+(windowWidth-windowHeight)/2, windowHeight*0.1+(windowWidth-windowHeight)/3/7.5*7), fonts.STXinWei, (windowWidth-windowHeight)/3/7.5, LIGHT)


            elif gameScene == GAMESETTINGS:
                # 绘制按钮
                blackMachineGameButton.update(mousePressing)
                whiteMachineGameButton.update(mousePressing)
                weightSituationGameButton.update(mousePressing)
                musicGameButton.update(mousePressing)
                soundGameButton.update(mousePressing)
                returnButton.update(mousePressing)

                blackMachineGameButton.draw()
                whiteMachineGameButton.draw()
                weightSituationGameButton.draw()
                musicGameButton.draw()
                soundGameButton.draw()
                returnButton.draw()

                if blackMachineGameButton.isJustPress:
                    if not soundsError and soundOn:sounds.newStone.play()
                    blackMachine = not blackMachine
                    if blackMachine:
                        blackMachineButton.text = "开启黑棋电脑"
                        blackMachineGameButton.text = "开启黑棋电脑"
                    else:
                        blackMachineButton.text = "关闭黑棋电脑"
                        blackMachineGameButton.text = "关闭黑棋电脑"
                if whiteMachineGameButton.isJustPress:
                    if not soundsError and soundOn:sounds.newStone.play()
                    whiteMachine = not whiteMachine
                    if whiteMachine:
                        whiteMachineButton.text = "开启白棋电脑"
                        whiteMachineGameButton.text = "开启白棋电脑"
                    else:
                        whiteMachineButton.text = "关闭白棋电脑"
                        whiteMachineGameButton.text = "关闭白棋电脑"
                if weightSituationGameButton.isJustPress:
                    if not soundsError and soundOn:sounds.newStone.play()
                    weight = not weight
                    if weight:
                        weightSituationButton.text = "开启数子权重"
                        weightSituationGameButton.text = "开启数子权重"
                    else:
                        weightSituationButton.text = "关闭数子权重"
                        weightSituationGameButton.text = "关闭数子权重"
                if musicGameButton.isJustPress:
                    if not soundsError and soundOn:sounds.newStone.play()
                    if musicOn:
                        musicOn = False
                        musicButton.text = "关闭音乐"
                        musicGameButton.text = "关闭音乐"
                    else:
                        musicOn = True
                        musicButton.text = "开启音乐"
                        musicGameButton.text = "开启音乐"
                if soundGameButton.isJustPress:
                    if not soundsError and soundOn:sounds.newStone.play()
                    if soundOn:
                        soundOn = False
                        soundButton.text = "关闭音效"
                        soundGameButton.text = "关闭音效"
                    else:
                        soundOn = True
                        soundButton.text = "开启音效"
                        soundGameButton.text = "开启音效"
                if returnButton.isJustPress:
                    if not soundsError and soundOn:sounds.newStone.play()
                    mousePressing = False
                    gameScene = GAME

            # 绘制预落棋子
            try:
                if inrange(array(mouse.get_pos()), array((0, 0)), array((min(windowWidth, windowHeight),)*2)) and weiqi.getPoint((round(x/min(windowWidth, windowHeight)*ways-0.5), round(y/min(windowWidth, windowHeight)*ways-0.5))) == VOID:
                    if weiqi.round == BLACK:
                        draw.circle(
                            window, DEEPDEEPGRAY,
                            ((round(x/min(windowWidth, windowHeight)*ways-0.5)+0.5)*min(windowWidth, windowHeight)/ways,
                            (round(y/min(windowWidth, windowHeight)*ways-0.5)+0.5)*min(windowWidth, windowHeight)/ways),
                            0.4*min(windowWidth, windowHeight)/ways
                        )
                    else:
                        draw.circle(
                            window, LIGHTGRAY,
                            ((round(x/min(windowWidth, windowHeight)*ways-0.5)+0.5)*min(windowWidth, windowHeight)/ways,
                                (round(y/min(windowWidth, windowHeight)*ways-0.5)+0.5)*min(windowWidth, windowHeight)/ways),
                            0.4*min(windowWidth, windowHeight)/ways
                        )
            except IndexError:pass

            # 绘制棋盘
            for x in range(ways):
                draw.line(
                    window, LIGHTGRAY,
                    ((x+0.5)*min(windowWidth, windowHeight)/ways, 0.5*min(windowWidth, windowHeight)/ways),
                    ((x+0.5)*min(windowWidth, windowHeight)/ways, (ways-0.5)*min(windowWidth, windowHeight)/ways), 1
                )
            for y in range(ways):
                draw.line(
                    window, LIGHTGRAY,
                    (0.5*min(windowWidth, windowHeight)/ways, (y+0.5)*min(windowWidth, windowHeight)/ways),
                    ((ways-0.5)*min(windowWidth, windowHeight)/ways, (y+0.5)*min(windowWidth, windowHeight)/ways), 1
                )
            
            # 绘制星位
            for x in [1/6, 1/2, 5/6]:
                for y in [1/6, 1/2, 5/6]:
                    draw.circle(
                        window, LIGHTLIGHTGRAY,
                        ((round(x*(ways-1))+0.5)*min(windowWidth, windowHeight)/ways,
                        (round(y*(ways-1))+0.5)*min(windowWidth, windowHeight)/ways),
                        0.1*min(windowWidth, windowHeight)/ways
                    )

            # 绘制棋子
            for x in range(ways):
                for y in range(ways):
                    if weiqi.getPoint((x, y)) == BLACK:
                        draw.circle(
                            window, DEEP,
                            ((x+0.5)*min(windowWidth, windowHeight)/ways,
                            (y+0.5)*min(windowWidth, windowHeight)/ways),
                            0.4*min(windowWidth, windowHeight)/ways
                        )
                    elif weiqi.getPoint((x, y))  == WHITE:
                        draw.circle(
                            window, LIGHT,
                            ((x+0.5)*min(windowWidth, windowHeight)/ways,
                            (y+0.5)*min(windowWidth, windowHeight)/ways),
                            0.4*min(windowWidth, windowHeight)/ways
                        )

            # 绘制结算结果
            if showCalculation:
                for x in range(ways):
                    for y in range(ways):
                        if calculation[x][y] != None:
                            try:
                                color = RED_GREEN[511 *
                                                (calculation[x][y] - min_)//(max_ - min_)]
                            except ZeroDivisionError:
                                color = GREEN
                            draw.circle(
                                window, color,
                                ((x+0.5)*min(windowWidth, windowHeight)/ways,
                                (y+0.5)*min(windowWidth, windowHeight)/ways),
                                0.4*min(windowWidth, windowHeight)/ways
                            )
                for position in best:
                    if weiqi.round == BLACK:
                        color = DEEP
                    elif weiqi.round == WHITE:
                        color = LIGHT
                    draw.circle(
                        window, color,
                        ((position[0]+0.5)*min(windowWidth, windowHeight)/ways,
                        (position[1]+0.5)*min(windowWidth, windowHeight)/ways),
                        0.4*min(windowWidth, windowHeight)/ways, 10
                    )

            # 绘制上一手落子位置提示
            if lastround != None and not showSituation and not showCalculation:
                x, y = lastround
                draw.circle(
                    window, RED,
                    ((x+0.5)*min(windowWidth, windowHeight)/ways,
                    (y+0.5)*min(windowWidth, windowHeight)/ways),
                    0.15*min(windowWidth, windowHeight)/ways
                )

            # 绘制形势
            if showSituation and not stoned:
                for x in range(ways):
                    for y in range(ways):
                        if situation[x][y] == BLACK:
                            draw.rect(window, DEEP, (
                                (x+0.4)*min(windowWidth, windowHeight)/ways,
                                (y+0.4)*min(windowWidth, windowHeight)/ways,
                                0.2*min(windowWidth, windowHeight)/ways,
                                0.2*min(windowWidth, windowHeight)/ways
                            ))
                        elif situation[x][y] == WHITE:
                            draw.rect(window, LIGHT, (
                                (x+0.4)*min(windowWidth, windowHeight)/ways,
                                (y+0.4)*min(windowWidth, windowHeight)/ways,
                                0.2*min(windowWidth, windowHeight)/ways,
                                0.2*min(windowWidth, windowHeight)/ways
                            ))

        # 显示FPS
        write(window, f"FPS  {round(fps)}", (windowWidth*0.95, windowHeight*0.95), fonts.SourceHanSansSC, windowHeight*.04, LIGHT)

        # 更新
        display.update()
