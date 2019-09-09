#cpu utilization in percentage:user mode, system mode and overall utilization\
index=0
while (index < 10):

	count=0
	f=open("/proc/stat","r")
	cpu_search=f.readlines()
	for line in cpu_search:
        	if "cpu" in line:
                	count=count+1
                	logical_cpu=count-1
	print("Total number of CPUs = " +str(count)+ ".")
	print("Number of Logical CPUs = " +str(logical_cpu)+ ".")
	f.close()
#for u time

	f=open("/proc/stat","r")
	ut_search=f.readlines()
	col=1
	u_time=[]
	s_time=[]
	for line1 in ut_search:
        	if line1.startswith("cpu"):
                	u_time.append(line1.split(' ')[col+1])
                	s_time.append(line1.split(' ')[col+3])
#print(u_time)
#print(s_time)
	x=u_time[0]
	y=s_time[0]
#cpu=[]
	cpu=int(x)+int(y)
	print("CPU time= " +str(cpu)+ ".")
	f.close()
	time.sleep(5)
	index += 10