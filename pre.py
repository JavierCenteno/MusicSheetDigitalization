# -*- coding: utf-8 -*-
"""
Preprocesamiento.

@author: Gonzalo Andrés Oberreuter Álvarez
@author: Javier Centeno Vega
"""

import cv2

"""
Lee una imagen en ./input/, la umbraliza y la guarda en ./output/
"""
def umbralize(path):
	pre = cv2.imread('./input/' + path, cv2.IMREAD_GRAYSCALE)
	ret, pre = cv2.threshold(pre, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	cv2.imwrite('./output/' + path, pre)

path = 'example_3.png'

umbralize(path)
