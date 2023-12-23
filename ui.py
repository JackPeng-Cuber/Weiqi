from pygame import *
from weiqi import inrange

init()

# 反色
def reverseColor(color):
    color = Color(color)
    return Color(255-color.r, 255-color.g, 255-color.b)

# 字体
class fonts:
    SourceHanSansSC = lambda size:font.Font("fonts/SourceHanSansSC-Regular.otf", round(size))
    STXingKa = lambda size:font.Font("fonts/STXingKa.ttf", round(size))
    STXinWei = lambda size:font.Font("fonts/STXinWei.ttf", round(size))
    TiejiliSC = lambda size:font.Font("fonts/TiejiliSC-Regular.ttf", round(size))

class Button:
    # 初始化
    def __init__(self, surface : Surface, position, size, text, font, color, borderRadius=None) -> None:
        self.surface = surface
        self.position = position
        self.size = size
        self.textSize = min(size[1], size[0]/len(text))*0.9
        self.text = text
        self.font = font
        self.color = color
        self.onButton = False
        self.mousePressing = False
        self.isPressing = False
        self.isJustPress = False
        if borderRadius != None:
            self.borderRadius = round(borderRadius)
        else:
            self.borderRadius = round(min(size)/3)

    # 绘制按钮
    def draw(self):
        x, y = self.position
        width, height = self.size
        self.textSize = min(height, width/len(self.text))*0.9
        if not self.isPressing:
            text = self.font(self.textSize).render(self.text, True, self.color)
            if self.onButton:
                draw.rect(self.surface, self.color, (x, y, width, height), 10, self.borderRadius)
            self.surface.blit(text, text.get_rect(center=(x + width / 2, y + height / 2)))
        else:
            text = self.font(self.textSize).render(self.text, True, reverseColor(self.color))
            draw.rect(self.surface, self.color, (x, y, width, height), border_radius=self.borderRadius)
            self.surface.blit(text, text.get_rect(center=(x + width / 2, y + height / 2)))

    # 更新按钮
    def update(self, mousePressing=False):
        x, y = self.position
        width, height = self.size
        mouseX, mouseY = mouse.get_pos()
        self.onButton = inrange(mouseX, x, x+width) and inrange(mouseY, y, y+height)
        if inrange(mouseX, x, x+width) and inrange(mouseY, y, y+height) and mousePressing:
            self.isJustPress = not self.mousePressing and mousePressing and not self.isPressing
            self.isPressing = True
        else:
            self.isJustPress = False
            self.isPressing = False
        self.mousePressing = mousePressing
