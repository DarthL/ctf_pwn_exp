#!/usr/bin/env python
# -*- coding: utf-8 -*-
# XD university 2014 the only reverse problem
from zio import *

'''
.text:00401000                 push    ebp
.text:00401001                 mov     ebp, esp
.text:00401003                 sub     esp, 58h
.text:00401006                 push    ebx
.text:00401007                 push    esi
.text:00401008                 push    edi
.text:00401009                 lea     edi, [ebp-58h]

55 8B EC 83 EC 58 53 56  57 8D 7D A8

half key: (apply 55 8B EC 83 EC 58)
    1. llozmg
    2. ljozkg
'''

'''
open dump file and prepare
'''
def Prepare():
    global byte_41204C
    global byte_41214C
    # memory dump file
    dump_41204C = open('./dump41204c','rb')
    byte_41204C = []
    for i in range(256):
        byte_41204C.append(ord(dump_41204C.read(1)))
    # instruction dump file
    dump_41214C = open('./dump41214c','rb')
    byte_41214C = []
    for i in range(256):
        byte_41214C.append(hex(ord(dump_41214C.read(1))))


'''
Brute force to get the final key
testing 53 56  57 8D 7D A8
'''
def Getkey(half_key):
    label = 1
    for i in range(0x21, 0x7e+1):
        for j in range(0x21, 0x7e+1):
            inp = chr(i) + chr(j) + half_key
            new_41204C = []
            for k in range(256):
                new_41204C.append(0x00)
            n = 0
            for m in range(256):
                new_41204C[m] = byte_41204C[m] ^ ord(inp[n])
                n += 1
                n %= 8
            code = []
            for k in range(256):
                code.append(0x00)
            for k in range(256):
                code[new_41204C[k]] = byte_41214C[k]
            if(code[0]=='0x55' and code[1]=='0x8b' and code[2]=='0xec' and\
                code[3]=='0x83' and code[4]=='0xec' and code[5]=='0x58' and\
                code[6]=='0x53' and code[7]=='0x56' and code[8]=='0x57' and\
                code[9]=='0x8d'):
                log(inp, 'red')
                label = 0
    if (label):
        log('none', 'red')

if __name__ == '__main__' :
    log('Open dump file and prepare', 'blue')
    Prepare()

    for s in ('ljozkg', 'llozmg'):
        log('Brute force ' + s + ': ', 'yellow')
        Getkey(s)

'''
another way to get the flag bypass the key Verify
import os
a = '=<:=<:<:=<?;u@|=qp?~:|t|'
for i in a:
    sys.stdout.write(chr(ord(i)-12))
'''
