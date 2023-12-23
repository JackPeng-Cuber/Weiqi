from pygame import *
from math import *
from time import time
from ui import fonts
from main import write
import sys

def showAnimation(surface : Surface):
    def calculate1(value):
        return cos((value-1)*pi)/2+0.5

    def calculate2(value):
        return cos((value/2-1)*pi)+1
    
    def actionListener(fullscreen):
        width, height = surface.get_rect().size
        for e in event.get():
            if e.type == QUIT:
                sys.exit()
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                raise KeyboardInterrupt
            elif e.type == KEYDOWN and e.key == K_F11:
                if e.key == K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        display.set_mode(flags=FULLSCREEN)
                    else:
                        display.set_mode((width*0.8, height*0.8), flags=RESIZABLE)
        return width, height, fullscreen

    width, height = surface.get_rect().size
    font = fonts.STXingKa
    fullscreen = False
    DEEPGRAY = "#555555"
    
    start = time()
    while time() - start < 1:
        try:width, height, fullscreen = actionListener(fullscreen)
        except KeyboardInterrupt:
            try:
                mixer.Sound("sounds/newStone.mp3").play()
            except error:pass
            return fullscreen

        surface.fill(DEEPGRAY)

        draw.circle(
            surface=surface,
            color="black",
            center=(width/2, height/2),
            radius=calculate1(time()-start)*height/12
        )

        write(
            surface=surface,
            text="按 ESC 键跳过",
            position=(width*0.1, height*0.05),
            font=fonts.TiejiliSC,
            size=height*0.05,
            color="white"
        )

        display.update()
    
    start = time()
    while time() - start < 1:
        try:width, height, fullscreen = actionListener(fullscreen)
        except KeyboardInterrupt:
            try:
                mixer.Sound("sounds/newStone.mp3").play()
            except error:pass
            return fullscreen
        
        surface.fill(DEEPGRAY)

        draw.rect(
            surface=surface,
            color="black",
            rect=(
                width/2-height/16*calculate1(time()-start)-height/12,
                height/2-height/16*calculate1(time()-start)-height/12,
                height/8*calculate1(time()-start)+height/6,
                height/8*calculate1(time()-start)+height/6
            ),
            border_radius=round((1-calculate1(time()-start)+0.5)*height/12)
        )

        write(
            surface=surface,
            text="按 ESC 键跳过",
            position=(width*0.1, height*0.05),
            font=fonts.TiejiliSC,
            size=height*0.05,
            color="white"
        )

        display.update()

    start = time()
    while time() - start < 1:
        try:width, height, fullscreen = actionListener(fullscreen)
        except KeyboardInterrupt:
            try:
                mixer.Sound("sounds/newStone.mp3").play()
            except error:pass
            return fullscreen

        surface.fill(DEEPGRAY)

        draw.rect(
            surface=surface,
            color="black",
            rect=(
                width/2-height/16-height/12,
                height/2-height/16-height/12,
                height/8+height/6,
                height/8+height/6
            ),
            border_radius=round(0.5*height/12)
        )

        draw.rect(
            surface=surface,
            color = "white",
            rect=(
                width/2-height/16*calculate1(time()-start)*1.8,
                height/2-height/16*calculate1(time()-start)*1.8,
                height/16*calculate1(time()-start)*3.6,
                height/16*calculate1(time()-start)*3.6
            ),
            border_radius=round((1-calculate1(time()-start)+0.1)*height/12)
        )

        write(
            surface=surface,
            text="按 ESC 键跳过",
            position=(width*0.1, height*0.05),
            font=fonts.TiejiliSC,
            size=height*0.05,
            color="white"
        )

        display.update()

    start = time()
    while time() - start < 1:
        try:width, height, fullscreen = actionListener(fullscreen)
        except KeyboardInterrupt:
            try:
                mixer.Sound("sounds/newStone.mp3").play()
            except error:pass
            return fullscreen

        surface.fill(DEEPGRAY)

        draw.rect(
            surface=surface,
            color="black",
            rect=(
                width/2-height/16-height/12,
                height/2-height/16-height/12,
                height/8+height/6,
                height/8+height/6
            ),
            border_radius=round(0.5*height/12)
        )

        draw.rect(
            surface=surface,
            color = "white",
            rect=(
                width/2-height/16*1.8,
                height/2-height/16*1.8,
                height/16*3.6,
                height/16*3.6
            ),
            border_radius=round(0.1*height/12)
        )

        if time() - start > 0 and time() - start < 4/7:
            draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2-height/17, height/2.6),
                end_pos=(width/2-height/17, height/2.6+height*0.6/2.6*calculate1((time()-start)*7/4)),
                width=round(height/120)
            )
        elif time() - start > 4/7:
            draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2-height/17, height/2.6),
                end_pos=(width/2-height/17, height/2.6+height*0.6/2.6),
                width=round(height/120)
            )

        if time() - start > 1/7 and time() - start < 5/7:
            draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2, height/2.6),
                end_pos=(width/2, height/2.6+height*0.6/2.6*calculate1((time()-start-1/7)*7/4)),
                width=round(height/120)
            )
        elif time() - start > 5/7:
            draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2, height/2.6),
                end_pos=(width/2, height/2.6+height*0.6/2.6),
                width=round(height/120)
            )

        if time() - start > 2/7 and time() - start < 6/7:
            draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2+height/17, height/2.6),
                end_pos=(width/2+height/17, height/2.6+height*0.6/2.6*calculate1((time()-start-2/7)*7/4)),
                width=round(height/120)
            )
        elif time() - start > 6/7:
            draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2+height/17, height/2.6),
                end_pos=(width/2+height/17, height/2.6+height*0.6/2.6),
                width=round(height/120)
            )

        if time() - start > 1/7 and time() - start < 5/7:
            draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2-height/8.5, height/2-height/17),
                end_pos=(width/2-height/8.5+height/2.6*calculate1((time()-start-1/7)*7/4)*0.6, height/2-height/17),
                width=round(height/120)
            )
        elif time() - start > 5/7:
            draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2-height/8.5, height/2-height/17),
                end_pos=(width/2-height/8.5+height/2.6*0.6, height/2-height/17),
                width=round(height/120)
            )

        if time() - start > 2/7 and time() - start < 6/7:
            draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2-height/8.5, height/2),
                end_pos=(width/2-height/8.5+height/2.6*calculate1((time()-start-2/7)*7/4)*0.6, height/2),
                width=round(height/120)
            )
        elif time() - start > 6/7:
            draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2-height/8.5, height/2),
                end_pos=(width/2-height/8.5+height/2.6*0.6, height/2),
                width=round(height/120)
            )

        if time() - start > 3/7 and time() - start < 1:
            draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2-height/8.5, height/2+height/17),
                end_pos=(width/2-height/8.5+height/2.6*calculate1((time()-start-3/7)*7/4)*0.6, height/2+height/17),
                width=round(height/120)
            )
        elif time() - start > 1:
            draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2-height/8.5, height/2+height/17),
                end_pos=(width/2-height/8.5+height/2.6*0.6, height/2+height/17),
                width=round(height/120)
            )

        write(
            surface=surface,
            text="按 ESC 键跳过",
            position=(width*0.1, height*0.05),
            font=fonts.TiejiliSC,
            size=height*0.05,
            color="white"
        )

        display.update()

    start = time()
    while time() - start < 1:
        try:width, height, fullscreen = actionListener(fullscreen)
        except KeyboardInterrupt:
            try:
                mixer.Sound("sounds/newStone.mp3").play()
            except error:pass
            return fullscreen
        
        surface.fill(DEEPGRAY)
        
        draw.rect(
            surface=surface,
            color="black",
            rect=(
                width/2-height/16-height/12,
                height/2-height/16-height/12,
                height/8+height/6,
                height/8+height/6
            ),
            border_radius=round(0.5*height/12)
        )

        draw.rect(
            surface=surface,
            color = "white",
            rect=(
                width/2-height/16*1.8,
                height/2-height/16*1.8,
                height/16*3.6,
                height/16*3.6
            ),
            border_radius=round(0.1*height/12)
        )

        draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2-height/17, height/2.6),
                end_pos=(width/2-height/17, height/2.6+height*0.6/2.6),
                width=round(height/120)
            )
        draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2, height/2.6),
                end_pos=(width/2, height/2.6+height*0.6/2.6),
                width=round(height/120)
            )
        draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2+height/17, height/2.6),
                end_pos=(width/2+height/17, height/2.6+height*0.6/2.6),
                width=round(height/120)
            )
        draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2-height/8.5, height/2-height/17),
                end_pos=(width/2-height/8.5+height/2.6*0.6, height/2-height/17),
                width=round(height/120)
            )
        draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2-height/8.5, height/2),
                end_pos=(width/2-height/8.5+height/2.6*0.6, height/2),
                width=round(height/120)
            )
        draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2-height/8.5, height/2+height/17),
                end_pos=(width/2-height/8.5+height/2.6*0.6, height/2+height/17),
                width=round(height/120)
            )

        if time() - start > 0 and time() - start < 1/3:
            draw.circle(
                surface=surface,
                color="black",
                center=(width/2, height/2-height/17),
                radius=height/32*(2-calculate2((time()-start)*3)),
            )
            draw.circle(
                surface=surface,
                color="white",
                center=(width/2, height/2-height/17),
                radius=height/36*(2-calculate2((time()-start)*3)),
                width=round(height/32-height/36)
            )
        elif time() - start > 1/3:
            draw.circle(
                surface=surface,
                color="black",
                center=(width/2, height/2-height/17),
                radius=height/32,
            )
            draw.circle(
                surface=surface,
                color="white",
                center=(width/2, height/2-height/17),
                radius=height/36,
                width=round(height/32-height/36)
            )
        
        if time() - start > 1/3 and time() - start < 2/3:
            draw.circle(
                surface=surface,
                color="white",
                center=(width/2-height/17, height/2+height/17),
                radius=height/32*(2-calculate2((time()-start-1/3)*3)),
            )
            draw.circle(
                surface=surface,
                color="black",
                center=(width/2-height/17, height/2+height/17),
                radius=height/36*(2-calculate2((time()-start-1/3)*3)),
                width=round(height/32-height/36)
            )
        elif time() - start > 2/3:
            draw.circle(
                surface=surface,
                color="white",
                center=(width/2-height/17, height/2+height/17),
                radius=height/32,
            )
            draw.circle(
                surface=surface,
                color="black",
                center=(width/2-height/17, height/2+height/17),
                radius=height/36,
                width=round(height/32-height/36)
            )

        if time() - start > 2/3 and time() - start < 1:
            draw.circle(
                surface=surface,
                color="black",
                center=(width/2+height/17, height/2),
                radius=height/32*(2-calculate2((time()-start-2/3)*3)),
            )
            draw.circle(
                surface=surface,
                color="white",
                center=(width/2+height/17, height/2),
                radius=height/36*(2-calculate2((time()-start-2/3)*3)),
                width=round(height/32-height/36)
            )
        elif time() - start > 1:
            draw.circle(
                surface=surface,
                color="black",
                center=(width/2+height/17, height/2),
                radius=height/32,
            )
            draw.circle(
                surface=surface,
                color="white",
                center=(width/2+height/17, height/2),
                radius=height/36,
                width=round(height/32-height/36)
            )

        write(
            surface=surface,
            text="按 ESC 键跳过",
            position=(width*0.1, height*0.05),
            font=fonts.TiejiliSC,
            size=height*0.05,
            color="white"
        )

        display.update()

    start = time()
    while time() - start < 1:
        try:width, height, fullscreen = actionListener(fullscreen)
        except KeyboardInterrupt:
            try:
                mixer.Sound("sounds/newStone.mp3").play()
            except error:pass
            return fullscreen

        surface.fill(DEEPGRAY)
        
        draw.rect(
            surface=surface,
            color="black",
            rect=(
                width/2-height/16-height/12,
                height/2-height/16-height/12-height/12*calculate1(time()-start),
                height/8+height/6,
                height/8+height/6
            ),
            border_radius=round(0.5*height/12)
        )

        draw.rect(
            surface=surface,
            color = "white",
            rect=(
                width/2-height/16*1.8,
                height/2-height/16*1.8-height/12*calculate1(time()-start),
                height/16*3.6,
                height/16*3.6
            ),
            border_radius=round(0.1*height/12)
        )

        draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2-height/17, height/2.6-height/12*calculate1(time()-start)),
                end_pos=(width/2-height/17, height/2.6+height*0.6/2.6-height/12*calculate1(time()-start)),
                width=round(height/120)
            )
        draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2, height/2.6-height/12*calculate1(time()-start)),
                end_pos=(width/2, height/2.6+height*0.6/2.6-height/12*calculate1(time()-start)),
                width=round(height/120)
            )
        draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2+height/17, height/2.6-height/12*calculate1(time()-start)),
                end_pos=(width/2+height/17, height/2.6+height*0.6/2.6-height/12*calculate1(time()-start)),
                width=round(height/120)
            )
        draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2-height/8.5, height/2-height/17-height/12*calculate1(time()-start)),
                end_pos=(width/2-height/8.5+height/2.6*0.6, height/2-height/17-height/12*calculate1(time()-start)),
                width=round(height/120)
            )
        draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2-height/8.5, height/2-height/12*calculate1(time()-start)),
                end_pos=(width/2-height/8.5+height/2.6*0.6, height/2-height/12*calculate1(time()-start)),
                width=round(height/120)
            )
        draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2-height/8.5, height/2+height/17-height/12*calculate1(time()-start)),
                end_pos=(width/2-height/8.5+height/2.6*0.6, height/2+height/17-height/12*calculate1(time()-start)),
                width=round(height/120)
            )

        draw.circle(
            surface=surface,
            color="black",
            center=(width/2, height/2-height/17-height/12*calculate1(time()-start)),
            radius=height/32,
        )
        draw.circle(
            surface=surface,
            color="white",
            center=(width/2, height/2-height/17-height/12*calculate1(time()-start)),
            radius=height/36,
            width=round(height/32-height/36)
        )

        draw.circle(
            surface=surface,
            color="white",
            center=(width/2-height/17, height/2+height/17-height/12*calculate1(time()-start)),
            radius=height/32,
        )
        draw.circle(
            surface=surface,
            color="black",
            center=(width/2-height/17, height/2+height/17-height/12*calculate1(time()-start)),
            radius=height/36,
            width=round(height/32-height/36)
        )

        draw.circle(
            surface=surface,
            color="black",
            center=(width/2+height/17, height/2-height/12*calculate1(time()-start)),
            radius=height/32,
        )
        draw.circle(
            surface=surface,
            color="white",
            center=(width/2+height/17, height/2-height/12*calculate1(time()-start)),
            radius=height/36,
            width=round(height/32-height/36)
        )

        write(
            surface=surface,
            text="围棋",
            position=(width/2, height*0.75-height/12*calculate1(time()-start)),
            font=font,
            size=height/6,
            color=Color(
                round(85+170*calculate1(time()-start)),
                round(85+170*calculate1(time()-start)),
                round(85+170*calculate1(time()-start))
            )
        )

        write(
            surface=surface,
            text="按 ESC 键跳过",
            position=(width*0.1, height*0.05),
            font=fonts.TiejiliSC,
            size=height*0.05,
            color="white"
        )

        display.update()

    start = time()
    while time() - start < 1:
        try:width, height, fullscreen = actionListener(fullscreen)
        except KeyboardInterrupt:
            try:
                mixer.Sound("sounds/newStone.mp3").play()
            except error:pass
            return fullscreen

        surface.fill(DEEPGRAY)
        
        draw.rect(
            surface=surface,
            color="black",
            rect=(
                width/2-height/16-height/12,
                height/2-height/16-height/12-height/12,
                height/8+height/6,
                height/8+height/6
            ),
            border_radius=round(0.5*height/12)
        )

        draw.rect(
            surface=surface,
            color = "white",
            rect=(
                width/2-height/16*1.8,
                height/2-height/16*1.8-height/12,
                height/16*3.6,
                height/16*3.6
            ),
            border_radius=round(0.1*height/12)
        )

        draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2-height/17, height/2.6-height/12),
                end_pos=(width/2-height/17, height/2.6+height*0.6/2.6-height/12),
                width=round(height/120)
            )
        draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2, height/2.6-height/12),
                end_pos=(width/2, height/2.6+height*0.6/2.6-height/12),
                width=round(height/120)
            )
        draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2+height/17, height/2.6-height/12),
                end_pos=(width/2+height/17, height/2.6+height*0.6/2.6-height/12),
                width=round(height/120)
            )
        draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2-height/8.5, height/2-height/17-height/12),
                end_pos=(width/2-height/8.5+height/2.6*0.6, height/2-height/17-height/12),
                width=round(height/120)
            )
        draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2-height/8.5, height/2-height/12),
                end_pos=(width/2-height/8.5+height/2.6*0.6, height/2-height/12),
                width=round(height/120)
            )
        draw.line(
                surface=surface,
                color="black",
                start_pos=(width/2-height/8.5, height/2+height/17-height/12),
                end_pos=(width/2-height/8.5+height/2.6*0.6, height/2+height/17-height/12),
                width=round(height/120)
            )

        draw.circle(
            surface=surface,
            color="black",
            center=(width/2, height/2-height/17-height/12),
            radius=height/32,
        )
        draw.circle(
            surface=surface,
            color="white",
            center=(width/2, height/2-height/17-height/12),
            radius=height/36,
            width=round(height/32-height/36)
        )

        draw.circle(
            surface=surface,
            color="white",
            center=(width/2-height/17, height/2+height/17-height/12),
            radius=height/32,
        )
        draw.circle(
            surface=surface,
            color="black",
            center=(width/2-height/17, height/2+height/17-height/12),
            radius=height/36,
            width=round(height/32-height/36)
        )

        draw.circle(
            surface=surface,
            color="black",
            center=(width/2+height/17, height/2-height/12),
            radius=height/32,
        )
        draw.circle(
            surface=surface,
            color="white",
            center=(width/2+height/17, height/2-height/12),
            radius=height/36,
            width=round(height/32-height/36)
        )

        write(
            surface=surface,
            text="围棋",
            position=(width/2, height*0.75-height/12),
            font=font,
            size=height/6,
            color=Color(
                round(85+170),
                round(85+170),
                round(85+170)
            )
        )

        write(
            surface=surface,
            text="按 ESC 键跳过",
            position=(width*0.1, height*0.05),
            font=fonts.TiejiliSC,
            size=height*0.05,
            color="white"
        )

        display.update()

    start = time()
    while time() - start < 1:
        try:width, height, fullscreen = actionListener(fullscreen)
        except KeyboardInterrupt:
            try:
                mixer.Sound("sounds/newStone.mp3").play()
            except error:pass
            return fullscreen

        surface.fill(DEEPGRAY)
        
        draw.rect(
            surface=surface,
            color=Color(round(85*(time()-start)), round(85*(time()-start)), round(85*(time()-start))),
            rect=(
                width/2-height/16-height/12,
                height/2-height/16-height/12-height/12,
                height/8+height/6,
                height/8+height/6
            ),
            border_radius=round(0.5*height/12)
        )

        draw.rect(
            surface=surface,
            color = Color(round(255-170*(time()-start)), round(255-170*(time()-start)), round(255-170*(time()-start))),
            rect=(
                width/2-height/16*1.8,
                height/2-height/16*1.8-height/12,
                height/16*3.6,
                height/16*3.6
            ),
            border_radius=round(0.1*height/12)
        )

        draw.line(
                surface=surface,
                color=Color(round(85*(time()-start)), round(85*(time()-start)), round(85*(time()-start))),
                start_pos=(width/2-height/17, height/2.6-height/12),
                end_pos=(width/2-height/17, height/2.6+height*0.6/2.6-height/12),
                width=round(height/120)
            )
        draw.line(
                surface=surface,
                color=Color(round(85*(time()-start)), round(85*(time()-start)), round(85*(time()-start))),
                start_pos=(width/2, height/2.6-height/12),
                end_pos=(width/2, height/2.6+height*0.6/2.6-height/12),
                width=round(height/120)
            )
        draw.line(
                surface=surface,
                color=Color(round(85*(time()-start)), round(85*(time()-start)), round(85*(time()-start))),
                start_pos=(width/2+height/17, height/2.6-height/12),
                end_pos=(width/2+height/17, height/2.6+height*0.6/2.6-height/12),
                width=round(height/120)
            )
        draw.line(
                surface=surface,
                color=Color(round(85*(time()-start)), round(85*(time()-start)), round(85*(time()-start))),
                start_pos=(width/2-height/8.5, height/2-height/17-height/12),
                end_pos=(width/2-height/8.5+height/2.6*0.6, height/2-height/17-height/12),
                width=round(height/120)
            )
        draw.line(
                surface=surface,
                color=Color(round(85*(time()-start)), round(85*(time()-start)), round(85*(time()-start))),
                start_pos=(width/2-height/8.5, height/2-height/12),
                end_pos=(width/2-height/8.5+height/2.6*0.6, height/2-height/12),
                width=round(height/120)
            )
        draw.line(
                surface=surface,
                color=Color(round(85*(time()-start)), round(85*(time()-start)), round(85*(time()-start))),
                start_pos=(width/2-height/8.5, height/2+height/17-height/12),
                end_pos=(width/2-height/8.5+height/2.6*0.6, height/2+height/17-height/12),
                width=round(height/120)
            )

        draw.circle(
            surface=surface,
            color=Color(round(85*(time()-start)), round(85*(time()-start)), round(85*(time()-start))),
            center=(width/2, height/2-height/17-height/12),
            radius=height/32,
        )
        draw.circle(
            surface=surface,
            color=Color(round(255-170*(time()-start)), round(255-170*(time()-start)), round(255-170*(time()-start))),
            center=(width/2, height/2-height/17-height/12),
            radius=height/36,
            width=round(height/32-height/36)
        )

        draw.circle(
            surface=surface,
            color=Color(round(255-170*(time()-start)), round(255-170*(time()-start)), round(255-170*(time()-start))),
            center=(width/2-height/17, height/2+height/17-height/12),
            radius=height/32,
        )
        draw.circle(
            surface=surface,
            color=Color(round(85*(time()-start)), round(85*(time()-start)), round(85*(time()-start))),
            center=(width/2-height/17, height/2+height/17-height/12),
            radius=height/36,
            width=round(height/32-height/36)
        )

        draw.circle(
            surface=surface,
            color=Color(round(85*(time()-start)), round(85*(time()-start)), round(85*(time()-start))),
            center=(width/2+height/17, height/2-height/12),
            radius=height/32,
        )
        draw.circle(
            surface=surface,
            color=Color(round(255-170*(time()-start)), round(255-170*(time()-start)), round(255-170*(time()-start))),
            center=(width/2+height/17, height/2-height/12),
            radius=height/36,
            width=round(height/32-height/36)
        )

        write(
            surface=surface,
            text="围棋",
            position=(width/2, height*0.75-height/12),
            font=font,
            size=height/6,
            color=Color(round(255-170*(time()-start)), round(255-170*(time()-start)), round(255-170*(time()-start)))
        )

        write(
            surface=surface,
            text="按 ESC 键跳过",
            position=(width*0.1, height*0.05),
            font=fonts.TiejiliSC,
            size=height*0.05,
            color="white"
        )

        display.update()

    return fullscreen

if __name__ == "__main__":
    window = display.set_mode(flags=FULLSCREEN)
    showAnimation(window)
    window.fill("#555555")
    while True:
        for e in event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                sys.exit()
