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

# Algunos de los mínimos encontrados partían símbolos por la mitad.
# Estos mínimos, al cortar símbolos por la mitad, estaban muy altos respecto a
# otros mínimos.
# Por ello, se ha decidido no escoger mínimos por encima de un cierto umbral.

# Algunos de los segmentos eran demasiado anchos, abarcando múltiples símbolos
# Por lo que se ha decidido ignorar las restricciones y trocear un segmento
# igualmente si tiene segmentos demasiado anchos.

# Algunos de los segmentos no contenían símbolos, por lo que se descartan
# segmentos cuyo rango en la proyección x esté por debajo de cierto umbral.

# Ancho de la matriz del filtro de media para emborronar la imagen
blur_distance = nivel0.d2
# Ancho mínimo que puede tener un segmento conteniendo un símbolo
minimum_slice_width = nivel0.d1
# Ancho máximo que puede tener un segmento conteniendo un símbolo
maximum_slice_width = nivel0.d2 * 4
# Solo se aceptarán los mínimos que estén por debajo del umbral
minimum_accepting_threshold = nivel0.n1 * 5 * 255 * 2
# Solo se aceptarán imágenes cuyo rango en la proyección x sea mayor que el umbral
minimum_slice_range = nivel0.n2 * 255 * 2

"""
Lee una imagen en ./nivel0/, aplica el nivel 1 y guarda los resultados ./nivel1/
"""
def nivel1_file(path):
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
				# Check the minimum is below the threshold
				# Or ignore if any of the chunks is over the maximum width
				if x_proyection[__slice_local_minimum] < minimum_accepting_threshold or (__slice_local_minimum - __minimum_x) > maximum_slice_width or (__maximum_x - __slice_local_minimum) > maximum_slice_width:
					slice_image(__minimum_x, __slice_local_minimum)
					slice_image(__slice_local_minimum + 1, __maximum_x)
					return
		# If no local minimum can slice the image in two pieces wider than minimum_slice_width
		sliced_images.append(image[:, __minimum_x:__maximum_x])
	
	slice_image(0, width)
	
	# sliced_images filtradas
	sliced_images_filtered = []
	
	# Discard images with a low range in the x projection as those images
	# are assumed to be an empty staff
	for sliced_image in sliced_images:
		sliced_image_minimum = None
		sliced_image_maximum = None
		sliced_image_height, sliced_image_width = sliced_image.shape
		for sliced_image_col in range(sliced_image_width):
			sliced_image_x_proyection = 0
			for sliced_image_row in range(sliced_image_height):
				sliced_image_x_proyection += 255 - sliced_image[sliced_image_row][sliced_image_col]
			if sliced_image_minimum == None:
				sliced_image_minimum = sliced_image_x_proyection
			elif sliced_image_x_proyection < sliced_image_minimum:
				sliced_image_minimum = sliced_image_x_proyection
			if sliced_image_maximum == None:
				sliced_image_maximum = sliced_image_x_proyection
			elif sliced_image_x_proyection > sliced_image_maximum:
				sliced_image_maximum = sliced_image_x_proyection
		sliced_image_range = sliced_image_maximum - sliced_image_minimum
		if sliced_image_range > minimum_slice_range and sliced_image_width < maximum_slice_width:
			sliced_images_filtered.append(sliced_image)
	
	sliced_images = sliced_images_filtered
	index = 0
	for sliced_image in sliced_images:
		cv2.imwrite("./nivel1/" + path + "-" + str(index) + ".png", sliced_image)
		index += 1

import os
def nivel1():
	for file in os.listdir("nivel0"):
		if file.endswith(".png"):
			file_path = os.path.join("nivel0", file)
			nivel1_file(file)
			os.remove(file_path)

nivel1()
