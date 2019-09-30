import time

interval = 2
ctxt_curr = [0]*50
ctxt_prev = [0]*50

class ReadFile:
        def __init__(self, path):
                self.path = path

        def ctxt(self):
                global ctxt_curr, ctxt_prev
                index = 0
                i=0
                c=0
                self.total={}
                self.no_ctxt = 0
                self.delta_ctxt = 0
                while True:
                        with open(self.path, 'r') as stat_file:
                                for line in stat_file:
                                        if line.startswith("ctxt"):
                                                split_ctxt = line.split()
                                                self.ctxt = split_ctxt[1]
                                                ctxt_curr[i] = self.ctxt
                                                if ctxt_prev[i] == 0:
                                                        ctxt_prev[i] = self.ctxt
                                                else:
                                                        self.delta_ctxt = (float(ctxt_curr[i]) - float(ctxt_prev[i]))
                                                        self.no_ctxt = (self.delta_ctxt)/2
                                                        ctxt_prev[i] = ctxt_curr[i]
                                                        self.total[c]=[str(self.no_ctxt)]
                                                        i+=1
                                                        c+=1
                                                        print(self.total)
                        time.sleep(interval)
                        #index += 1
                        stat_file.close()
if __name__ == "__main__":
    reader = ReadFile("/proc/stat")
    reader.ctxt()
