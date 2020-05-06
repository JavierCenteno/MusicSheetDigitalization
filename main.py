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

width = len(img1[0])

dx = int(width/60)

#### optimizar para obtener secciones y proyeccones automaticas

a = random.randint(int(width/5), int(2*width/5))
b = random.randint(int(2*width/5), int(3*width/5))
c = random.randint(int(3*width/5), int(4*width/5))

a = img1[:, a:a+dx]
b = img1[:, b:b+dx]
c = img1[:, c:c+dx]

proya = [sum(i) for i in a]
compareA = max(proya)
proya = compareA - proya

proyb = [sum(i) for i in b]
compareB = max(proyb)
proyb = compareB - proyb

proyc = [sum(i) for i in c]
compareC = max(proyc)
proyc = compareC - proyc

tProyA = np.zeros(len(proya))
tProyB = np.zeros(len(proyb))
tProyC = np.zeros(len(proyc))

inStaffA = False
countA = 0

inStaffB = False
countB = 0

inStaffC = False
countC = 0

for pixel in range(len(proya)):
	if inStaffA:
		if proya[pixel] < compareA*0.98:
			inStaffA = False
			if countA >= n1 and countA <= n2:
				middleA = round(countA/2)
				tProyA[pixel - middleA] = 1
			countA = 0
		countA+=1

	else:
		if proya[pixel] > compareA*0.98:
			inStaffA = True
			countA+=1

for pixel in range(len(proyb)):
	if inStaffB:
		if proyb[pixel] < compareB*0.98:
			inStaffB = False
			if countB >= n1 and countB <= n2:
				middleB = round(countB/2)
				tProyB[pixel - middleB] = 1
			countB = 0
		countB+=1

	else:
		if proyb[pixel] > compareB*0.98:
			inStaffB = True
			countB+=1

for pixel in range(len(proyc)):
	if inStaffC:
		if proyc[pixel] < compareC*0.98:
			inStaffC = False
			if countC >= n1 and countC <= n2:
				middleC = round(countC/2)
				tProyC[pixel - middleC] = 1
			countC = 0
		countC+=1

	else:
		if proyc[pixel] > compareC*0.98:
			inStaffC = True
			countC+=1

alpha = d1
beta = int(round(d2 + 2*(n2-(n2-n1)/2)))
I = int(round((5*n2 + 4*d2)*1.2))

def pentSearch(tProyA, I, alpha, beta, pentagramas):
	A = 0
	while A < tProyA.size:
		if tProyA[A] == 1:
			first = A
			system = True
			staffs = 1
			lastSpot = A
			for t in range(first+1,first+I):
				if tProyA[t] == 1.0:
					distance = t - lastSpot
					lastSpot = t
					if distance > alpha and distance < beta:
						staffs +=1
					else:
						system = False
			if staffs == 5 and system:
				pentagramas.append((first,lastSpot))		
		A+=1
	return pentagramas

def intersectingIntervals(a, b):
	if (a[0] <= b[0] and a[1] >= b[0]) or (a[0] <= b[1] and a[1] >= b[1]):
		return False
	else:
		return True



x=pentSearch(tProyA, I, alpha, beta, [])
y=pentSearch(tProyB, I, alpha, beta, x)
z=pentSearch(tProyC, I, alpha, beta, y)

final = list()
for tup in z:
	if len(final) == 0:
		final.append(tup)
	else:
		flag = True
		for tup2 in final:
			if not intersectingIntervals(tup2, tup):
				flag = False
		if flag:
			final.append(tup)

#Cutting the systems in files with name upper-lower

imgCount = 0

for tup in final:
	countUP = 0
	countDOWN = 0
	#cheking for blankspace above the system
	flag = True
	a = tup[0]
	while flag:
		if sum(img1[a]) > 255*width*0.98:
			flag = False
		a-=1
		countUP+=1
	#cheking for blankspace below the system
	flag = True
	b = tup[1]
	while flag:
		if sum(img1[b]) > 255*width*0.98:
			flag = False
		b+=1
		countDOWN+=1
	cv2.imwrite('./system/'+str(imgCount)+"-"+str(countUP)+".png", img1[tup[0]-countUP:tup[1]+countDOWN,:]) 
	imgCount+=1
