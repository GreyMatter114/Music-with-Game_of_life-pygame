import os
import numpy as np
from tkinter import *
from tkinter import filedialog as fd
cells1=[]

def save(cells):
	e2=input("Enter file name:: ")
	os.chdir(os.path.dirname(__file__))
	direc=os.getcwd()
	path=f'{direc}/Saved/{e2}.txt'
	fp=open(path,"w+")
	for i in cells:
		for j in i:
			if j:
				fp.write("*")
			else:
				fp.write(" ")
		fp.write("\n")
	fp.close()
	
def load():
	c=0
	cells=[]
	filepath = fd.askopenfilename(title="Open a Text File", filetypes=(("text    files","*.txt"), ("all files","*.*")))
	f=open(filepath,'r')
	lines=f.readlines()
	f.close()
	try:
		for line in lines:
			l=[]
			for i in line:
				if i=="*":
					l.append(True)
				else:
					l.append(False)
			cells.append(l)

	except:
		print("Error displaying the file")
	return cells	