import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk,Image
from pathlib import Path
from dna_encryption import image_encrypt,image_decrypt
from playfair_cipher import encrypt,decrypt
import numpy as np

def merge(image,text):
    cols = image.shape[0]
    rows = image.shape[1]
    list1 = []
    for i in range (0,len(text)):
        randc = np.random.randint(0,cols)
        randr = np.random.randint(0,rows)
        list1.append(randc)
        list1.append(randr)
        list1.append(image[randc,randr,2])
        image[randc,randr,2] = ord(text[i])
        
    return image,list1

def unmerge(image,list1):
    text= ""
    for i in range(0,len(list1),3):
        
        text = text + chr(image[list1[i],list1[i+1],2])
        image[list1[i],list1[i+1],2]= list1[i+2]
    return image,text


def select_file():
    root.filename = filedialog.askopenfilename(initialdir=Path.cwd(),title="select an image to encrypt")
    return root.filename
def btn_encrypt():
    top = tk.Toplevel()
    global im1,im2,im1_label,im2_label,im4_label
    # encryption::::::::::::::::::::::::::::::::::::::::::::::::::
    loc = select_file()
    im1_label = Image.open(loc)
    im1_label = im1_label.resize((300,200))
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
    test,list1 = merge(test,cipher)
    im2 = Image.fromarray(test, mode="RGB")
    encrypted_image_name = "encrypted_img.png"
    im2.save(encrypted_image_name)
    im2_label = Image.open(encrypted_image_name)
    im2_label = im2_label.resize((300,200))
    im2_label = ImageTk.PhotoImage(im2_label)
    label3 = tk.Label(top,image=im2_label).grid(column=0,row=3)
    label = tk.Label(top,text="encrypted Image :").grid(column=0,row=2)


    # decreption::::::::::::::::::::::::::::::::::::::::
    im3 = Image.open("encrypted_img.png")
    p2 = np.asarray(im3)
    p2 = p2.copy()
    p2,text = unmerge(p2,list1)
    p2 = image_decrypt(p2)
    text = decrypt(text,key)
    print(text)
    im4 = Image.fromarray(p2, mode="RGB")
    decryption_image_name = "decryption_final.png"
    im4.save(decryption_image_name)
    im4_label = Image.open(decryption_image_name)
    im4_label = im4_label.resize((300,200))
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