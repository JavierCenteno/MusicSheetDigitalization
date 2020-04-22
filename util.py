# -*- coding: utf-8 -*-
"""
Métodos auxiliares usados para el desarrollo del proyecto.

@author: Gonzalo Andrés Oberreuter Álvarez
@author: Javier Centeno Vega
"""

import pdf2image
import cv2
import numpy

'''
Convierte el archivo pdf en la ubicación dada a imágenes jpg, guardando cada página como una imagen separada.
'''
def pdf_to_jpg(path):
	pages = pdf2image.convert_from_path(path, 500, single_file = True)
	count = 0
	for page in pages:
		if count == 0:
			page.save(path + '_' + str(count) + '.jpg', 'JPEG')
			count += 1

'''
Elimina todas las filas y columnas de píxeles de la imagen dada que no sean múltiplos del número dado.
'''
def shred(path, number):
	image = cv2.imread('./input/' + path)
	result = []
	for row in image[::number]:
		result_row = []
		result.append(result_row)
		for pixel in row[::number]:
			result_row.append(pixel)
	cv2.imwrite('./output/' + path, numpy.array(result))
