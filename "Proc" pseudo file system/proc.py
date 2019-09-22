import time
import sys

u_time_curr = [0]*50
u_time_prev = [0]*50
s_time_curr = [0]*50
s_time_prev = [0]*50
idle_time_curr = [0]*50
idle_time_prev = [0]*50

inter_curr = [0]*50
inter_prev = [0]*50

interval = 2

class ReadFile:
        def __init__(self, path):
                self.path = path

        def stat_file_data(self):
                global u_time_curr, u_time_prev, s_time_curr, s_time_prev, idle_time_prev, idle_time_curr
                i=0
                c=0
                d=0
                self.cpu={}
                self.cpu_utl = 0
                self.delta_u_time = 0
                self.delta_s_time = 0
                self.delta_idle_time = 0
        #       index=0
                self.total={}
                self.no_inter = 0
                self.delta_inter = 0
                while True:
                         with open(self.path, 'r') as stat_file:
                                count =0
                                for line in stat_file:
                                        if line.startswith ("cpu"):
                                                count =count+1
                                                logical_cpu=count-1
                                                split_total=line.split()
                                                self.cpu_name = split_total[0]
                                                self.u_time=split_total[1]
                                                self.s_time=split_total[3]
                                                self.idle_time=split_total[4]
                                                #x=split_total[1]
                                                #y=split_total[3]               
                                                #cpu=float(x)+ float(y)

                                                #print("Name of CPU = " +str(split_total[0])+ ".")
                                                       #print("User Time = " +str(split_total[1])+ ".")
                                                       #print("System Time  = " +str(split_total[3])+ ".")
                                                        #print("Idle Time  = " +str(split_total[4])+ ".")
                                                #print("CPU time = " +str(cpu)+ ".")
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
                                                        self.cpu_utl = ((self.delta_u_time + self.delta_s_time)/(self.delta_u_time + self.delta_s_time + self.delta_idle_time))*100                          
                                                        #self.u_cpu_utl = (((float(u_time_curr[i])/100)-(float(u_time_prev[i])/100))/3)*100
                                                        #self.s_cpu_utl = (((float(s_time_curr[i])/100)-(float(s_time_prev[i])/100))/3)*100
                                                        u_time_prev[i] = u_time_curr[i]
                                                        s_time_prev[i] = s_time_curr[i]
                                                        idle_time_prev[i] = idle_time_curr[i]
                                                        #print("User time is = " +(self.u_time)+ ".")
                                                        #print(self.u_cpu_utl)
                                                        self.cpu[c]=[self.cpu_name, self.u_time, self.s_time, self.idle_time, str(self.delta_u_time), str(self.delta_s_time), str(self.delta_idle_time), str(round(self.cpu_utl))]
                                                        c+=1
                                                        print(self.cpu)

                                                if line.startswith("intr"):
                                                split_inter = line.split()
                                                self.inter = split_inter[1]
                                                inter_curr[i] = self.inter
                                                if inter_prev[i] == 0:
                                                        inter_prev[i] = self.inter
                                                else:
                                                        self.delta_inter = (float(inter_curr[i]) - float(inter_prev[i]))
                                                        self.no_inter = (self.delta_inter)/2
                                                        inter_prev[i] = inter_curr[i]
                                                        self.total[d]=[str(self.no_inter)]
                                                        d+=1
                                                        print(self.total)
                                                        i+=1
                        time.sleep(interval)
                #       index += 1
                        #print("Total number of CPUs = " +str(count)+ ".")
                        #print("Number of Logical CPUs = " +str(logical_cpu)+ ".")
                        #print("CPU time = " +str(cpu)+ ".")
                        stat_file.close()
#print("Total number of CPUs = " +str(count)+ ".")
#print("Number of Logical CPUs = " +str(logical_cpu)+ ".")
if __name__ == "__main__":
    reader = ReadFile("/proc/stat")
    reader.stat_file_data()
