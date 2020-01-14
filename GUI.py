import os
import re
import Tkinter
from Tkinter import *
from ttk import *
import sys
import time
import heapq

interval = 2

u_time_curr = [0]*50
u_time_prev = [0]*50
s_time_curr = [0]*50
s_time_prev = [0]*50
idle_time_curr = [0]*50
idle_time_prev = [0]*50

inter_curr = [0]*50
inter_prev = [0]*50

ctxt_curr = [0]*50
ctxt_prev = [0]*50

num_intr=0
num_ctxt=0

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
      global u_time_curr, u_time_prev, s_time_curr, s_time_prev, idle_time_prev, idle_time_curr
      global inter_curr, inter_prev, num_intr
      global ctxt_curr, ctxt_prev, num_ctxt
      i=0
      j=0
      k=0
      c=0
      d=0
      e=0
      index=0
      self.h_Top={}
      self.h_int={}
      self.ctxt_total={}
      
      self.no_inter = 0
      self.delta_inter = 0
      self.cpu_utl_u = 0
      self.cpu_utl_s = 0
      self.delta_u_time = 0
      self.delta_s_time = 0
      self.delta_idle_time = 0
      self.no_ctxt = 0
      self.delta_ctxt = 0
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
            if u_time_prev[i] and s_time_prev[i] and idle_time_prev[i] == 0:
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
         elif line.startswith("intr"):
            split_inter = line.split()
            self.inter = split_inter[1]
            inter_curr[j] = self.inter
            if inter_prev[j] == 0:
               inter_prev[j] = self.inter
            else:
               self.delta_inter = (float(inter_curr[j]) - float(inter_prev[j]))
               self.no_inter = (self.delta_inter)/interval
               inter_prev[j] = inter_curr[j]
               self.h_int[d]=[str(self.no_inter)]
               num_intr = self.h_int[d]
               j+=1
               d+=1
           #j = 0    
         elif line.startswith("ctxt"):
            split_ctxt = line.split()
            self.ctxt = split_ctxt[1]
            ctxt_curr[k] = self.ctxt
            if ctxt_prev[k] == 0:
               ctxt_prev[k] = self.ctxt
            else:
               self.delta_ctxt = (float(ctxt_curr[k]) - float(ctxt_prev[k]))
               self.no_ctxt = (self.delta_ctxt)/interval
               ctxt_prev[k] = ctxt_curr[k]
               self.ctxt_total[e]=[str(self.no_ctxt)]
               num_ctxt = self.ctxt_total[e]
               k+=1
               e+=1
            #k=0
   def GetMem(self): # Getting System Statistics #
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


def Display_system():
   r.GetData()
   r.GetMem()
   textBox1.delete('1.0',END)
   textBox1.insert(END,"CPU Utilization: proc/stat \n\n")
   textBox1.insert(END,"\tName\t\t"+"User Time\t\t"+"Idle Time\t\t"+"System Time\t\t"+"U_CPU_UTL\t\t"+ "S_CPU_UTL\t\t"+"\n")
   textBox1.insert(END,'\t'+r.h_Top[0][0]+'\t\t'+r.h_Top[0][1]+'\t\t'+r.h_Top[0][4]+'\t\t'+r.h_Top[0][5]+'\t\t'+"{0:.2f}".format(float(r.h_Top[0][2]))+'\t\t'+"{0:.2f}".format(float(r.h_Top[0][3]))+'\n')
   textBox1.insert(END,'\t'+r.h_Top[1][0]+'\t\t'+r.h_Top[1][1]+'\t\t'+r.h_Top[1][4]+"\t\t"+r.h_Top[1][5]+'\t\t'+"{0:.2f}".format(float(r.h_Top[1][2]))+"\t\t"+"{0:.2f}".format(float(r.h_Top[1][3]))+'\n')
   textBox1.insert(END,'\t'+r.h_Top[2][0]+'\t\t'+r.h_Top[2][1]+'\t\t'+r.h_Top[2][4]+"\t\t"+r.h_Top[2][5]+'\t\t'+"{0:.2f}".format(float(r.h_Top[2][2]))+"\t\t"+"{0:.2f}".format(float(r.h_Top[2][3]))+'\n')
   textBox1.insert(END,"----------------------------------------------------------------------------------------------------------\n\n")
   textBox1.insert(END,"Number of Interrupts\t\t"+"\n")
   textBox1.insert(END,str(num_intr)+'\t'+'\n')
   #textBox1.insert(END,'\t'+"{0:.2f}".format(float(r.num_intr[0][0]))+'\n')
   textBox1.insert(END,"\n")
   textBox1.insert(END,"----------------------------------------------------------------------------------------------------------\n\n")
   textBox1.insert(END,"Number of Context Switches\t\t"+"\n")
   textBox1.insert(END,str(num_ctxt)+'\t'+'\n')
   #textBox1.insert(END,'\t'+"{0:.2f}".format(float(r.ctxt_total[0][0]))+'\n')
   textBox1.insert(END,"\n")
   textBox1.insert(END,"----------------------------------------------------------------------------------------------------------\n\n")
   textBox1.insert(END,"Memory Utilization: proc/meminfo \n\n")
   textBox1.insert(END,"Total Memory\t\t\t"+"Free Memory\t\t"+"Mem_Util\t\t"+"\n")
   textBox1.insert(END,str(mem_total)+'\t\t\t'+str(r.h_Mem[0][1])+"\t\t"+"{0:.2f}".format(float(r.h_Mem[0][2]))+'\n') 
   r.h_Top.clear()  
   r.h_Mem.clear()   
   root.after(3000,Display_system)


r=Read()

Display_system()
root.mainloop()

