import sys, os
from PIL import Image
from scipy import ndimage
import cv2
import numpy as np
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import(
	QGridLayout, QPushButton, QLabel, QFileDialog, QMessageBox, QWidget, QMainWindow, QApplication
)


class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		
		self.setWindowTitle("Convert A4 to F4 Scanned Paper")
		self.font = QFont()
		self.font.setPointSize(11)
		self.layout = QGridLayout()
		
		self.inp_top_label = QLabel('Input Top Image')
		self.inp_bot_label = QLabel('Input Bottom Image')
		self.out_label = QLabel('Output File Name')
		self.inp_top_name = QLabel()
		self.inp_bot_name = QLabel()
		self.out_name = QLabel()
		self.inp_top_but = QPushButton('Select File')
		self.inp_top_but.clicked.connect(self.inp_top)
		self.inp_bot_but = QPushButton('Select File')
		self.inp_bot_but.clicked.connect(self.inp_bot)
		self.out_but = QPushButton('Select File')
		self.out_but.clicked.connect(self.out_file)
		self.conv_but = QPushButton('Merge Image')
		self.conv_but.clicked.connect(self.conv_run)
		
		# Layout Setting
		self.layout.addWidget(self.inp_top_label, 0, 0, 1, 1)
		self.layout.addWidget(self.inp_top_but, 1, 0, 1, 2)
		self.layout.addWidget(self.inp_top_name, 1, 1, 1, 1)
		self.layout.addWidget(self.inp_bot_label, 2, 0, 1, 1)
		self.layout.addWidget(self.inp_bot_but, 3, 0, 1, 2)
		self.layout.addWidget(self.inp_bot_name, 3, 1, 1, 1)
		self.layout.addWidget(self.out_label, 4, 0, 1, 1)
		self.layout.addWidget(self.out_but, 5, 0, 1, 2)
		self.layout.addWidget(self.out_name, 5, 1, 1, 1)
		self.layout.addWidget(self.conv_but, 7, 0, 2, 2)
		
		self.widget = QWidget()
		self.widget.setMinimumSize(QSize(400, 300))
		self.widget.setLayout(self.layout)
		self.widget.setFont(self.font)
		self.setCentralWidget(self.widget)
		
	def inp_top(self):
		global top_name
		top_name, _ = QFileDialog.getOpenFileName(self, 'Open File', './', "Image Files (*.jpg *.png)")
		self.inp_top_but.setText(top_name)
	
	def inp_bot(self):
		global bot_name
		bot_name, _ = QFileDialog.getOpenFileName(self, 'Open File', './', "Image Files (*.jpg *.png)")
		self.inp_bot_but.setText(bot_name)
		
	def out_file(self):
		global out_name
		out_name, _ = QFileDialog.getSaveFileName(self, 'Open File', './', "Image Files (*.jpg *.png)")
		self.out_but.setText(out_name)
	
	def conv_run(self):
		img1 = cv2.imread(top_name)
		img2 = cv2.imread(bot_name)

		img1c = img1[0:3376, 0:2481]
		img1h1 = Image.new(mode='RGB', size=(29, 3376), color=(255, 255, 255))
		img1hp = np.concatenate((img1h1, img1c), axis=1)
		img1h2 = Image.new(mode='RGB', size=(29, 3376), color=(255, 255, 255))
		img1hf = np.concatenate((img1hp, img1h2), axis=1)
		img1v1 = Image.new(mode='RGB', size=(2539, 522), color=(255, 255, 255))
		img1vf = np.concatenate((img1hf, img1v1), axis=0)

		imgr = ndimage.rotate(img2, 180)
		img2c = imgr[130:3506, 0:2481]
		img2v = Image.new(mode='RGB', size=(2481, 495), color=(255, 255, 255))
		img2v2 = Image.new(mode='RGB', size=(2481, 27), color=(255, 255, 255))
		img2vf = np.concatenate((img2v, img2c), axis=0)
		img2vf2 = np.concatenate((img2vf, img2v2), axis=0)
		img2vs = img2vf2[0:3898, 0:2467]
		img2h = Image.new(mode='RGB', size=(72, 3898), color=(255, 255, 255))
		img2hf = np.concatenate((img2h, img2vs), axis=1)

		imgtop = img1vf[0:1949, 0:2539]
		imgbottom = img2hf[1949:3898, 0:2539]
		imgfinal = np.concatenate((imgtop, imgbottom), axis=0)
		cv2.imwrite(out_name, imgfinal)

		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())
