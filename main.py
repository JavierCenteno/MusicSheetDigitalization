import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
import random

ts = time.time()

img1 = cv2.imread('./output/example_3.png', 0)
img = cv2.transpose(img1);

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

# Se obtienen los valores n1, n2, d1, d2

n = list()
d = list()

N = max(list(histBlack.values()))/3.0
D = max(list(histWhite.values()))/3.0

for dist in histBlack:
	if histBlack[dist] > N:
		n.append(dist)

for dist in histWhite:
	if histWhite[dist] > D:
		d.append(dist)
n1 = min(n)
n2 = max(n)
d1 = min(d)
d2 = max(d)

print(n1, n2, d1, d2)

I = int((5*n2 + 4*n2)*1.2)

width = len(img1[0])

dx = int(width/50)

#a = random.randint(width/5, 2*width/5)
b = random.randint(2*width/5, 3*width/5)
#c = random.randint(3*width/5, 4*width/5)

#a = img1[:, a:a+dx]
b = img1[:, b:b+dx]
#c = img1[:, c:c+dx]

proy = [sum(i) for i in b]
proy = max(proy) - proy

plt.plot(proy)
plt.show()

# firstGuess = list()
# first = True
# i=0
# while i < len(proy): # Mientras solo se guardan la primera y ultima linea
# 	if proy[i] == 0:
# 		StaffFound = 0
# 		inStaff = True
# 		black = 0
# 		white = 0
# 		keep = True
# 		for j in range(I):
# 			if keep and first:
# 				first = False
# 				print()
# 				if inStaff:
# 					if proy[i+j] == 0:
# 						black+=1
# 					else:
# 						inStaff = False
# 						if black >= n1 and black <= n2:
# 								StaffFound+=1
# 								if StaffFound == 5:
# 									keep = False
# 									firstGuess.append((i, i+j-1))
# 									i = i + j - 1
# 				else:
# 					if proy[i+j] != 0:
# 						white+=1
# 					else:
# 						inStaff = True
# 						if white >= d1 and white <= d2:
# 								keep = False
# 	i+=1
# print(len(firstGuess), ":)")


#print(round(ts))

