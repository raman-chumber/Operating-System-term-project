import os
import re
import Tkinter
from Tkinter import *
from ttk import *
import sys
import time
import heapq

interval = 2
d_read_curr = [0]*500
d_read_prev = [0]*500
d_write_curr = [0]*500
d_write_prev = [0]*500
b_read_curr = [0]*500
b_read_prev = [0]*500
b_write_curr = [0]*500
b_write_prev = [0]*500


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
      
   def GetDisk(self): # Getting System Statistics #
      global d_read_curr, d_read_prev, d_write_curr, d_write_prev, b_read_curr, b_read_prev, b_write_curr, b_write_prev
      index = 0
      i=0
      d=0
      self.h_Stat = {}
      self.no_d_read = 0
      self.no_d_write = 0
      self.no_b_read = 0
      self.no_b_write = 0
      self.delta_d_read = 0
      self.delta_d_write = 0
      self.delta_b_read = 0
      self.delta_b_write = 0
      disk_file= open("/proc/diskstats","r")
      for line in disk_file:
         if line.find('sda')!=-1:
            split_total = line.split()
            self.sda = split_total[2]
            self.d_read = split_total[4]
            self.b_read = split_total[3]
            self.d_write = split_total[8]
            self.b_write = split_total[10]
            d_read_curr[i] = self.d_read
            b_read_curr[i] = self.b_read
            d_write_curr[i] = self.d_write
            b_write_curr[i] = self.b_write
            if d_read_prev[i]==0 and d_write_prev[i] == 0 and b_read_prev[i]==0 and b_write_prev[i]==0:
               d_read_prev[i] = self.d_read
               d_write_prev[i] = self.d_write
               b_read_prev[i] = self.b_read
               b_write_prev[i] = self.b_write
            else:
               self.delta_d_read = float(d_read_curr[i]) - float(d_read_prev[i])
               self.delta_d_write = float(d_write_curr[i]) - float(d_write_prev[i])
               self.delta_b_read = float(b_read_curr[i]) - float(b_read_prev[i])
               self.delta_b_write = float(b_write_curr[i]) - float(b_write_prev[i])
               self.no_d_read = ((float(self.delta_d_read))/interval)*100
               self.no_d_write= ((float(self.delta_d_write))/interval)*100
               self.no_b_read = ((float(self.delta_b_read))/interval)*100
               self.no_b_write= ((float(self.delta_b_write))/interval)*100
               d_read_prev[i] = d_read_curr[i]
               d_write_prev[i] = d_write_curr[i]
               b_read_prev[i] = b_read_curr[i]
               b_write_prev[i] = b_write_curr[i]
            self.h_Stat[d]=[self.sda, str(self.no_d_read), str(self.no_d_write), str(self.no_b_read), str(self.no_b_write)]
            i+=1
            d+=1 
         #i=0  

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


def Display_disk():
	r.GetDisk()
	textBox4.delete('1.0',END)
	textBox4.insert(END,"Disk Stats: proc/diskstats \n\n")
	textBox4.insert(END,"Name\t\t"+"No of Disk Reads\t\t\t"+"No of Disk Writes\t\t\t"+"No of Block Reads\t\t\t"+"No of Block Writes\t\t\t"+"\n")
	textBox4.insert(END,r.h_Stat[0][0]+'\t\t'+"{0:.2f}".format(float(r.h_Stat[0][1]))+'\t\t\t'+"{0:.2f}".format(float(r.h_Stat[0][2]))+'\t\t\t'+"{0:.2f}".format(float(r.h_Stat[0][3]))+'\t\t\t'+"{0:.2f}".format(float(r.h_Stat[0][4]))+'\n')
	textBox4.insert(END,r.h_Stat[1][0]+'\t\t'+"{0:.2f}".format(float(r.h_Stat[1][1]))+'\t\t\t'+"{0:.2f}".format(float(r.h_Stat[1][2]))+'\t\t\t'+"{0:.2f}".format(float(r.h_Stat[1][3]))+'\t\t\t'+"{0:.2f}".format(float(r.h_Stat[1][4]))+'\n')
	r.h_Stat.clear()     
	root.after(3000,Display_disk)


r=Read()

Display_disk()
root.mainloop()




