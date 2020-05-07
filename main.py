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

#### Algoritmo
#### buscar un area de y*dx random dentro del "centro"de la partitura
#### buscar su proyeccion horizontal e invertirla segun el maximo cosa que la cantidad de negro sean picos en el histograma
#### formar la Tproyeccion
#### se buscan los pentagramas y se agregan a la lista de tuplas.
#### Se detiene el proceso cuando no se encuentran mas pentagramas en 3 iteraciones
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

def biggestConectedArea(image, id, beggin):
    image = image.astype('uint8')
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(image, connectivity=4)
    sizes = stats[:, -1]

    max_label = 1
    max_size = sizes[1]
    for i in range(2, nb_components):
        if sizes[i] > max_size:
            max_label = i
            max_size = sizes[i]

    img2 = np.zeros(output.shape)
    img2[output == max_label] = 255
    cv2.imwrite("./staves/"+str(id)+"-"+str(beggin)+".png", 255 -img2)
    return

final = list()
pastLen = len(final)
Flag = True
noChange = 0

while Flag:
	a = random.randint(int(width/5), int(2*width/5))  ## Buscar alguna columna de la imagen
	a = img1[:, a:a+dx]
	proya = [sum(i) for i in a]
	compareA = max(proya)
	proya = compareA - proya
	tProyA = np.zeros(len(proya))
	inStaffA = False
	countA = 0
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
	alpha = d1
	beta = int(round(d2 + 2*(n2-(n2-n1)/2)))
	I = int(round((5*n2 + 4*d2)*1.2))
	finded = pentSearch(tProyA, I, alpha, beta, [])
	for tup in finded:
		if len(final) == 0:
			final.append(tup)
		else:
			flag = True
			for tup2 in final:
				if not intersectingIntervals(tup2, tup):
					flag = False
			if flag:
				final.append(tup)
	if pastLen == len(final):
		noChange+=1
		if noChange == 3:
			Flag = False
	pastLen = len(final)


#Cutting the systems in files with name upper-lower

imgCount = 0

for tup in final:
	sub = 255 - img1[tup[0]-int(I/2):tup[1]+int(I/2), :]
	biggestConectedArea(sub, imgCount, int(I/2))
	imgCount+=1
