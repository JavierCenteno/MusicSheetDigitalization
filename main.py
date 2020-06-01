# -*- coding: utf-8 -*-
"""
Método principal del programa.

@author: Javier Centeno Vega
"""

path = 'example_5.png'

import pre
pre.umbralize(path, 1)

import nivel0
images = nivel0.nivel0(path)

import post0
for name in images: 
	post0.post0(name)

import nivel1
nivel1.nivel1()
