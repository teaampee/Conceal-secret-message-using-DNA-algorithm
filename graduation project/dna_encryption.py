# importing pillow to load images and numpy for array handling 
from PIL import Image as im
import numpy as np

#transform the output of the bin() function into an 8 bit string for example:
# bin(3) = 0b11 makes that into 00000011 
# to prepare it for handling the DNA encryption function()
def eightbitbinary(x):
    temp = bin(x)
    s = temp[2:]
    for i in range(0,10-len(temp)):
        s = "0" + s
    return s
# transforms the 8 bits binary number into DNA encryption string
# where (00 = a,01 = t,10 = g,11 = c ),, so for example:
# 00000011 => 00,00,00,11 => a,a,a,c => aaac
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
# transorm the DNA string back into an integer
def dna2int(x):
    num = ""
    for i in range(4):
        if x[i]  == "a" :
            num = num + "00"
        elif x[i]  == "t" :
            num = num + "01"
        elif x[i]  == "g" :
            num = num + "10"
        elif x[i] == "c" :
            num = num + "11"
        else:
            num = num + "10"
    
    return int(num,2)

# function to implement the compliment the DNA nitrogenous bases as in their natural habit to bond in a specific pairs A-T, G-C.. for example if we get an A we swap it with a T
def dna_complement(x):
    temp = ""
    for element in x:
        if element == "a":
            temp += "t"
        elif element == "t":
            temp += "a"
        elif element == "c":
            temp += "g"
        elif element == "g":
            temp += "c"
        else: 
            temp += element
        
    return temp
    


# encrypts the image using the DNA function()
# creates a new array that is double the size of the original image
# goes through the pixels gets their RGB values 
# transform the values of the RGB into a 4 letter string using the dna encryption function()
# for example 3 = aaac
# for every letter in the string it we get its numeric value in ASCII using ord()
# and we put these 4 numbers as seperate value for RGB in 4 neighboring pixels in the new array

def image_encrypt(im):
    temp = np.zeros((im.shape[0]*2,im.shape[1]*2,im.shape[2]),np.uint8)
    for i in range(0,im.shape[0]):
        for j in range(0,im.shape[1]):
            temprgb = im[i,j]
            r = temprgb[0]
            r = eightbitbinary(r)
            r = bits2dna(r)
            r = dna_complement(r)
            g = temprgb[1]
            g = eightbitbinary(g)
            g = bits2dna(g)
            g = dna_complement(g)
            b = temprgb[2]  
            b = eightbitbinary(b)
            b = bits2dna(b)
            b = dna_complement(b)
            temp[i*2,j*2]= (ord(r[0]),ord(g[0]),ord(b[0]))
            temp[i*2+1,j*2]= (ord(r[1]),ord(g[1]),ord(b[1]))
            temp[i*2,j*2+1]= (ord(r[2]),ord(g[2]),ord(b[2]))
            temp[i*2+1,j*2+1]= (ord(r[3]),ord(g[3]),ord(b[3]))

    return temp
# decrypts the encrypted image
# by getting the values of the RGB in the 4 neighboring pixels
# transform them back into letters
# adds them back into a string 
# then transform them back into integers using the dna2int() function
def image_decrypt(im):
    temp = np.zeros((int(im.shape[0]/2),int(im.shape[1]/2),im.shape[2]),np.uint8)
    for i in range(0,im.shape[0],2):
        for j in range(0,im.shape[1],2):
            r = ""
            r = r + chr(im[i,j,0])         
            r = r + chr(im[i+1,j,0])
            r = r + chr(im[i,j+1,0])
            r = r + chr(im[i+1,j+1,0])
            r = dna_complement(r)
            g = ""
            g = g + chr(im[i,j,1]) 
            g = g + chr(im[i+1,j,1])
            g = g + chr(im[i,j+1,1])
            g = g + chr(im[i+1,j+1,1])
            g = dna_complement(g)
            b = ""
            b = b + chr(im[i,j,2])
            b = b + chr(im[i+1,j,2])
            b = b + chr(im[i,j+1,2])
            b = b + chr(im[i+1,j+1,2]) 
            b = dna_complement(b)
            r = dna2int(r)
            g = dna2int(g)
            b = dna2int(b)
            temp[int(i/2),int(j/2)] = (r,g,b)
    return temp


        

    
        
    



    
                        
            
# cipher = encrypt("ball","monarchy")
# decrypt(cipher,"monarchy")

# im1 = im.open("grad_project\graduation project\coolit.jpeg")
# p1 = np.asarray(im1) 
# test = image_encrypt(p1)
# # test,list1 = merge(test,cipher)
# im2 = im.fromarray(test, mode="RGB")
# im2.save("encrypted_img.png")


# im3 = im.open("encrypted_img.png")
# p2 = np.asarray(im3)
# p2 = p2.copy()
# # p2,text = unmerge(p2,list1)
# test = image_decrypt(p2)
# # text = decrypt(text,"monarchy")
# # print(text)
# im4 = im.fromarray(test, mode="RGB")
# im4.save("decryption_final.png")
