import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from PIL import ImageTk,Image
import shutil
import pathlib
import time
global img
root=tk.Tk()
root.title("Licence Plate Detection And Extraction for Non-Helmeted Motorcyclists")

#-------------------------------------------------------------------------
import cv2
import imutils
import pytesseract
import numpy as np
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
#-------------------------------------------------------------------------
def lpextract():

	var1=os.path.isfile("result_img/non-helmet.jpg")
	if var1==False:
		messagebox.showerror("Helmet Detected","Helmet has detected for rider(s).")
		return

	if os.path.isfile("result_img/licenceplate.jpg")==False:
		messagebox.showerror("LP Error","No License Plate has been detected!")
		return
	img = cv2.imread('result_img/licenceplate.jpg')
	image=np.array(img)
	image = imutils.resize(image,width=600)
	text=pytesseract.image_to_string(image)
	#print("LP:",text)
	
	gray=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
	#cv2.imshow("grayscaled image",gray)
	#cv2.waitKey(0)
	edged = cv2.Canny(gray,170,200)
	#cv2.imshow("Canny Edged Image",edged)
	#cv2.waitKey(0)
	thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	#cv2.imshow("OTSU processed image",thresh)
	#cv2.waitKey(0)
	blur=cv2.medianBlur(gray, 3)
	blur = cv2.resize(blur, None, fx = 2, fy = 2, interpolation = cv2.INTER_CUBIC)
	#cv2.imshow("Median Blurred Image",gray)
	#cv2.waitKey(0)
	bilat=cv2.bilateralFilter(blur,11,17,17)
	#edged = cv2.Canny(gray,170,200)
	
	text=""
	text1=pytesseract.image_to_string(blur,config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 6 --oem 3')
	list1=text1.split()
	def checkstr(str):
		flag1=False
		flag2=False
		flag3=False
		if len(str)>=4:
			flag3=True
		for i in str:
			if i.isalpha():
				flag1=True
			if i.isdigit():
				flag2=True
		return flag1 and flag2 and flag3

	for i in list1:
		if checkstr(i)==True:
			text=text+i;
	
	def messageWindow1():
		def destlabel():
			cv2.destroyAllWindows()
		win=Toplevel()
		win.title('License Plate Extracted')
		message="License Plate Number:"+text
		Label(win, text=message, font=('helvetica',8,'bold')).pack()
		Button(win,text='OK',command=lambda:[destlabel(),win.destroy()]).pack()
		cv2.imshow("License Plate",image)
		return
	
	def messageWindow2():
		def destlabel():
			cv2.destroyAllWindows()
		win=Toplevel()
		win.title('License Plate Extracted')
		message="License Plate Number has been partially extracted\nNumber:"+text1
		Label(win, text=message, font=('helvetica',8,'bold')).pack()
		Button(win,text='OK',command=lambda:[destlabel(),win.destroy()]).pack()
		cv2.imshow("License Plate",image)	
		return
	
	if text=="":
		messageWindow2()
	else:
		messageWindow1()
	print(text,text1)
	file1=open('detectedlp.txt','a')
	file1.write(text+"\n")
	file1.close
	return









#-------------------------------------------------------------------------
canvas1=tk.Canvas(root,width=800,height=200,bg='gray90',relief='raised')
canvas1.pack()

def mycmd():
	os.system('cmd /c "dir"')



def loadphoto():
	filename=askopenfilename()
	print(filename)
	image=Image.open(filename)
	#img=image.rotate(270)
	img=image.resize((780,780),Image.ANTIALIAS)

	img=ImageTk.PhotoImage(img)
	canvas2=tk.Canvas(root,width=800,height=800,bg='gray90',relief='raised')
	canvas2.img=img
	
	obj1=canvas2.create_image(0,0,image=img,anchor="nw")
	canvas2.pack(fill=BOTH,expand=YES)

	def clearall():
		canvas2.delete(obj1)
		canvas2.destroy()
		return
	def cleardir():
		canvas2.destroy()
		strdir=r'%s' % os.getcwd().replace('\\','/')+"/result_img"
		shutil.rmtree(strdir)
		os.mkdir('result_img')
		return

	def detecthelmet():
		str1="cmd /c darknet.exe detector test data/obj.data cfg/helmet.cfg backup/helmet_8000.weights "
		str3=" -dont_show -ext_output > resultbbox.txt"
		str2=str1 + filename + str3
		os.system(str2)
		clearall()
		time.sleep(1)
		image1=Image.open('predictions.jpg')
		img1=image1.resize((780,780),Image.ANTIALIAS)
		img1=ImageTk.PhotoImage(img1)

		canvas3=tk.Canvas(root,width=800,height=800,bg='gray90',relief='raised')
		canvas3.img1=img1
	
		canvas3.create_image(0,0,image=img1,anchor="nw")
		canvas3.pack(fill=BOTH,expand=YES)

		def cleardet():
			canvas3.delete('all')
			canvas3.destroy()
			strdir=r'%s' % os.getcwd().replace('\\','/')+"/result_img"
			shutil.rmtree(strdir)
			os.mkdir('result_img')
			return

		button6=tk.Button(text='Clear Detection',command=cleardet,bg='green',fg='white',font=('helvetica',12,'bold'))
		canvas1.create_window(440,130,window=button6)
		return
		

	def showlptxt():
		os.system("detectedlp.txt")
		return

	button3=tk.Button(text='  Clear  ',command=cleardir,bg='green',fg='white',font=('helvetica',12,'bold'))
	canvas1.create_window(75,130,window=button3)
	button5=tk.Button(text='Extract LP',command=lpextract,bg='green',fg='white',font=('helvetica',12,'bold'))
	canvas1.create_window(285,130,window=button5)
	button4=tk.Button(text='Detect',command=detecthelmet,bg='green',fg='white',font=('helvetica',12,'bold'))
	canvas1.create_window(175,130,window=button4)
	button7=tk.Button(text='Show Detected LPs',command=showlptxt,bg='green',fg='white',font=('helvetica',8,'bold'))
	canvas1.create_window(700,130,window=button7)
	

#button1=tk.Button(text='dir',command=mycmd,bg='blue',fg='white',font=('helvetica',12,'bold'))
#canvas1.create_window(75,50,window=button1)
def showinf():
	messagebox.showinfo("Info of the project","Project Details\nCreated by:\n Amal Mohan (SCT17CS010)\n Aman M Rafi(SCT17CS012)\n Anjali BS(SCT17CS016)\n\nBuild Using Darknet,YoloV3,OpenCV,Python\nGUI based on KTinker(Python)")

button2=tk.Button(text=' Get file ',command=loadphoto,bg='green',fg='white',font=('helvetica',12,'bold'))
canvas1.create_window(75,60,window=button2)

button8=tk.Button(text=' i ',command=showinf,bg='blue',fg='white',font=('helvetica',8,'bold'))
canvas1.create_window(750,30,window=button8)

root.mainloop()