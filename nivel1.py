# -*- coding: utf-8 -*-
"""
Nivel 1.

Este archivo contiene los métodos para el nivel 1 de la segmentación dedicados a segmentar los pentagramas en símbolos.

@author: Javier Centeno Vega
"""

import cv2
import nivel0

# El método del artículo define un método de detección de notas y un método de
# detección de otros símbolos.
# El método de distinguir segmentos con notas de segmentos con otros símbolos
# está pobremente definido.
# Además, el método de detección de cabezas de notas parece asumir que las
# cabezas de notas son todas negras, ignorando las blancas, ya que usa el
# ancho de la proyección de la ventana para detectar las notas y el ancho de
# las notas blancas difícilmente será el mismo que el de las negras.

# El método usado está basado en el método de detección de otros símbolos.
# Este método emborrona la imagen con un filtro de media (ver parámetro
# blur_distance). Posteriormente calcula la proyección en x y encuentra los
# mínimos locales.
# En cada paso, corta la imagen en dos trozos en el mínimo local más pequeño
# que divida la imagen en dos segmentos que tengan un ancho igual o superior al
# ancho mínimo (ver parámetro minimum_slice_width).
# El método para de cortar la imagen cuando no hay mínimos locales que puedan
# dividir la imagen en dos segmentos que cumplan esta condición.

# Ancho de la matriz del filtro de media para emborronar la imagen
blur_distance = nivel0.d2
# Ancho mínimo que puede tener un segmento conteniendo un símbolo
minimum_slice_width = nivel0.d1
# Solo se aceptarán los mínimos que estén por debajo del umbral
minimum_accepting_threshold = nivel0.n1 * 5 * 255 * 2

"""
Lee una imagen en ./nivel0/, aplica el nivel 1 y guarda los resultados ./nivel1/
"""
def nivel1(path):
	image = cv2.imread('./nivel0/' + path, 0)
	sliced_images = []
	height, width = image.shape
	blurred_image = cv2.blur(image, (blur_distance, blur_distance))
	x_proyection = dict()
	for col in range(width):
		x_proyection[col] = 0
		for row in range(height):
			x_proyection[col] += 255 - blurred_image[row][col]
	# the local minima, not counting minima at the start and at the end
	local_minima = []
	for index in range(1, len(x_proyection) - 1):
		if x_proyection[index] < x_proyection[index - 1] and x_proyection[index] < x_proyection[index + 1]:
			local_minima.append(index)

	# Recursive function to slice image
	def slice_image(__minimum_x, __maximum_x):
		__slice_local_minima = []
		for __index in range(__minimum_x, __maximum_x):
			if __index in local_minima:
				__slice_local_minima.append(__index)
		__slice_local_minima.sort(key = lambda x : x_proyection[x])
		for __slice_local_minimum in __slice_local_minima:
			if (__slice_local_minimum - __minimum_x) > minimum_slice_width and (__maximum_x - __slice_local_minimum) > minimum_slice_width:
				if x_proyection[__slice_local_minimum] < minimum_accepting_threshold:
					slice_image(__minimum_x, __slice_local_minimum)
					slice_image(__slice_local_minimum + 1, __maximum_x)
					return
		# If no local minimum can slice the image in two pieces wider than minimum_slice_width
		sliced_images.append(image[:, __minimum_x:__maximum_x])
	
	slice_image(0, width)
	index = 0
	for sliced_image in sliced_images:
		cv2.imwrite("./nivel1/" + path + "-" + str(index) + ".png", sliced_image)
		index += 1
