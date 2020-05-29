import cv2
import numpy as np

def post0(path):
	imwr = cv2.imread('./nivel0/' + path, 0)
	imwr = 255 - imwr
	output = cv2.connectedComponentsWithStatsWithAlgorithm(imwr, 4, ltype=cv2.CV_16U, ccltype=cv2.CCL_DEFAULT)
	num_labels = output[0]
	labels = output[1]
	stats = output[2]
	centroids = output[3]

	length = len(imwr)
	height = len(imwr[0])
	area = length*height
	dispose = list()
	#Se recorren borde superior e inferior
	for num in range(length):
		if labels[num,0] != 0:
			if stats[labels[num,0],cv2.CC_STAT_AREA] < area*0.1:
				dispose.append(labels[num,0])
		elif labels[num,height-1] != 0:
			if stats[labels[num,height-1],cv2.CC_STAT_AREA] < area*0.1:
				dispose.append(labels[num,height-1])

	for num in range(height):
		if labels[0,num] != 0:
			if stats[labels[0,num],cv2.CC_STAT_AREA] < area*0.1:
				dispose.append(labels[0,num])
		elif labels[length-1,num] != 0:
			if stats[labels[length-1,num],cv2.CC_STAT_AREA] < area*0.1:
				dispose.append(labels[length-1,num])

	dispose = set(dispose)
	tmp = imwr
	print(dispose)
	for v in range(length):
		for b in range(height):
			if labels[v,b] in dispose:
				tmp[v,b] = 0
	tmp = 255 - tmp
	cv2.imshow("image",tmp)
	cv2.waitKey(0)

	# sizes = stats[:, -1]
	# max_label = 1
	# max_size = sizes[1]
	# for i in range(2, num_labels):
	# 	if sizes[i] > max_size:
	# 		max_label = i
	# 		max_size = sizes[i]
	# img2 = np.zeros(labels.shape, dtype=np.uint8)
	# img2[labels == max_label] = 255 
