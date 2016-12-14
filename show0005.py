import os, sys, re
from PIL import ImageOps, Image


def crop_image(file, iphone_version='5', scale=True,):
	if not os.path.isfile(file) or \
		re.search('\.(png|gif|jpg|jpeg)$', file, re.IGNORECASE) is None:
		return False
	im = Image.open(file)
	if iphone_version == '5':
		iphone_width = 1136
		iphone_height = 640
	elif iphone_version = '6':
		iphone_width = 1334
		iphone_height = 750
	else:
		iphone_width = 1920
		iphone_height = 1080
	if scale:
		r1 = iphone_width / im.width
		r2 = iphone_height / im.height
		if r1 < 1 or  r2 < 1:
			ratio = r1 if r1 < r2 else r2
		else:
			return False
		width = int(im.width * ratio)
		height = int(im.height * ratio)
	else:
		if im.width < iphone_width and im.height < iphone_height:
			return False
		width = iphone_width if im.width > iphone_width else im.width
		height = iphone_height if im.height > iphone_height else im.height

	im2 = im.resize((width, height))
	index = file.rindex('.')
	im2.save(file[:index + 1] + '_iphone5' + file[index:])


if __name__ == '__main__':
	if len(sys.argv) < 2 and not os.path.isdir(sys.argv[1]):
		print('Usage: %s images_directory' % sys.argv[0])
		sys.exit(-1)
	for img in os.listdir(sys.argv[1]):
		crop_image(os.path.join(os.path.abspath(sys.argv[1]), img))