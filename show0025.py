#!/usr/bin/env python3
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from base64 import b64encode
from uuid import uuid4
import json



def get_token(key):
	url = 'https://api.cognitive.microsoft.com/sts/v1.0/issueToken'
	header = {
		'Content-Type': 'application/x-www-form-urlencoded',
		'Content-Length': 0,
		'Ocp-Apim-Subscription-Key': key
	}

	req = Request(url, headers=header, method='POST')
	try:
		resp = urlopen(req)
		token = resp.read().decode('utf-8')
	except:
		raise SystemExit("Can not get the token")
	return token

def recognize_audio(data, token):
	header = {
		'Authorization': 'Bearer %s' % token,
		'Content-Type': 'audio/wav; rate=8000'
	}
	data = open(data, 'rb').read()
	# data = urlencode(data, encoding='utf-8').encode('utf-8')
	version = '3.0'
	requestid = str(uuid4())
	app_id = 'D4D52672-91D7-4C74-8AD8-42B1D98141A5'
	_format = 'json'
	locale = 'zh-CN'
	device_os = 'linux'
	scenarios = 'ulm'
	instanceid = requestid

	url = 'https://speech.platform.bing.com/recognize?version={version}&' \
		'requestid={requestid}&appid={app_id}&format={_format}&locale={locale}' \
		'&device.os={device_os}&scenarios={scenarios}&instanceid={instanceid}'.format(
			version=version,
			requestid=requestid,
			app_id=app_id,
			_format=_format,
			locale=locale,
			device_os=device_os,
			scenarios=scenarios,
			instanceid=instanceid
		)
	req = Request(url, data=data, headers=header)
	resp = urlopen(req)
	result = resp.read().decode('utf-8')
	print(result)
	return result

try:
	import pyaudio, wave
	def record():
		CHUNK = 1024
		FORMAT = pyaudio.paInt16
		CHANNELS = 2
		RATE = 44100
		RECORD_SECONDS = 3
		WAVE_OUTPUT_FILENAME = 'output.wav'

		p = pyaudio.PyAudio()
		stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
			frames_per_buffer=CHUNK)
		print('recording......')
		frames = []
		for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
			data = stream.read(CHUNK)
			frames.append(data)
		print('done recording...')
		stream.stop_stream()
		stream.close()
		p.terminate()
		# return b''.join(frames)
		wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(frames))
		wf.close()
except ImportError:
	print('You should install pyaudio(https://people.csail.mit.edu/hubert/pyaudio/)')

def open_browser(data):
	data = json.loads(data)
	try:
		if '百度' in data['results'][0]['lexical']:
			import webbrowser
			webbrowser.open_new('https://www.baidu.com')
	except:
		print('asdflakjf;')

def init(key):
	record()
	token = get_token(key)
	result = recognize_audio('output.wav', token=token)
	open_browser(result)

if __name__ == '__main__':
	init(key='you-code')