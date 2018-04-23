#!/usr/bin/env python3
#-*-coding:utf-8-*-
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import random
#随机字母
def rndChar():
    return chr(random.randint(65,90))

#随机颜色1
def rndColor():
    return (random.randint(64,255), random.randint(64, 255), random.randint(64, 255))

#随机颜色2
def rndColor2():
    return (random.randint(32,127), random.randint(32,127), random.randint(32,127))

if __name__ == '__main__':
    width = 240
    height = 60
    image = Image.new('RGB', (width, height), (255, 255, 255))

    #创建Font对象
    font = ImageFont.truetype('E:\Administrator\Desktop\Programming practice\Python\廖雪峰\arial.tff', 36)

    #创建Draw对象
    draw = ImageDraw.Draw(image)

    #填充每个像素
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())

    #输出文字
    for t in range(4):
        draw.text((60 * t + 10, 10), rndColor(), font=font, fill=rndColor2())

    image.save('code.jpg', 'jpeg')