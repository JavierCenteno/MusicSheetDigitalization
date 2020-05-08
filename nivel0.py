# -*- coding: utf-8 -*-
"""
Nivel 0.

Este archivo contiene los métodos para el nivel 0 de la segmentación dedicados a segmentar la imagen en pentagramas.

@author: Gonzalo Andrés Oberreuter Álvarez
@author: Javier Centeno Vega
"""

import cv2
import numpy as np
import random

#### Optimizar para obtener secciones y proyeccones automaticas

#### Algoritmo
#### buscar un area de y*dx random dentro del "centro"de la partitura
#### buscar su proyeccion horizontal e invertirla segun el maximo cosa que la cantidad de negro sean picos en el histograma
#### formar la Tproyeccion
#### se buscan los pentagramas y se agregan a la lista de tuplas.
#### Se detiene el proceso cuando no se encuentran mas pentagramas en 3 iteraciones
def stave_search(t_proy_a, I, alpha, beta, staves):
	A = 0
	while A < t_proy_a.size:
		if t_proy_a[A] == 1:
			first = A
			system = True
			staffs = 1
			lastSpot = A
			for t in range(first + 1, first + I):
				if t_proy_a[t] == 1.0:
					distance = t - lastSpot
					lastSpot = t
					if distance > alpha and distance < beta:
						staffs +=1
					else:
						system = False
			if staffs == 5 and system:
				staves.append((first,lastSpot))		
		A += 1
	return staves

def intersecting_intervals(a, b):
	if (a[0] <= b[0] and a[1] >= b[0]) or (a[0] <= b[1] and a[1] >= b[1]):
		return False
	else:
		return True

def biggest_conected_area(image, id, beggin):
    image = image.astype('uint8')
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(image, connectivity=4)
    sizes = stats[:, -1]

    max_label = 1
    max_size = sizes[1]
    for i in range(2, nb_components):
        if sizes[i] > max_size:
            max_label = i
            max_size = sizes[i]

    image_2 = np.zeros(output.shape)
    image_2[output == max_label] = 255
    cv2.imwrite('./nivel0/' + str(id) + '-' + str(beggin) + '.png', 255 - image_2)
    return

"""
Lee una imagen en ./pre/, aplica el nivel 0 y guarda los resultados ./nivel0/
"""
def nivel0(path):
	image = cv2.imread('./pre/' + path, 0)
	image_transposed = cv2.transpose(image);
	
	histogram_black = dict()
	histogram_white = dict()
	
	# Se cuentan las ocurrencias de secuencias de pixeles blancos y negros en un quinto de las columnas de la imagen
	for col in range(0, len(image_transposed), 5):
		count = 0
		flag = True
		if image_transposed[col][0] == 0:
				flag = False
		for pixel in range(len(image_transposed[col])):
			if flag:
				if image_transposed[col][pixel] == 255:
					count += 1
				elif pixel == len(image_transposed[col]) - 1:
					if count not in histogram_white:
						histogram_white[count] = 0
					histogram_white[count] += 1
				else:
					if count not in histogram_white:
						histogram_white[count] = 0
					histogram_white[count] += 1
					count = 0
					flag = False
			else:
				if image_transposed[col][pixel] == 0:
					count += 1
				elif pixel == len(image_transposed[col]) - 1:
					if count not in histogram_black:
						histogram_black[count] = 0
					histogram_black[count] += 1
				else:
					if count not in histogram_black:
						histogram_black[count] = 0
					histogram_black[count] += 1
					count = 0
					flag = True
	
	# Se obtienen los valores n1, n2, d1, d2
	
	n = list()
	d = list()
	
	N = max(list(histogram_black.values())) / 3.0
	D = max(list(histogram_white.values())) / 3.0
	
	for dist in histogram_black:
		if histogram_black[dist] > N:
			n.append(dist)
	
	for dist in histogram_white:
		if histogram_white[dist] > D:
			d.append(dist)
	
	n1 = min(n)
	n2 = max(n)
	d1 = min(d)
	d2 = max(d)
	
	print(n1, n2, d1, d2)
	
	width = len(image[0])
	
	dx = int(width / 60)
	
	final = list()
	past_len = len(final)
	iterations_without_change = 0
	
	while True:
		sec = random.randint(2, 5)
		# Buscar alguna columna de la imagen
		a = random.randint(int(sec * width / 7), int((sec + 1) * width / 7))
		a = image[:, a : a + dx]
		proy_a = [sum(i) for i in a]
		compare_a = max(proy_a)
		proy_a = compare_a - proy_a
		t_proy_a = np.zeros(len(proy_a))
		in_staff_a = False
		count_a = 0
		for pixel in range(len(proy_a)):
			if in_staff_a:
				if proy_a[pixel] < compare_a * 0.98:
					in_staff_a = False
					if count_a >= n1 and count_a <= n2:
						middle_a = round(count_a / 2)
						t_proy_a[pixel - middle_a] = 1
					count_a = 0
				count_a += 1
	
			else:
				if proy_a[pixel] > compare_a*0.98:
					in_staff_a = True
					count_a += 1
		alpha = d1
		beta = int(round(d2 + 2 * (n2 - (n2 - n1) / 2)))
		I = int(round((5 * n2 + 4 * d2) * 1.2))
		finded = stave_search(t_proy_a, I, alpha, beta, [])
		for tup in finded:
			if len(final) == 0:
				final.append(tup)
			else:
				flag = True
				for tup2 in final:
					if not intersecting_intervals(tup2, tup):
						flag = False
				if flag:
					final.append(tup)
		if past_len == len(final):
			iterations_without_change += 1
			if iterations_without_change == 3:
				break
		past_len = len(final)
	
	# Cutting the systems in files with name upper-lower
	
	image_count = 0
	
	for tup in final:
		sub = 255 - image[tup[0] - int(I / 2) : tup[1] + int(I / 2), :]
		biggest_conected_area(sub, image_count, int(I / 2))
		image_count += 1
