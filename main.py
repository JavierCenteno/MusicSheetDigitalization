import cv2
import time
import numpy as np
import matplotlib.pyplot as plt

ts = time.time()

img = cv2.imread('./output/example_3.png', 0)
img = cv2.transpose(img);

histBlack = dict()
histWhite = dict()

for col in range(0, len(img), 5):  # Se cuentan las ocurrencias de secuencias de pixeles blancos y negros en un quinto de las columnas de la imagen
	count = 0
	flag = True
	if img[col][0] == 0:
			flag = False
	for pixel in range(len(img[col])):
		if flag:
			if img[col][pixel] == 255:
				count+=1
			elif pixel == len(img[col]) - 1:
				if count not in histWhite:
					histWhite[count] = 0
				histWhite[count]+=1
			else:
				if count not in histWhite:
					histWhite[count] = 0
				histWhite[count]+=1
				count = 0
				flag = False
		else:
			if img[col][pixel] == 0:
				count+=1
			elif pixel == len(img[col]) - 1:
				if count not in histBlack:
					histBlack[count] = 0
				histBlack[count]+=1
			else:
				if count not in histBlack:
					histBlack[count] = 0
				histBlack[count]+=1
				count = 0
				flag = True

ts = time.time() -  ts
print(ts)

a = max(list(histBlack.keys())) + 1

bPlotX = np.linspace(1, a, a)
print(bPlotX)
bPlotY = np.zeros(len(bPlotX))
for key in histBlack:
	bPlotY[key] = histBlack[key]
plt.plot(bPlotX, bPlotY)
plt.show()





#print(round(ts))

