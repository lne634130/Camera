import cv2
import time
import requests
import threading
import numpy as np
import pyvirtualcam
from typing import *





__all__=["VirtualCamera"]





class VirtualCamera:
	def __init__(self,width:int=1280,height:int=720,fps:int=20,*,fmt=pyvirtualcam.PixelFormat.RGB,device=None,backend=None):
		
		self.capture=pyvirtualcam.Camera(width,height,fps,fmt=fmt,device=device,backend=backend,print_fps=False)

		self.width=width
		self.height=height
		self.fps=fps

		self.fmt=fmt
		self.device=device
		self.backend=backend





	# ~~~~~~~~~~~~~ Data ~~~~~~~~~~~~~
	@property
	def data(self)->Tuple[bool,np.ndarray]:
		data=self.capture.frames_sent

		if (data==0):
			return False,0

		else:
			return True,data



	@data.setter
	def data(self,data:np.ndarray)->NoReturn:
		if (isinstance(data,np.ndarray) and data.dtype==np.uint8):
			self.capture.send(data)
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





	# ~~~~~~~~~~~~~ Wait ~~~~~~~~~~~~~
	def wait(self)->NoReturn:
		self.capture.sleep_until_next_frame()
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~