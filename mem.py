import os
import re
import Tkinter
from Tkinter import *
from ttk import *
import sys
import time
import heapq

interval = 2

curr_free_mem = [0]*50
prev_free_mem = [0]*50


locallist=[]

heap=[]
p_uname = re.compile(r'^(?P<name>\w+):(?P<value>\w+):(?P<measure>\w+)?')
user_uid={} 
uid_user={}



class Read:
   
   def __init__(self):
      s=0
      self.firstInterval = 1
      self.h_proc={}
      
   def GetData(self): # Getting System Statistics #
      global mem_total, curr_free_mem, prev_free_mem
      a=0
      l=0
      mem_total = 0
      self.mem_free = 0
      self.h_Mem={}
      self.mem_utl = 0
      file_mem= open("/proc/meminfo","r")
      for line in file_mem:
         if line.startswith('MemTotal'):
            split_total=line.split()
            self.mem_total=split_total[1]
            mem_total =self.mem_total
         if line.startswith('MemFree'):
            split_total=line.split()
            self.mem_free=split_total[1]
            curr_free_mem[l] = self.mem_free
            if prev_free_mem[l] == 0:
               prev_free_mem[l]= self.mem_free
            else:
               self.mem_free = (float(curr_free_mem[l]) + float(prev_free_mem[l]))/2
               self.mem_utl = ((float(mem_total) - float(self.mem_free))/ (float(mem_total))) * 100
               prev_free_mem[l] = curr_free_mem[l]
            self.h_Mem[a]=[mem_total, str(self.mem_free), str(self.mem_utl)] 
                                           
            l+=1
            a+=1
         l=0   

root=Tkinter.Tk()

root.title("Activity Monitor")
root.geometry(("%dx%d")%(1000,1000))
note = Notebook(root)
note.place(x = 40, y = 40, height = 800, width = 900)

frame1 = Frame(note)
frame2 = Frame(note)
frame3 = Frame(note)
frame4 = Frame(note)
frame5 = Frame(note)

note.add(frame1, text = "CPU Stats")
note.add(frame2, text = "Disk Stats")
note.add(frame3, text = "Network Stats")
note.add(frame4, text = "Process Stats")
note.add(frame5, text = "User Stats")

Label(frame5, text = "Username :", anchor = 'center', borderwidth = '4').grid(row = 0, column = 0)
Label(frame5, text = "Process name :", anchor = 'center', borderwidth = '4').grid(row = 1, column = 0)

e1 = Entry(frame5)
e2 = Entry(frame5)
e1.grid(row = 0, column = 1, padx = 4)
e2.grid(row = 1, column = 1, padx = 4)
#Button(frame5, text = "Find", command=Sample).grid(row = 0, column = 2,sticky = 'w', pady=4)      
Button(frame5, text = "clear").grid(row = 1, column = 2,sticky = 'w', pady=4)

textBox1=Text(frame1,height=800,width=400)
textBox1.grid(row=0,column=0,columnspan=3)

textBox2=Text(frame4,height=400,width=200)
textBox2.grid(row=0,column=0,columnspan=3)

textBox3=Text(frame3,height=400,width=200)
textBox3.grid(row=0,column=0,columnspan=3)
 
textBox4=Text(frame2,height=400,width=200)
textBox4.grid(row=0,column=0,columnspan=3)


#username()


def Display_memory():
    r.GetData()
    textBox1.delete('1.0',END)
    textBox1.insert(END,"File: proc/meminfo \n\n")
    textBox1.insert(END,"Total Memory\t\t\t"+"Free Memory\t\t"+"Mem_Util\t\t"+"\n")
    textBox1.insert(END,str(mem_total)+'\t\t\t'+str(r.h_Mem[0][1])+"\t\t"+"{0:.2f}".format(float(r.h_Mem[0][2]))+'\n') 
    r.h_Mem.clear()     
    root.after(3000,Display_memory)


r=Read()

Display_memory()
root.mainloop()