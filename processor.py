from PIL import Image
import numpy
import time

def wrapper(data , check):		
	counter = 0
	temp = []
	buffer = [] # this will store the entire result
	for item in data:
		temp.append(item)
		counter = counter + 1
		if (counter %  check == 0):
			buffer.append(temp)
			temp = []
			counter = 0
	return buffer

def tranpose(buffer):
	result = []
	for i in range(len(buffer[0])):
		temp = []
		for j in range(len(buffer)):
			temp.append(buffer[j][i])
		result.append(temp)
	return result

def inverter(p): 
	buffer = []
	for row in p:
		temp = []
		for triplet in row:
			temp.append((abs(triplet[0]-255), abs(triplet[1] - 255) , abs(triplet[2] - 255)))
		buffer.append(temp)		
	return (buffer)

def linearInterpolation(p):
	buffer = []
	for i in range(len(p)):
		newData = []
		for j in range(len(p[i])):	
			try:
				tempR =  (p[i][j][0] + p[i][j+1][0]) // 2
				tempG =  (p[i][j][1] + p[i][j+1][1]) // 2
				tempB =  (p[i][j][2] + p[i][j+1][2]) // 2

				interpolatedData = (tempR , tempG  , tempB)

				newData.append(p[i][j])
				newData.append(interpolatedData)
	
			except:
				
				newData.append(p[i][j])
	
		
		buffer.append(newData)
	
	newBuffer = []
	for i in range(len(buffer[0])):
		newData = []
		for j in range(len(buffer)):	
			try:
				tempR =  (buffer[j][i][0] + buffer[j][i+1][0]) // 2
				tempG =  (buffer[j][i][1] + buffer[j][i+1][1]) // 2
				tempB =  (buffer[j][i][2] + buffer[j][i+1][2]) // 2

				interpolatedData = (tempR , tempG  , tempB)

				newData.append(buffer[j][i])
				newData.append(interpolatedData)
	
			except:
				
				newData.append(buffer[j][i])
	

		newBuffer.append(newData)
	newBuffer.pop()
	
	return tranpose(newBuffer)

def blend(left , right , pivot): # this is the base blend function
	buffer = []
	for i in range (len(left)):
		temp = []
		for j in range(len(left[i])):
			first =  blendValue(left[i][j][0] , right[i][j][0] , pivot)
			second = blendValue(left[i][j][1] , right[i][j][1] , pivot)
			third =  blendValue(left[i][j][2] , right[i][j][2] , pivot)

			temp.append((first , second ,third))
		buffer.append(temp)	
	return (buffer)

			
def blendValue(left , right , pivot): # this is the helper function for the blend
	leftContribution = left * (1 - pivot)
	rightContribution = right * pivot
	newPixelData = leftContribution + rightContribution
	return newPixelData


def blackAndWhite(p): # this would be our worker function 
	buffer = []
	for row in p:
		temp = []
		
		for triplet in row:
			sum = 0
			for i in triplet:
				sum = sum + i
			result = sum // 3
			temp.append((result, result , result))
						
		buffer.append(temp)
	
		
	return (buffer)

			

price = Image.open("200x200price.jpg") # supply the file name with path here
data = wrapper(list(price.getdata()), 200)
startTime = time.time()



# ~ FUNCTIONS 
result = linearInterpolation(data) # this scales a m X n image into an 2m X 2n image using linear interpolation
# can also chain the function as such linearInterpolation(linearInterpolation(data)) to call it multiple times

#result = blackAndWhite(data) # this would turn the image into black and white
#result = inverter(data) # this would invert the image 



#Image Blender
#image1 = "nature400x400.jpg"
#image2 = "person400x400.jpg"
	
#i1 = Image.open(image1) # supply the file name with path here
#i2 = Image.open(image2) # supply the file name with path here

#data1 = wrapper(list(i1.getdata()), i1.size[0])
#data2 = wrapper(list(i2.getdata()), i2.size[0])
#pivot = float(input("Enter the pivot  value : "))
#result = blend(data1 , data2 , pivot)

# ~
resultData = numpy.array(result , dtype = numpy.uint8)
newData = Image.fromarray(resultData)
newData.show()
print("total time taken : " , time.time() - startTime)


 


