import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk,Image
from dna_encryption import image_encrypt,image_decrypt,eightbitbinary
from playfair_cipher import encrypt,decrypt
import numpy as np
import os

# [16, 18, 21, 34, 39, 50, 60, 68, 77, 84, 90, 102, 106, 120, 135, 136] mb used later

def merge(image,text):
    # using the magic(4) in matlab to create a matrix each value in that matrix determine how far is the next pixel in the merging technique
    key_matrix = np.array([16,2,3,13,5,11,10,8,9,7,6,12,4,14,15,1])    
    cols = image.shape[1]
    rows = image.shape[0]
    text_length = len(text)
    # section of code to test out if the image can handle the inputed text
    s = (text_length+1)%16
    su = 0
    for i in range(0,s):
        su += key_matrix[i]
    su = (int(text_length/16)*136) + su 
    if(su > (rows*cols)-1):
        print("ERROR/////: the image can't handle that many characters")
        return image
    position = 0
    # hiding the in the lower bit of the color values (8-bits) the least two bits for Red and Green, 4 least bits in the Blue color coz in reality the eye only sees the blue color about 20 times less than red and green
    # a simple for-loop for hiding the text than the same code to put the letter "j" as a stop sign for the merging technique
    for i in range (0,text_length):
        s = i%16
        position += key_matrix[s]
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
    i += 1
    s = i%16
    position += key_matrix[s]
    row = int(position / cols)
    col = position % cols
    # print(i,",",position,",row:",row,",",rows,",col",col,",",cols)
    char = eightbitbinary(ord("j"))
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

def unmerge(image):
    key_matrix = np.array([16,2,3,13,5,11,10,8,9,7,6,12,4,14,15,1]) 
    cols = image.shape[1]
    text= ""
    position = 0
    i = 0
    while True:   
        s = i%16
        position += key_matrix[s]
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
            return image,text
        text += char
        i += 1
    


def select_file():
    root.filename = filedialog.askopenfilename(initialdir=os.path.dirname(__file__),title="select an image to encrypt")
    return root.filename
def btn_encrypt():
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
    test = image_encrypt(p1)
    msg = enrty_1.get()
    # label = tk.Label(top,text="secret message: "+msg).grid(column=1,row=2)
    key = enrty_2.get()
    # label = tk.Label(top,text="cipher key: "+key).grid(column=1,row=3)
    cipher = encrypt(msg,key)
    test = merge(test,cipher)
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
    p2,text = unmerge(p2)
    p2 = image_decrypt(p2)
    text = decrypt(text,key)
    print(text)
    im4 = Image.fromarray(p2, mode="RGB")
    decryption_image_name = os.path.join(dirtemp,"decryption_final"+".png")
    im4.save(decryption_image_name)
    im4_label = Image.open(decryption_image_name)
    im4_label = im4_label.resize((400,300))
    im4_label = ImageTk.PhotoImage(im4_label)
    label = tk.Label(top,text="decrypted Image :").grid(column=1,row=0)
    label4= tk.Label(top,image=im4_label).grid(column=1,row=1)
    label = tk.Label(top,text="secret message: "+msg+"\ncipher key: "+key+"\ndecrypted text: "+text).grid(column=1,row=3)


# main program:::::::::::::::::::::::::::::::::::::::::::
root = tk.Tk()
root.title('DNA encryption graduation project')

# root.geometry("800x600")

mylabel = tk.Label(root, text="Select an image to be encrypted")
mylabel.grid(column=0,pady=5)
# im1 = ImageTk.PhotoImage(Image.open("decryption_final.png"))
# label1 =  tk.Label(root, image=im1)
# label1.pack()

button1 = tk.Button(root, text="Encrypt", padx= 30, command=btn_encrypt)
button1.grid(column=0)
mylabel = tk.Label(root, text="Enter secret message: ").grid(column=0,pady=5)
enrty_1= tk.Entry(root,width=40)
enrty_1.grid(column=0)
mylabel = tk.Label(root, text="Enter playfair cipher key: ").grid(column=0,pady=5)
enrty_2= tk.Entry(root,width=40)
enrty_2.grid(column=0)



root.mainloop()