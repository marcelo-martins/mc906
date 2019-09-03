from PIL import Image
from PIL import ImageOps
import sys
import random
import numpy as np
from copy import deepcopy
import time

arquivo = open("arquivo.txt", "w")
arquivo.close()

class Person:
	def __init__(self, goal, array, score, mutation):
		self.goal = goal
		self.array = array
		self.mutation = mutation

		if (score<0):
			score = 0
			for i in range(len(array)):
				for j in range(len(array[0])):
					goalPixel = goal[i,j]
					pixel = array[i,j]
					R = abs(goalPixel[0]-pixel[0])**2
					G = abs(goalPixel[1]-pixel[1])**2
					B = abs(goalPixel[2]-pixel[2])**2
					score += (R+G+B)
		self.score = score

	def mutate(self):

		Npixels = len(self.array)*len(self.array[0])
		Npixels = int(Npixels*self.mutation)

		for i in range(Npixels):
			#chooses random pixel
			pix_i = random.randint(0,len(self.array)-1)
			pix_j = random.randint(0,len(self.array[0])-1)

			#calculates the score of that pixel
			pixel = self.array[pix_i,pix_j]
			goalPixel = self.goal[pix_i,pix_j]
			R = abs(goalPixel[0]-pixel[0])**2
			G = abs(goalPixel[1]-pixel[1])**2
			B = abs(goalPixel[2]-pixel[2])**2
			pixelScore = (R+G+B)

			#generates new pixel
			color = random.randint(0,2)
			rand_value = random.randint(0,255)
			if (color==0):
				new_pixel=(rand_value,pixel[1],pixel[2],255)
			elif(color==1):
				new_pixel=(pixel[0],rand_value,pixel[2],255)
			else:
				new_pixel=(pixel[0],pixel[1],rand_value,255)

			#calculates the new pixel score
			R = abs(goalPixel[0]-new_pixel[0])**2
			G = abs(goalPixel[1]-new_pixel[1])**2
			B = abs(goalPixel[2]-new_pixel[2])**2
			newPixelScore = (R+G+B)

			#updates score
			self.score-=pixelScore
			self.score+=newPixelScore

			#updates image
			self.array[pix_i,pix_j] = new_pixel


img_src = sys.argv[1]
population = sys.argv[2]
mutationRate = sys.argv[3]

img = Image.open(img_src)
img = img.convert("RGBA")
goal = img.load()

inicio = time.time()


population = int(population)
popList = list()
for popIter in range(population):

	matrix = []
	for i in range (img.size[0]):
		line = []
		for j in range(img.size[1]):
			#pixel = (random.randint(0,255),random.randint(0,255),random.randint(0,255),255)
			pixel = (0,0,0,255)
			line.append(pixel)
		matrix.append(line)
	array = np.array(matrix,dtype=np.uint8)
	pessoa = Person(goal,array,-1,float(mutationRate))
	popList.append(pessoa)


lim = 1
for nIter in range(5000000):
	newList = list()
	for i in range(population):
		person = popList[i]
		newList.append(person)
		newPerson = Person(person.goal,deepcopy(person.array),person.score,person.mutation)
		newPerson.mutate()
		newList.append(newPerson)

	newList.sort(key=lambda x:x.score,reverse=False)
	popList = list()
	for i in range(population):
		popList.append(newList[i])

	gerList = [1,100,10000,30000,50000,80000,110000,150000,200000,250000,300000,400000,500000,600000,700000,800000,900000,1000000,1300000,1600000,1900000,2200000,2500000,3000000,4000000,5000000]
	if (not(nIter not in gerList)):
		print(nIter)
		media = 0
		for j in range(population):
			media+=popList[j].score
		media = media/population

		arquivo = open("arquivo.txt", "a")
		print("Best: " + str(popList[0].score))
		arquivo.write("Best: " + str(popList[0].score) + "\n")
		print("Mean: " + str(media))
		arquivo.write("Mean: " + str(media) + "\n")
		print("Worst: " + str(popList[population-1].score))
		arquivo.write("Worst: " + str(popList[population-1].score) + "\n")
		print("Time: " + str(time.time()- inicio))
		arquivo.write("Time: " + str(time.time()- inicio) + "\n")
		print("")
		arquivo.write("\n")
		arquivo.close()
		lim*=10
		imagem = Image.fromarray(popList[0].array)
		im = ImageOps.mirror(imagem.rotate(-90))
		im.save("geracao" + str(nIter),"png")



print(popList[0].score)
imagem = Image.fromarray(popList[0].array)
im = ImageOps.mirror(imagem.rotate(-90))
im.save("out","png")
im.show()
