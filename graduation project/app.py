from PIL import Image as im
import numpy as np
def eightbitbinary(x):
    temp = bin(x)
    s = temp[2:]
    for i in range(0,10-len(temp)):
        s = "0" + s
    return s
def bits2dna(x):
    dna=""
    for i in range(0,8,2):
        if x[i] + x[i+1] == "00" :
            dna += "a"
        elif x[i] + x[i+1] == "01" :
            dna += "t"
        elif x[i] + x[i+1] == "10" :
            dna += "g"
        else :
            dna += "c"
    
    return dna
def dna2int(x):
    num = ""
    for i in range(4):
        if x[i]  == "a" :
            num = num + "00"
        elif x[i]  == "t" :
            num = num + "01"
        elif x[i]  == "g" :
            num = num + "10"
        else :
            num = num + "11"
    
    return int(num,2)

def image_encrypt(im):
    temp = np.zeros((im.shape[0]*2,im.shape[1]*2,im.shape[2]),np.uint8)
    for i in range(0,im.shape[0]):
        for j in range(0,im.shape[1]):
            temprgb = im[i,j]
            r = temprgb[0]
            r = eightbitbinary(r)
            r = bits2dna(r)
            g = temprgb[1]
            g = eightbitbinary(g)
            g = bits2dna(g)
            b = temprgb[2]  
            b = eightbitbinary(b)
            b = bits2dna(b)
            # print(r)
            temp[i*2,j*2]= (ord(r[0]),ord(g[0]),ord(b[0]))
            temp[i*2+1,j*2]= (ord(r[1]),ord(g[1]),ord(b[1]))
            temp[i*2,j*2+1]= (ord(r[2]),ord(g[2]),ord(b[2]))
            temp[i*2+1,j*2+1]= (ord(r[3]),ord(g[3]),ord(b[3]))

            # print(temp[i*2,j*2])
            # print(temp[i*2+1,j*2])
            # print(temp[i*2,j*2+1])
            # print(temp[i*2+1,j*2+1])
    return temp
def image_decrypt(im):
    # temp = np.zeros((im.shape[0]/2,im.shape[1]/2,im.shape[2]),np.uint8)
    for i in range(0,im.shape[0],2):
        for j in range(0,im.shape[1],2):
            r = ""
            t_i = i/2
            t_j = j/2
            s = im[i,j]
            print(s[0])
            # r = r + chr(im[i/2+1,j/2,0])
            # r = r + chr(im[i/2,j/2+1,0])
            # r = r + chr(im[i/2+1,j/2+1,0])
            # # g = ""
            # g = g + chr(im[i/2,j/2,1])
            # g = g + chr(im[i/2+1,j/2,1])
            # g = g + chr(im[i/2,j/2+1,1])
            # g = g + chr(im[i/2+1,j/2+1,1])
            # b = ""
            # b = b + chr(im[i/2,j/2,2])
            # b = b + chr(im[i/2+1,j/2,2])
            # b = b + chr(im[i/2,j/2+1,2])
            # b = b + chr(im[i/2+1,j/2+1,2])
           
            
            
    return temp

                        
            


im1 = im.open('/home/ismail0w249/grad_project/graduation project/coolit.jpeg')
p1 = np.asarray(im1) 

# print(p1.shape[0] , p1.shape[1] , p1.shape[2])

test = image_encrypt(p1)
im2 = im.fromarray(test, mode="RGB")
im2.save("siuu.png")
im3 = im.open("siuu.png")
p2 = np.asarray(im3)
# test = image_decrypt(p2)

# print(im2.getpixel((4,4)))
# print(test.shape[0] , test.shape[1] , test.shape[2])
# print(p1[4,4])
# # print(test[4,4])
# test[4,4] = p1[4,4]
# # print(test[4,4])
        

# ax = test[4,4]
# g = eightbitbinary(ax[0])
# g = bits2dna(g)
# print(g)




# # Base 2(binary)
# bin_a = eightbitbinary(ax[1])
# print(bin_a)
# print(int(bin_a, 2)) 

######################binary to dna test###################
# x = 99
# x = eightbitbinary(x)
# print(x)
# x = bits2dna(x)
# print(x)
# x = dna2int(x)
# print(x)
##########################################################
# --------------------------------------
# Creates an image memory from an object exporting the array interface (using the buffer protocol).

# If obj is not contiguous, then the tobytes method is called and frombuffer() is used.

# If you have an image in NumPy:

# from PIL import Image
# import numpy as np
# im = Image.open("hopper.jpg")
# a = np.asarray(im)
# Then this can be used to convert it to a Pillow image:

# im = Image.fromarray(a)
# PARAMETERS:
# obj – Object with array interface

# mode –

# Optional mode to use when reading obj. Will be determined from type if None.

# This will not be used to convert the data after reading, but will be used to change how the data is read: