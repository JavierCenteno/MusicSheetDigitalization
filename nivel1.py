# -*- coding: utf-8 -*-
"""
Nivel 1.

Este archivo contiene los métodos para el nivel 1 de la segmentación dedicados a segmentar los pentagramas en símbolos.

@author: Javier Centeno Vega
"""

import cv2

"""
Lee una imagen en ./nivel0/, aplica el nivel 1 y guarda los resultados ./nivel1/
"""
def nivel1(path):
	image = cv2.imread('./nivel0/' + path, 0)
