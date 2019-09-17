#cpu utilization in percentage:user mode, system mode and overall utilization\
import time
import sys

u_time_curr = [0]*5
u_time_prev = [0]*5
s_time_curr = [0]*5
s_time_prev = [0]*5
idle_time_curr = [0]*5
idle_time_prev = [0]*5

interval = 2

class ReadFile:
        def __init__(self, path):
                self.path = path
                self.interval_one = 1

        def print_data(self):
                global u_time_curr, u_time_prev, s_time_curr, s_time_prev, idle_time_prev, idle_time_curr
                i=0
                index=0
                self.cpu={}
                self.cpu_utl = 0
                #self.s_cpu_utl = 0
                self.delta_u_time = 0
                self.delta_s_time = 0
                self.delta_idle_time = 0
                while(index<10):
                        with open(self.path, 'r') as stat_file:
                                count =0
                                c=0
                                i=0
                                for line in stat_file:
                                        if line.startswith ("cpu"):
                                                count =count+1
                                                logical_cpu=count-1
                                                split_total=line.split()
                                                self.cpu_name = split_total[0]
                                                self.u_time=split_total[1]
                                                self.s_time=split_total[3]
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
                                                        self.cpu_utl = ((self.delta_u_time + self.delta_s_time)/(self.delta_u_time + self.delta_s_time + self.delta_idle_time))*100
                                                        u_time_prev[i] = u_time_curr[i]
                                                        s_time_prev[i] = s_time_curr[i]
                                                        idle_time_prev[i] = idle_time_curr[i]
                                                         self.cpu[c]=[self.cpu_name, self.u_time, self.s_time, self.idle_time, str(self.delta_u_time), str(self.delta_s_time), str(self.delta_idle_time), str(self.cpu_utl)]
                                                        i+=1
                                                        c+=1

                                                        print(self.cpu)
                        time.sleep(interval)
                        index += 1
                        stat_file.close()
if __name__ == "__main__":
    reader = ReadFile("/proc/stat")
    reader.print_data()