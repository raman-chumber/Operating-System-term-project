import os
import re
import Tkinter
from Tkinter import *
from ttk import *
import sys
import time
import heapq


u_time_curr = [0]*50
u_time_prev = [0]*50
s_time_curr = [0]*50
s_time_prev = [0]*50
idle_time_curr = [0]*50
idle_time_prev = [0]*50


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
#-------------------------------------------------CPU Stat-------------------------------------------------------#
      
   def GetData(self): # Getting System Statistics #
      global u_time_curr, u_time_prev, s_time_curr, s_time_prev, idle_time_prev, idle_time_curr
      c=0
      d=0
      i=0
      self.h_Top={}
      self.cpu_utl_u = 0
      self.cpu_utl_s = 0
      self.delta_u_time = 0
      self.delta_s_time = 0
      self.delta_idle_time = 0
      file_stat= open("/proc/stat","r")
      for line in file_stat :
         if line.startswith ('cpu'):
            split_total=line.split()
            self.cpu_name = split_total[0]
            self.u_time=split_total[1]
            self.s_time=split_total [3]
            self.idle_time=split_total[4]
            u_time_curr[i] = self.u_time
            s_time_curr[i] = self.s_time
            idle_time_curr[i] = self.idle_time 
            if u_time_prev[i]==0 and s_time_prev[i]==0 and idle_time_prev[i] == 0:
               u_time_prev[i] = self.u_time
               s_time_prev[i] = self.s_time
               idle_time_prev[i] = self.idle_time
            else: 
               self.delta_u_time = (float(u_time_curr[i]) - float(u_time_prev[i]))
               self.delta_s_time = (float(s_time_curr[i]) - float(s_time_prev[i]))
               self.delta_idle_time = (float(idle_time_curr[i]) - float(idle_time_prev[i]))
               self.cpu_utl_u = ((self.delta_u_time)/(self.delta_u_time + self.delta_s_time + self.delta_idle_time))*100
               self.cpu_utl_s = ((self.delta_s_time)/(self.delta_u_time + self.delta_s_time + self.delta_idle_time))*100
               u_time_prev[i] = u_time_curr[i]
               s_time_prev[i] = s_time_curr[i]
               idle_time_prev[i] = idle_time_curr[i]
                   
            self.h_Top[c]=[self.cpu_name,self.u_time,str(self.cpu_utl_u),str(self.cpu_utl_s),self.idle_time,self.s_time]     
                   
            i+=1
            c+=1             
         #i = 0

#---------------------------------------Display using Tkinter---------------------------------------#

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


#CPU Display

def Display_system():
	r.GetData()
	textBox1.delete('1.0',END)
	textBox1.insert(END,"File: proc/stat \n\n")
	textBox1.insert(END,"\tName\t\t"+"User Time\t\t"+"Idle Time\t\t"+"System Time\t\t"+"U_CPU_UTL\t\t"+ "S_CPU_UTL\t\t"+"\n")
	textBox1.insert(END,'\t'+r.h_Top[0][0]+'\t\t'+r.h_Top[0][1]+'\t\t'+r.h_Top[0][4]+'\t\t'+r.h_Top[0][5]+'\t\t'+"{0:.2f}".format(float(r.h_Top[0][2]))+'\t\t'+"{0:.2f}".format(float(r.h_Top[0][3]))+'\n')
	textBox1.insert(END,'\t'+r.h_Top[1][0]+'\t\t'+r.h_Top[1][1]+'\t\t'+r.h_Top[1][4]+"\t\t"+r.h_Top[1][5]+'\t\t'+"{0:.2f}".format(float(r.h_Top[1][2]))+"\t\t"+"{0:.2f}".format(float(r.h_Top[1][3]))+'\n')
	textBox1.insert(END,'\t'+r.h_Top[2][0]+'\t\t'+r.h_Top[2][1]+'\t\t'+r.h_Top[2][4]+"\t\t"+r.h_Top[2][5]+'\t\t'+"{0:.2f}".format(float(r.h_Top[2][2]))+"\t\t"+"{0:.2f}".format(float(r.h_Top[2][3]))+'\n')
	
	r.h_Top.clear()     
	root.after(3000,Display_system)


r=Read()

Display_system()
root.mainloop()

