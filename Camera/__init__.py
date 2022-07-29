import cv2
import time
import requests
import threading
import numpy as np
from typing import *





__all__=["Webcam"]





class Webcam:
	def __init__(self,host:str,port:int,login:str,password:str):
		self.host=host
		self.port=port

		self.login=login
		self.password=password

		self.videoUrl=f"http://{self.login}:{self.password}@{self.host}:{self.port}/video"
		self.audioUrl=f"http://{self.login}:{self.password}@{self.host}:{self.port}/audio.wav"

		self.videoCapture=None
		self.audioCapture=None

		self.videoConnected=False
		self.audioConnected=False

		self.chunkSize=1024
		self.running=True



		self.videoThread=threading.Thread(None,self.connectVideoLoop,"Video",(),{},daemon=True)
		self.audioThread=threading.Thread(None,self.connectAudioLoop,"Audio",(),{},daemon=True)

		self.videoThread.start()
		self.audioThread.start()







	def connectVideoLoop(self):
		while self.running:
			time.sleep(1)


			if (self.videoCapture!=None and self.videoCapture.isOpened()):
				self.videoConnected=True


			else:
				self.videoConnected=False
				self.videoCapture=cv2.VideoCapture(self.videoUrl,cv2.CAP_FFMPEG)
				print("Reconnecting...")







	def connectAudioLoop(self):
		while self.running:
			time.sleep(1)


			if (self.audioCapture!=None):
				...

			else:
				try:
					self.audioCapture=requests.get(
						self.audioUrl,
						headers={
							"User-Agent":"Webcam/1.0",
							"Connection":"Keep-Alive",
							"Content-Type":"audio/wav; charset=utf-8",
						},
						stream=True,
						timeout=2,
					)



					if (self.audioCapture.status_code==200):
						self.audioConnected=True


					else:
						self.audioCapture=None
						self.audioConnected=False


				except:
					self.audioCapture=None
					self.audioConnected=False








	def readVideo(self):
		if (self.videoConnected):
			result,frame=self.videoCapture.read()
			

			if (result):
				return result,frame

		

		return False,None







	def readAudio(self):
		if (self.audioConnected):
			data=self.audioCapture.raw.read(self.chunkSize,decode_content=True)

			if (data):
				return True,data


		return False,None








import pyaudio
audio=pyaudio.PyAudio()

# stream=audio.open(in)


w=Webcam("192.168.1.180",9999,"Atlis","6013")


while w.running:
	result,frame=w.readVideo()
	result_,frame_=w.readAudio()

	if (result):
		cv2.imshow("Stream",frame)
	
	cv2.waitKey(1)




