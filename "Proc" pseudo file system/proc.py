{\rtf1\ansi\ansicpg1252\cocoartf1671\cocoasubrtf400
{\fonttbl\f0\fnil\fcharset0 HelveticaNeue;\f1\fnil\fcharset0 Menlo-Regular;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;\red255\green255\blue255;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;\cssrgb\c100000\c100000\c100000;}
\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\deftab560
\pard\pardeftab560\slleading20\partightenfactor0

\f0\fs24 \cf0 \
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\partightenfactor0

\f1\fs28 \cf2 \cb3 \CocoaLigature0 #Python Script to capture CPU and system statistics on an #interval basis: \
\
#cpu utilization in percentage:user mode, system mode and overall utilization\
\
count=0\
f=open("/proc/stat","r")\
cpu_search=f.readlines()\
for line in cpu_search:\
        if "cpu" in line:\
                count=count+1\
                logical_cpu=count-1\
print("Total number of CPUs = " +str(count)+ ".")\
print("Number of Logical CPUs = " +str(logical_cpu)+ ".")\
f.close()\
\
#for u time\
\
f=open("/proc/stat","r")\
ut_search=f.readlines()\
col=1\
u_time=[]\
s_time=[]\
for line1 in ut_search:\
        if line1.startswith("cpu"):\
                u_time.append(line1.split(' ')[col+1])\
                s_time.append(line1.split(' ')[col+3])\
\
#print(u_time)\
#print(s_time)\
\
x=u_time[0]\
y=s_time[0]\
#cpu=[]\
cpu=int(x)+int(y)\
print("CPU time= " +str(cpu)+ ".")\
\
f.close()}