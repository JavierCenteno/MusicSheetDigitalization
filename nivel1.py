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
def nivel1(path):
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
	
	for col in range(len(image_transposed)):
		# Índices donde empiezan los tramos de píxeles negros
		black_stretch_starters = []
		# Índices donde terminan los tramos de píxeles negros
		black_stretch_enders = []
		last_pixel = 255
		for row in range(len(image)):
			if image_transposed[col][row] == 255:
				if last_pixel == 0:
					last_pixel = 255
					black_stretch_enders.append(row)
			elif image_transposed[col][row] == 0:
				if last_pixel == 255:
					last_pixel = 0
					black_stretch_starters.append(row)
		if len(black_stretch_enders) < len(black_stretch_starters):
			# Si falta algún finalizador (porque el último píxel es negro)
			# Añadir a la lista de finalizadores
			black_stretch_enders.append(len(image) - 1)
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
	
	# Bueno, valdría la pena revisitar lo de los thresholds, el algoritmo por ahora
	# detecta demasiadas cosas
	# ¿Valdría la pena ampliar la ventana en vez de usar una sola columna?
