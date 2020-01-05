import time
import sys

interval = 2
inter_curr = [0]*5
inter_prev = [0]*5

class ReadFile:
        def __init__(self, path):
                self.path = path

        def print_data(self):
                global inter_curr, inter_prev
                index = 0
                i=0
                c=0
                self.total={}
                self.no_inter = 0
                self.delta_inter = 0
                while True:
                        with open(self.path, 'r') as stat_file:
                                for line in stat_file:
                                        if line.startswith("intr"):
                                        # if line starts with "inter" read the required columns #
                                                split_inter = line.split()
                                                self.inter = split_inter[1]
                                                inter_curr[i] = self.inter
                                                # if previous values are 0 meaning it is the first reading #
                                                if inter_prev[i] == 0:
                                                        inter_prev[i] = self.inter
                                                else:
                                                #if it is not the first reading then calculate the number of interrupts#
                                                        self.delta_inter = (float(inter_curr[i]) - float(inter_prev[i]))
                                                        self.no_inter = (self.delta_inter)/2
                                                        inter_prev[i] = inter_curr[i]
                                                        self.total[c]=[str(self.no_inter)]
                                                        i+=1
                                                        c+=1
                                                        print(self.total)
                        time.sleep(interval)
                        #index += 1
                        stat_file.close()
if __name__ == "__main__":
    # read values from stat file #
    reader = ReadFile("/proc/stat")
    reader.print_data()
