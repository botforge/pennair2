import sys
import os
import cv2
import numpy as np
from scipy.misc import imresize

class Stream:

		def __init__(self,mode="webcam",src=""):

			if ('pic' in mode) or ('img' in mode) or ('image' in mode):
				self.mode = 'pic'
			elif ('vid' in mode):
				self.mode = 'vid'
			else:
				self.mode = 'cam'

			self.src = src
			self.isfolder = (not '.' in src)
			if self.isfolder and self.mode != 'cam':
				self.files = []
				self.filenum = -1
				self.getfiles(src)

			if self.mode == 'vid':
				if self.isfolder:
					self.stream = cv2.VideoCapture(self.nextfile())
				else:
					self.stream = cv2.VideoCapture(src)
			elif self.mode == 'cam':
				self.stream = cv2.VideoCapture(0)

			self.imgnum = 0


		# 'Private' Functions

		def __iter__(self):
			return self

		def next(self):
			img = self.get()
			if img is None:
				raise StopIteration
			else:
				return img

		def getfiles(self,folder):
			os.chdir(os.path.join(os.getcwd(),folder))
			self.files = os.listdir(os.getcwd())

		def nextfile(self):
			while self.filenum < len(self.files)-1:
				self.filenum += 1
				if self.mode == 'vid':
					if self.files[self.filenum].endswith('.m4v') or \
					   self.files[self.filenum].endswith('.mp4') or \
					   self.files[self.filenum].endswith('.mov'):
						return self.files[self.filenum]
				elif self.mode == 'pic':
					if self.files[self.filenum].endswith('.jpg') or \
					   self.files[self.filenum].endswith('.png') or \
					   self.files[self.filenum].endswith('.bmp'):
						return self.files[self.filenum]
			return None

		def pic(self):
			try:
				if self.isfolder:
					image = cv2.imread(self.nextfile())
				else:
					image = cv2.imread(self.src)
			except Exception as err:
				return None
			return np.array(image)

		def vid(self):
			try:
				success,image = self.stream.read()
				if not success and self.isfolder:
					self.stream = cv2.VideoCapture(self.nextfile())
					_,image = self.stream.read()
			except Exception as err:
				return None
			return np.array(image)

		def cam(self):
			success,image = self.stream.read()
			if success:
				return np.array(image)
			else:
				return None


		# Public Functions

		# Returns the next frame as a numpy array
		def get(self):
			if self.mode == 'pic':
				image = self.pic()
			elif self.mode == 'vid':
				image = self.vid()
			elif self.mode == 'cam':
				image = self.cam()
			if image.dtype is np.dtype('object'):
				return None
			return image

		# type(size)==int: percent of current size
		# type(size)==float: fraction of current size
		# type(size)==tuple: new size
		def resize(self,image,size):
			return imresize(image,size)

		# returns grayscale image
		def im2gray(self,image):
			return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		# if pause=True, then the program will wait on the current frame until
		# you press a key (hold a key to run in real time)
		# if pause=False, then the program will run in real time until q is pressed
		def show(self,image,name=None,pause=False,resize=True):
			if name is None:
				name = str(self.imgnum)
				self.imgnum += 1
			if image is None:
				sys.exit()
			if resize:
				vertheight = 600 # Vertical height of the output, if resize=True
				aspectratio = float(image.shape[1])/float(image.shape[0])
				image = imresize(image,(vertheight,int(vertheight*aspectratio)))
			cv2.imshow(name,image)
			if pause:
				if cv2.waitKey(0) & 0xFF == ord('q'):
					sys.exit()
			else:
				if cv2.waitKey(2) & 0xFF == ord('q'):
					sys.exit()

		# type(mark)== 2-tuple or 2-tuple: (x,y) draws points
		# type(mark)== 3-tuple or 3-tuple: (x,y,radius) draws circles
		# type(mark)== 4-tuple or 4-tuple: (x,y,length,height) draws rectangles
		# type(mark)== string: 'text' places text in corner
		# type(mark)== (string,int,int): ('text',x,y) places text at position
		# if xyaxis=True then it will draw in xy coordinates, not image coordinates
		# copy=False: updates original. copy=True: does not edit original, returns new img
		def mark(self,image,marks,color=(0,0,255),xyaxis=False,size=4,copy=False):
			color = (color[2],color[1],color[0])

			if copy:
				image = np.copy(image)
			if type(marks) != list:
				marks = [marks]

			for mark in marks:
				if type(mark[0]) == str:
					if type(mark) == str:
						mark = [mark]
						if xyaxis:
							pos = (5,image.shape[0]-10)
						else:
							pos = (5,16*size+5)
					else:
						if xyaxis:
							pos = (int(mark[1]),int(image.shape[0]-mark[2]))
						else:
							pos = (int(mark[1]),int(mark[2]))
					cv2.putText(image,mark[0],pos,cv2.FONT_HERSHEY_COMPLEX_SMALL,size,color,size)
				elif len(mark) == 2:
					if xyaxis:
						mark = (mark[0],image.shape[0]-mark[1])
					cv2.circle(image,(int(mark[0]),int(mark[1])),1,color,size)
				elif len(mark) == 3:
					if xyaxis:
						mark = (mark[0],image.shape[0]-mark[1],mark[2])
					cv2.circle(image,(int(mark[0]),int(mark[1])),int(mark[2]),color,size)
				elif len(mark) == 4:
					if xyaxis:
						mark = (mark[0],image.shape[0]-mark[1],mark[2],mark[3])
					cv2.rectangle(image,(int(mark[0]-mark[2]/2),int(mark[1]-mark[3]/2)),
									    (int(mark[0]+mark[2]/2),int(mark[1]+mark[3]/2)),color,size)
			return image



#Example Usage

#import imgstream
#stream = imgstream.Stream(mode='image',src='imgfolder')
#while True:
#	img = stream.get()
#	img = stream.mark(img,[('output stream',40,20),(300,300),(200,250,30)],size=3,xyaxis=True)
#	stream.show(img,'Output')

from random import random

if __name__ == '__main__':
	stream = Stream(mode='webcam')
	for img in stream:
		img = stream.mark(img,['Testing'],size=2)
		stream.show(img,'Output',pause=False,resize=True)

