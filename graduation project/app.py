import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk,Image
from dna_encryption import image_encrypt,image_decrypt,eightbitbinary
from playfair_cipher import encrypt,decrypt
import numpy as np
import os

# [16, 18, 21, 34, 39, 50, 60, 68, 77, 84, 90, 102, 106, 120, 135, 136] mb used later
stego_key_matrixes  =[[8,1,6,3,5,7,4,9,2],
   [16, 2, 3, 13, 5, 11, 10, 8, 9, 7, 6, 12, 4, 14, 15, 1],
   [17, 24, 1, 8, 15, 23, 5, 7, 14, 16, 4, 6, 13, 20, 22, 10, 12, 19, 21, 3, 11, 18, 25, 2, 9],
    [35, 1, 6, 26, 19, 24, 3, 32, 7, 21, 23, 25, 31, 9, 2, 22, 27, 20, 8, 28, 33, 17, 10, 15, 30, 5, 34, 12, 14, 16, 4, 36, 29, 13, 18, 11],
    [30, 39, 48, 1, 10, 19, 28, 38, 47, 7, 9, 18, 27, 29, 46, 6, 8, 17, 26, 35, 37, 5, 14, 16, 25, 34, 36, 45, 13, 15, 24, 33, 42, 44, 4, 21, 23, 32, 41, 43, 3, 12, 22, 31, 40, 49, 2, 11, 20],
    [64, 2, 3, 61, 60, 6, 7, 57, 9, 55, 54, 12, 13, 51, 50, 16, 17, 47, 46, 20, 21, 43, 42, 24, 40, 26, 27, 37, 36, 30, 31, 33, 32, 34, 35, 29, 28, 38, 39, 25, 41, 23, 22, 44, 45, 19, 18, 48, 49, 15, 14, 52, 53, 11, 10, 56, 8, 58, 59, 5, 4, 62, 63, 1],
    [47, 58, 69, 80, 1, 12, 23, 34, 45, 57, 68, 79, 9, 11, 22, 33, 44, 46, 67, 78, 8, 10, 21, 32, 43, 54, 56, 77, 7, 18, 20, 31, 42, 53, 55, 66, 6, 17, 19, 30, 41, 52, 63, 65, 76, 16, 27, 29, 40, 51, 62, 64, 75, 5, 26, 28, 39, 50, 61, 72, 74, 4, 15, 36, 38, 49, 60, 71, 73, 3, 14, 25, 37, 48, 59, 70, 81, 2, 13, 24, 35],
    [92, 99, 1, 8, 15, 67, 74, 51, 58, 40, 98, 80, 7, 14, 16, 73, 55, 57, 64, 41, 4, 81, 88, 20, 22, 54, 56, 63, 70, 47, 85, 87, 19, 21, 3, 60, 62, 69, 71, 28, 86, 93, 25, 2, 9, 61, 68, 75, 52, 34, 17, 24, 76, 83, 90, 42, 49, 26, 33, 65, 23, 5, 82, 89, 91, 48, 30, 32, 39, 66, 79, 6, 13, 95, 97, 29, 31, 38, 45, 72, 10, 12, 94, 96, 78, 35, 37, 44, 46, 53, 11, 18, 100, 77, 84, 36, 43, 50, 27, 59],
    [68, 81, 94, 107, 120, 1, 14, 27, 40, 53, 66, 80, 93, 106, 119, 11, 13, 26, 39, 52, 65, 67, 92, 105, 118, 10, 12, 25, 38, 51, 64, 77, 79, 104, 117, 9, 22, 24, 37, 50, 63, 76, 78, 91, 116, 8, 21, 23, 36, 49, 62, 75, 88, 90, 103, 7, 20, 33, 35, 48, 61, 74, 87, 89, 102, 115, 19, 32, 34, 47, 60, 73, 86, 99, 101, 114, 6, 31, 44, 46, 59, 72, 85, 98, 100, 113, 5, 18, 43, 45, 58, 71, 84, 97, 110, 112, 4, 17, 30, 55, 57, 70, 83, 96, 109, 111, 3, 16, 29, 42, 56, 69, 82, 95, 108, 121, 2, 15, 28, 41, 54]]

def merge(image,text,skey):
    skey = eightbitbinary(skey)
    skey = skey[5:8]
    skey = int(skey,2)
    print(skey)
    # using the magic(4) in matlab to create a matrix each value in that matrix determine how far is the next pixel in the merging technique
    text += "jjjjj"
    # print("dodo:",text)
    key_array =  stego_key_matrixes[skey]
    key_array_len = len(key_array)
    print(key_array_len)
    cols = image.shape[1]
    rows = image.shape[0]
    text_length = len(text)
    # section of code to test out if the image can handle the inputed text
    s = (text_length)% key_array_len
    su = 0
    for i in range(0,s):
        su += key_array[i]
    su = (int(text_length/16)*136) + su 
    if(su > (rows*cols)-1):
        print("ERROR/////: the image can't handle that many characters")
        return image
    position = 0
    # hiding the in the lower bit of the color values (8-bits) the least two bits for Red and Green, 4 least bits in the Blue color coz in reality the eye only sees the blue color about 20 times less than red and green
    # a simple for-loop for hiding the text than the same code to put the letter "j" as a stop sign for the merging technique
    for i in range (0,text_length):
        s = i% key_array_len
        position += key_array[s]
        row = int(position / cols)
        col = position % cols
        # print(i,",",position,",row:",row,",",rows,",col",col,",",cols)
        char = eightbitbinary(ord(text[i]))
        red = eightbitbinary(image[row,col,0])
        red = list(red)
        red[6:8] = char[0:2]
        red = "".join(red)
        image[row,col,0] = int(red,2)
        green = eightbitbinary(image[row,col,1])
        green = list(green)
        green[6:8] = char[2:4]
        green = "".join(green)
        image[row,col,1] = int(green,2)
        blue = eightbitbinary(image[row,col,2])
        blue = list(blue)
        blue[4:8] = char[4:8]
        blue = "".join(blue)
        image[row,col,2] = int(blue,2)
    return image

def unmerge(image,skey):
    skey = eightbitbinary(skey)
    skey = skey[5:8]
    skey = int(skey,2)
    print(skey)
    j_count = 0
    key_array = stego_key_matrixes[skey] 
    key_array_len = len(key_array)
    print(key_array_len)
    cols = image.shape[1]
    text= ""
    position = 0
    i = 0
    while True:   
        s = i% key_array_len
        position += key_array[s]
        row = int(position / cols)
        col = position % cols
        char = ""
        temp = eightbitbinary(image[row,col,0])
        char += temp[6:8]
        temp = eightbitbinary(image[row,col,1])
        char += temp[6:8]
        temp = eightbitbinary(image[row,col,2])
        char += temp[4:8]
        char = int(char,2)
        char = chr(char)
        if(char == "j"):
            j_count += 1
            i += 1
            continue
        if(j_count == 5):
            return image,text
        j_count = 0
        text += char
        i += 1
    


def select_file():
    root.filename = filedialog.askopenfilename(initialdir=os.path.dirname(__file__),title="select an image to encrypt")
    return root.filename
def btn_encrypt(mode):
    top = tk.Toplevel()
    global im1,im2,im1_label,im2_label,im4_label
    # encryption::::::::::::::::::::::::::::::::::::::::::::::::::
    loc = select_file()
    im1_label = Image.open(loc)
    im1_label = im1_label.resize((400,300))
    im1_label = ImageTk.PhotoImage(im1_label)
    label2 = tk.Label(top,image=im1_label).grid(column=0,row=1)
    label = tk.Label(top,text="original Image :").grid(column=0,row=0)
    im1 = Image.open(loc)
    p1 = np.asarray(im1)
    dkey = enrty_3.get()
    dkey = int(dkey)
    if mode == 0:
        test = image_encrypt(p1,dkey)
        msg = enrty_1.get()
        # label = tk.Label(top,text="secret message: "+msg).grid(column=1,row=2)
        pkey = enrty_2.get()
        # label = tk.Label(top,text="cipher pkey: "+pkey).grid(column=1,row=3)
        cipher = encrypt(msg,pkey)
        test = merge(test,cipher,dkey)
    elif mode == 1:
        test = image_encrypt(p1,dkey)
    elif mode == 2:
        test = p1.copy()
        msg = enrty_1.get()
        pkey = enrty_2.get()
        cipher = encrypt(msg,pkey)
        test = merge(test,cipher,dkey)
    else:
        print("error encrypt mode select input")
    
    im2 = Image.fromarray(test, mode="RGB")
    dirtemp = os.path.dirname(__file__)
    encrypted_image_name = os.path.join(dirtemp,"encrypted_img"+".png")
    im2.save(encrypted_image_name)
    im2_label = Image.open(encrypted_image_name)
    im2_label = im2_label.resize((400,300))
    im2_label = ImageTk.PhotoImage(im2_label)
    label3 = tk.Label(top,image=im2_label).grid(column=0,row=3)
    label = tk.Label(top,text="encrypted Image :").grid(column=0,row=2)

    # decreption::::::::::::::::::::::::::::::::::::::::
    im3 = Image.open(encrypted_image_name)
    p2 = np.asarray(im3)
    p2 = p2.copy()
    if mode == 0:
        p2,text = unmerge(p2,dkey)
        p2 = image_decrypt(p2,dkey)
        text = decrypt(text,pkey)
        # print(text)
    elif mode == 1:
        p2 = image_decrypt(p2,dkey)
    elif mode == 2:
        p2,text = unmerge(p2,dkey)
        text = decrypt(text,pkey)
        # print(text)
    else:
        print("error encrypt mode select input")
    
    im4 = Image.fromarray(p2, mode="RGB")
    decryption_image_name = os.path.join(dirtemp,"decryption_final"+".png")
    im4.save(decryption_image_name)
    im4_label = Image.open(decryption_image_name)
    im4_label = im4_label.resize((400,300))
    im4_label = ImageTk.PhotoImage(im4_label)
    def decrypt_show(mode):
        label = tk.Label(top,text="decrypted Image :").grid(column=1,row=0)
        label4= tk.Label(top,image=im4_label).grid(column=1,row=1)
        if mode == 0 or 2:
            label = tk.Label(top,text="secret message: "+msg+"\ncipher pkey: "+pkey+"\ndecrypted text: "+text).grid(column=1,row=3)
    button_decrypt = tk.Button(top, text="decrypt", padx= 30, command=lambda: decrypt_show(mode))
    button_decrypt.grid(column=1,row= 0)

    
def manual_decrypt(mode):
    top = tk.Toplevel()
    global im4_label
    loc = select_file()
    pkey = enrty_2.get()   
    dirtemp = os.path.dirname(__file__)
    # decreption::::::::::::::::::::::::::::::::::::::::
    im3 = Image.open(loc)
    p2 = np.asarray(im3)
    p2 = p2.copy()
    dkey = enrty_3.get()
    dkey = int(dkey)
    if mode == 0:
        p2,text = unmerge(p2,dkey)
        p2 = image_decrypt(p2,dkey)
        text = decrypt(text,pkey)
        # print(text)
    elif mode == 1:
        p2 = image_decrypt(p2,dkey)
    elif mode == 2:
        p2,text = unmerge(p2,dkey)
        text = decrypt(text,pkey)
        # print(text)
    else:
        print("error encrypt mode select input")
    
    im4 = Image.fromarray(p2, mode="RGB")
    decryption_image_name = os.path.join(dirtemp,"decryption_final"+".png")
    im4.save(decryption_image_name)
    im4_label = Image.open(decryption_image_name)
    im4_label = im4_label.resize((400,300))
    im4_label = ImageTk.PhotoImage(im4_label)
    label = tk.Label(top,text="decrypted Image :").grid(column=1,row=0)
    label4= tk.Label(top,image=im4_label).grid(column=1,row=1)
    if mode == 0 or 2:
        label = tk.Label(top,text="cipher key: "+pkey+"\ndecrypted text: "+text).grid(column=1,row=3)
    



# main program:::::::::::::::::::::::::::::::::::::::::::
root = tk.Tk()
root.title('DNA encryption graduation project')

# root.geometry("800x600")

mylabel = tk.Label(root, text="Enter secret message: ").grid(column=0,pady=5)
enrty_1= tk.Entry(root,width=40)
enrty_1.grid(column=0)
mylabel = tk.Label(root, text="Enter playfair cipher key: ").grid(column=0,pady=5)
enrty_2= tk.Entry(root,width=40)
enrty_2.grid(column=0)
mylabel = tk.Label(root, text="Enter dna and stego key (0 to 255): ").grid(column=0,pady=5)
enrty_3= tk.Entry(root,width=40)
enrty_3.grid(column=0)
mylabel = tk.Label(root, text="Select an image to be encrypted")
mylabel.grid(column=0,pady=5)
button1 = tk.Button(root, text="Encrypt", padx= 30, command=lambda: btn_encrypt(0))
button1.grid(column=0)
button2 = tk.Button(root, text="Encrypt(DNA only)", padx= 30, command=lambda: btn_encrypt(1))
button2.grid(column=0)
button3 = tk.Button(root, text="Encrypt(secret text only)", padx= 30, command=lambda: btn_encrypt(2))
button3.grid(column=0)
button4 = tk.Button(root, text="manual decryption", padx= 30, command=lambda: manual_decrypt(0))
button4.grid(column=0)

root.mainloop()