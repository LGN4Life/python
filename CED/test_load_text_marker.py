from ctypes import *
from ctypes import util
import os
import numpy as np
import struct
import sys
from matplotlib import pyplot as plt
import cedLib
import ced_class
from time import sleep
file_name = b"rub_190719_con_024.smr"

sys.path.append("C:/CEDMATLAB")

text_channel = 30
mask_handle = 0

#open library
lib_path = 'C:/CEDMATLAB/CEDS64ML/x64/ceds64int.dll'
ced = cedLib.open_library(lib_path)

#open data file
fhand = ced.S64Open(file_name)

channel_type = ced.S64ChanType(fhand, text_channel)
print('channel type = ' + str(channel_type))

row_count = c_int(0)
col_count = c_int(0)
r_pointer = POINTER(c_int)
c_pointer = POINTER(c_int)
text_count = ced.S64GetExtMarkInfo(fhand, text_channel, r_pointer(row_count), c_pointer(col_count))

no_mask = 0
max_tick = ced.S64ChanMaxTime(fhand, text_channel)
start_tick = c_longlong(0)

text_marker = ced_class.S64Marker()
t_pointer = POINTER(ced_class.S64Marker)
string_buffer = create_string_buffer(row_count.value)
# s_pointer = POINTER(c_char)

#input: [file handle, channel number, pointer to a S64Marker object, pointer to hold the returned string,
    # start tick, end tick, mask handle]
text_list = []
time_list = []
start_tick = start_tick.value
loop_count = 0
while start_tick < max_tick:
    start_time = ced.S64TicksToSecs(fhand, start_tick)
    print('start_time  = ' + str(start_time))

    ced.S64Read1TextMark(fhand, text_channel, t_pointer(text_marker), string_buffer, start_tick, max_tick, no_mask)
    text_list.append(string_buffer.value)
    print('start_tick  = ' +  str(start_tick))
    print(' current string was found at : ' + str(text_marker.m_time))
    if text_marker.m_time < start_tick:
        break
    start_tick = text_marker.m_time+1
    loop_count +=1
    if loop_count > 2000:
        break

    print('current string = ' +str(string_buffer.value))

    print('loop count = ' + str(loop_count))




result = ced.S64Close(fhand)
print('file closed  = ' + str(result))
print('now explore the data')
