from pdf2image import convert_from_path
import time
import cv2

ts = time.time()

#Conversion de pdf a imagen, resultados se guardan en output

pages = convert_from_path('1.pdf', 500, single_file=True)
count = 0
for page in pages:
	if count == 0:
		page.save('./output/'+str(count)+'.jpg', 'JPEG')
		count+=1
ts = time.time() - ts

print(round(ts))

#Umbralizacion de los resultados

for page in range(count):
	pre = cv2.imread('./output/'+str(page)+'.jpg', cv2.IMREAD_GRAYSCALE)
	ret,pre = cv2.threshold(pre,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	
	cv2.imwrite('./output/'+str(page)+'new.jpg', th)


#print("Se convirtieron "+str(count)+" paginas en "+str(end)+" segundos." )