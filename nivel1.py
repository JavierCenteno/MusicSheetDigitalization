# -*- coding: utf-8 -*-
"""
Nivel 1.

Este archivo contiene los métodos para el nivel 1 de la segmentación dedicados a segmentar los pentagramas en símbolos.

@author: Javier Centeno Vega
"""

import cv2
import nivel0

"""
Lee una imagen en ./nivel0/, aplica el nivel 1 y guarda los resultados ./nivel1/
"""
def nivel1_deteccion_de_notas(path):
	image = cv2.imread('./nivel0/' + path, 0)
	image_transposed = cv2.transpose(image)

	minimumNoteHeadHeight = 2 * nivel0.n2
	maximumNoteHeadHeight = 2 * nivel0.n2 + 2 * nivel0.d1
	
	# Mapea el índice de las columnas al índice del píxel donde empieza una nota
	note_starters = dict()
	# Mapea el índice de las columnas al índice del píxel donde termina una nota
	note_enders = dict()
	# Mapea el índice de las columnas al ancho de la nota
	note_ranges = dict()
	
	window_width = 5
	
	for col in range(len(image_transposed) - window_width):
		y_proyection = dict()
		y_proyection[-1] = 0
		y_proyection[len(image)] = 0
		
		for row in range(len(image)):
			y_proyection[row] = 0
			for window_col in range(window_width):
				if image_transposed[col + window_col][row] == 0:
					y_proyection[row] += 1
		
		# Índices donde empiezan los tramos de píxeles negros
		black_stretch_starters = []
		# Índices donde terminan los tramos de píxeles negros
		black_stretch_enders = []
		
		for row in range(len(image) + 1):
			if y_proyection[row] == 0 and y_proyection[row - 1] > 0:
				black_stretch_enders.append(row)
			elif y_proyection[row] > 0 and y_proyection[row - 1] == 0:
				black_stretch_starters.append(row)
		
		# Tamaños de los tramos de píxeles negros
		black_stretch_sizes = []
		for index in range(len(black_stretch_starters)):
			black_stretch_sizes.append(black_stretch_enders[index] - black_stretch_starters[index])
		
		potential_black_stretch_starters = []
		potential_black_stretch_enders = []
		potential_black_stretch_sizes = []
		for index in range(len(black_stretch_sizes)):
			if minimumNoteHeadHeight < black_stretch_sizes[index] and black_stretch_sizes[index] < maximumNoteHeadHeight:
				potential_black_stretch_starters.append(black_stretch_starters[index])
				potential_black_stretch_enders.append(black_stretch_enders[index])
				potential_black_stretch_sizes.append(black_stretch_sizes[index])
		
		if len(potential_black_stretch_sizes) != 0:
			note_index = potential_black_stretch_sizes.index(max(potential_black_stretch_sizes))
			note_starter = potential_black_stretch_starters[note_index]
			note_ender = potential_black_stretch_enders[note_index]
			note_range = potential_black_stretch_sizes[note_index]
			
			note_starters[col] = note_starter
			note_enders[col] = note_ender
			note_ranges[col] = note_range
	
	# Nos saltamos lo de los thresholds
	# Ya estamos asumiendo que una nota tiene tal ancho y es negrita
	# Con la búsqueda de notas por altura debería darnos para encontrar las notas
	# Además, la diferencia en números de beams puede provocar que no haya un
	# umbral que separe las notas de los beams a lo largo de todas las notas

"""
Lee una imagen en ./nivel0/, aplica el nivel 1 y guarda los resultados ./nivel1/
"""
def nivel1(path):
	image = cv2.imread('./nivel0/' + path, 0)
	sliced_images = []
	blur_distance = nivel0.d2 * 2
	minimum_slice_width = nivel0.d1
	print("Minimum slice width: {}".format(minimum_slice_width))
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
		print("Minimum: {} Maximum: {} No issue".format(__minimum_x, __maximum_x))
		__slice_local_minima = []
		for __index in range(__minimum_x, __maximum_x):
			if __index in local_minima:
				__slice_local_minima.append(__index)
		__slice_local_minima.sort(key = lambda x : x_proyection[x])
		for __slice_local_minimum in __slice_local_minima:
			if (__slice_local_minimum - __minimum_x) > minimum_slice_width and (__maximum_x - __slice_local_minimum) > minimum_slice_width:
				slice_image(__minimum_x, __slice_local_minimum)
				slice_image(__slice_local_minimum + 1, __maximum_x)
				return
		# If no local minimum can slice the image in two pieces wider than minimum_slice_width
		sliced_images.append(image[:, __minimum_x:__maximum_x])
	
	slice_image(0, width)
	for sliced_image in sliced_images:
		print(len(sliced_image))
