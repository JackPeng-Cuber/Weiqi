from PIL import Image, ImageDraw, ImageFont
from numpy import array
from tqdm import trange

size = 1024

image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype(font="fonts/STXingKa.ttf", size=size//3)

# 大方块
draw.rectangle(
    xy=(size*0.1, size*0.1, size*0.9, size*0.9),
    fill="white"
)

# 边框
draw.rectangle(
    xy=(size*0.05, size*0.1, size*0.1, size*0.9),
    fill="black"
)

draw.rectangle(
    xy=(size*0.1, size*0.05, size*0.9, size*0.1),
    fill="black"
)

draw.rectangle(
    xy=(size*0.9, size*0.1, size*0.95, size*0.9),
    fill="black"
)

draw.rectangle(
    xy=(size*0.1, size*0.9, size*0.9, size*0.95),
    fill="black"
)

# 圆角
draw.pieslice(
    xy=(size*0.05, size*0.05, size*0.15, size*0.15),
    start=180,
    end=-90,
    fill="black"
)

draw.pieslice(
    xy=(size*0.85, size*0.05, size*0.95, size*0.15),
    start=-90,
    end=0,
    fill="black"
)

draw.pieslice(
    xy=(size*0.05, size*0.85, size*0.15, size*0.95),
    start=90,
    end=180,
    fill="black"
)

draw.pieslice(
    xy=(size*0.85, size*0.85, size*0.95, size*0.95),
    start=0,
    end=90,
    fill="black"
)

# 横线
draw.line(
    xy=(size*0.3, size*0.1, size*0.3, size*0.9),
    fill="black",
    width=size//50
)

draw.line(
    xy=(size*0.5, size*0.1, size*0.5, size*0.9),
    fill="black",
    width=size//50
)

draw.line(
    xy=(size*0.7, size*0.1, size*0.7, size*0.9),
    fill="black",
    width=size//50
)

# 纵线
draw.line(
    xy=(size*0.1, size*0.3, size*0.9, size*0.3),
    fill="black",
    width=size//50
)

draw.line(
    xy=(size*0.1, size*0.5, size*0.9, size*0.5),
    fill="black",
    width=size//50
)

draw.line(
    xy=(size*0.1, size*0.7, size*0.9, size*0.7),
    fill="black",
    width=size//50
)

# 白棋
draw.ellipse(
    xy=(size*0.2, size*0.6, size*0.4, size*0.8),
    fill="white",
    outline="black",
    width=size//50
)

draw.ellipse(
    xy=(size*0.19, size*0.59, size*0.41, size*0.81),
    outline="white",
    width=size//100
)

# 黑棋1
draw.ellipse(
    xy=(size*0.4, size*0.2, size*0.6, size*0.4),
    fill="black",
    outline="white",
    width=size//50
)

draw.ellipse(
    xy=(size*0.39, size*0.19, size*0.61, size*0.41),
    outline="black",
    width=size//100
)

# 黑棋2
draw.ellipse(
    xy=(size*0.6, size*0.4, size*0.8, size*0.6),
    fill="black",
    outline="white",
    width=size//50
)

draw.ellipse(
    xy=(size*0.59, size*0.39, size*0.81, size*0.61),
    outline="black",
    width=size//100
)

# 文字
temp = Image.new("L", (size, size))
tempDraw = ImageDraw.Draw(temp)
tempDraw.text(
    xy=(size*0.5-size/3, size*0.5-size/6),
    text="围棋",
    fill="white",
    font=font,
)
for x in trange(size):
    for y in range(size):
        if image.getpixel((x, y))[3] == 0:
            continue
        imageColor = array(image.getpixel((x, y))[:3])
        tempColor = temp.getpixel((x, y))
        image.putpixel((x, y), tuple(imageColor+(127-imageColor)*tempColor//512))

image.save("textures/icon.png")
image.show()