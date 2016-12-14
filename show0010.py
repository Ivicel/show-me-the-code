#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from random import choice, seed, randint
from datetime import datetime

def validation_code(size=(230, 70), font_style='Arial.ttf', font_size=45,
	filename='validation_code.png'):
	seed(datetime.now())
	letter_number = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ'
	im = Image.new('RGB', size, 0xffffff)
	draw = ImageDraw.Draw(im)
	# background
	for x in range(0, size[0], 1):
		for y in range(0, size[1], 1):
			draw.point((x, y), fill=randint(0, 0xffffff))
	# 第一个字左边缘位置
	x = size[0] // 12
	font = ImageFont.truetype(font_style, font_size)
	# 写入 4 个字符
	for i in range(0, 4):
		letter = choice(letter_number)
		y = randint(0, size[1] // 2 - font_size // 2)
		draw.text((x, y), fill=randint(0, 0xffffff), text=letter, font=font)
		x = x + size[0] // 4
	# 5 条干扰线
	for i in range(5):
		draw.line((randint(0, size[0]), randint(0, size[1]), 
			randint(0, size[0]), randint(0, size[1])),
			fill=randint(0, 0xffffff), width=2)
	# 锐化模糊
	im = im.filter(ImageFilter.SHARPEN)
	im = im.filter(ImageFilter.GaussianBlur(1))
	im.save(filename)
if __name__ == '__main__':
	validation_code()