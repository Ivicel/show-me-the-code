import sys
import re
from PIL import Image, ImageDraw, ImageFont

class NotAPictureError(Exception):
	def __init__(self, message):
		self.message = message

def make_badge_count(picture, num, font=None, fill=None):
	if picture is None:
		raise FileNotFoundErro("can't not find the picture")
	if re.search('(png|jpg|jpeg|gif)$', picture, re.IGNORECASE) is None:
		raise NotAPictureError('this file is not a picture')
	fill_fallback = 'red'
	if num is None:
		raise ValueError("you don't input a number")
	font_fallback = ImageFont.truetype('Arial.ttf', size=25)
	font = font_fallback if font is None else font
	fill = fill_fallback if fill is None else fill
	im = Image.open(picture)
	location = (im.width * 0.82, im.height * 0.075)
	draw = ImageDraw.Draw(im)
	draw.text(location, text=num, fill=fill, font=font)
	del draw
	im.save(picture)


if __name__ == '__main__':
	if len(sys.argv) < 3:
		print('error!!!!\n')
		print('Usage: ' + sys.argv[0] + ' pictureName ' + 'number\n')
		sys.exit(-1)
	make_badge_count(sys.argv[1], sys.argv[2])