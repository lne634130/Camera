import cv2
import time
import requests
import threading
import numpy as np
from typing import *





__all__=["Webcam","Webcam_Video","Webcam_Audio"]





class Webcam:



	# ~~~~~~~~~ Action Urls ~~~~~~~~~~
	ledUrl:str=					"{host}/{value}torch" # enable/disable
	zoomUrl:str=				"{host}/ptz?zoom={value}" # 0-100
	qualityUrl:str=				"{host}/settings/quality?set={value}" # 0-100
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


	# ~~~~~~~~~ Action Vars ~~~~~~~~~~
	led_:bool=					False
	zoom_:float=				0.0
	quality_:float=				0.0
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~~~~ New ~~~~~~~~~~~~~~
	def __new__(cls,host:str,port:int,login:str=None,password:str=None):
		self=object.__new__(cls)


		if (login!=None and password!=None):
			self.host=f"http://{login}:{password}@{host}:{port}"

		else:
			self.host=f"http://{host}:{port}"



		self.videoHost=f"{self.host}/video"
		self.audioHost=f"{self.host}/audio.wav"


		self.running=True


		self.videoCapture=Webcam_Video(self.videoHost)
		self.audioCapture=Webcam_Audio(self.audioHost)


		return self
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





	# ~~~~~~~~~~~~ Close ~~~~~~~~~~~~~
	def close(self)->NoReturn:
		self.connected=False

		self.videoCapture.connected=False
		self.audioCapture.connected=False
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





	# ~~~~~~~~~~~~~~ Read ~~~~~~~~~~~~
	def readVideo(self)->Tuple[bool,np.ndarray]:
		return self.videoCapture.read()



	def readAudio(self)->Tuple[bool,np.ndarray]:
		return self.audioCapture.read()
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





	# ~~~~~~~~~~~~ Action ~~~~~~~~~~~~
	def action(self,url:str,value:Any)->bool:
		try:
			url=url.format(host=self.host,value=value)

			req=requests.get(
				url,
				headers={
					"User-Agent":"Webcam/1.0",
				},
				timeout=3,
				stream=False,
			)

			if (req.status_code==200):
				return True

		except:
			pass
		
		return False
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





	# ~~~~~~~~~~~~~~ LED ~~~~~~~~~~~~~
	@property
	def led(self)->bool:
		return self.led_



	@led.setter
	def led(self,value:bool)->NoReturn:
		if (value!=self.led_):

			v="disable"

			if (value):
				v="enable"

			result=self.action(self.ledUrl,v)

			if (result):
				self.led_=value
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





	# ~~~~~~~~~~~~~ Zoom ~~~~~~~~~~~~~
		@property
		def zoom(self)->float:
			return self.zoom_



		@zoom.setter
		def zoom(self,value:float)->NoReturn:
			if (isinstance(value,float)):
				if (value!=self.zoom_):
					
					perc=round(value*100)

					if (perc>100):
						perc=100



					result=self.action(self.zoomUrl,perc)
					
					if (result):
						self.zoom_=value
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





	# ~~~~~~~~~~~~ Quality ~~~~~~~~~~~
	@property
	def quality(self)->float:
		return self.quality_



	@quality.setter
	def quality(self,value:float)->NoReturn:
		if (isinstance(value,float)):
			if (value!=self.quality_):
					
				perc=round(value*100)

				if (perc>100):
					perc=100



				result=self.action(self.qualityUrl,perc)
					
				if (result):
					self.quality_=value
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~











class Webcam_Video:
	# ~~~~~~~~~~~~~ New ~~~~~~~~~~~~~~
	def __new__(cls,host:str):
		self=object.__new__(cls)


		self.host=host

		self.running=True
		self.connected=False

		self.capture=cv2.VideoCapture()


		self.thread=threading.Thread(target=self.connectLoop,daemon=True)
		self.thread.start()


		return self
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





	# ~~~~~~~~~ Connect Loop ~~~~~~~~~
	def connectLoop(self)->NoReturn:
		while self.running:
			if (self.connected):
				time.sleep(1)

			else:
				self.connect()
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





	# ~~~~~~~~~~~~ Close ~~~~~~~~~~~~~
	def close(self)->NoReturn:
		self.connected=False
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





	# ~~~~~~~~~~~ Connect ~~~~~~~~~~~~
	def connect(self)->bool:
		self.connected=False


		if (self.capture.isOpened()):
			self.capture.release()


		self.capture.open(self.host)


		if (self.capture.isOpened()):
			self.connected=True


		return self.connected
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





	# ~~~~~~~~~~~~~ Read ~~~~~~~~~~~~~
	def read(self)->Tuple[bool,np.ndarray]:
		if (self.connected):
			result,frame=self.capture.read()


			if (result):
				return result,frame


			self.connected=False


		return False,None
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~













class Webcam_Audio:
	# ~~~~~~~~~~~~~ New ~~~~~~~~~~~~~~
	def __new__(cls,host:str):
		self=object.__new__(cls)


		self.host=host

		self.chunkSize=2048

		self.running=True
		self.connected=False

		self.capture=None


		self.thread=threading.Thread(target=self.connectLoop,daemon=True)
		self.thread.start()


		return self
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





	# ~~~~~~~~~ Connect Loop ~~~~~~~~~
	def connectLoop(self)->NoReturn:
		while self.running:
			if (self.connected):
				time.sleep(1)

			else:
				self.connect()
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





	# ~~~~~~~~~~~~ Close ~~~~~~~~~~~~~
	def close(self)->NoReturn:
		self.connected=False
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





	# ~~~~~~~~~~~ Connect ~~~~~~~~~~~~
	def connect(self)->bool:
		self.connected=False


		try:
			self.capture=requests.get(
				self.host,
				headers={
					"User-Agent":"Webcam/1.0",
					"Connection":"Keep-Alive",
					"Content-Type":"audio/wav; charset=utf-8",
				},
				timeout=3,
				stream=True
			)

			if (self.capture.status_code==200):
				self.connected=True

		except:
			...


		return self.connected
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





	# ~~~~~~~~~~~~~ Read ~~~~~~~~~~~~~
	def read(self)->Tuple[bool,np.ndarray]:
		if (self.connected):
			data=self.capture.raw.read(self.chunkSize)

			if (data):
				newData=np.frombuffer(data,np.int8)

				return True,newData


			self.connected=False


		return False,None
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~











from Virtual import *

cap=Webcam("192.168.1.180",9999,"Atlis","6013")
vir=VirtualCamera(1920,1080,60)


error=cv2.imread("../Disconnected.png")



while cap.running:
	result,frame=cap.readVideo()


	if (result):
		...
		

	else:
		frame=error


	frame=cv2.resize(frame,(vir.width,vir.height))
	frame=cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
	# frame=cv2.flip(frame,1)


	vir.data=frame
	vir.wait()








