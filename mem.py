#memory stat file
import time
interval = 3

curr_free_mem = [0]*50
prev_free_mem = [0]*50

class ReadFile:
        def __init__(self, path):
                self.path = path

        def mem(self):
                global mem_total, curr_free_mem, prev_free_mem
                a=0
                i=0
                mem_total = 0
                self.mem_free = 0
                self.h_Mem={}
                self.mem_utl = 0
                #index=0
                while True:
                        with open(self.path, 'r') as mem:
                                for line in mem:
                                        if line.startswith('MemT'):
                                                split_total=line.split()
                                                self.mem_total=split_total[1]
                                                mem_total =self.mem_total
                                        if line.startswith('MemF'):
                                                split_total=line.split()
                                                self.mem_free=split_total[1]
                                                curr_free_mem[i] = self.mem_free
                                                if prev_free_mem[i] == 0:
                                                        prev_free_mem[i]= self.mem_free
                                                else:
                                                        self.mem_free = (float(curr_free_mem[i]) + float(prev_free_mem[i]))/2
                                                        self.mem_utl = ((float(mem_total) - float(self.mem_free))/ (float(mem_total))) * 100
                                                        prev_free_mem[i] = curr_free_mem[i]
                                                        self.h_Mem[a]=[mem_total, str(self.mem_free), str(self.mem_utl)]
                                                        i+=1
                                                        a+=1
                                                        print(self.h_Mem)
                        time.sleep(interval)
                        #index+=1
                        mem.close()

                                #print(line)

if __name__ == "__main__":
    reader = ReadFile("/proc/meminfo")
    reader.mem()
