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

# def image_encrypt(ar):
    
#     for i in range(0,ar.shape[0],1):
#         for j in range(0,ar.shape[1],1):
            


im1 = im.open('web/graduation project/coolit.jpeg')
px = np.asarray(im1) 

print(px.shape[0] , px.shape[1] , px.shape[2])

test = np.zeros((px.shape[0]*2,px.shape[1]*2,px.shape[2]),np.uint8)

print(test.shape[0] , test.shape[1] , test.shape[2])
print(px[4,4])
print(test[4,4])
test[4,4] = px[4,4]
print(test[4,4])
        

ax = test[4,4]
g = eightbitbinary(ax[0])
print(bits2dna(g))




# Base 2(binary)
bin_a = eightbitbinary(ax[1])
print(bin_a)
print(int(bin_a, 2)) 


print("s")



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