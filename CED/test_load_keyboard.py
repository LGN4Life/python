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

key_channel = 31
mask_handle = 0

#open library
lib_path = 'C:/CEDMATLAB/CEDS64ML/x64/ceds64int.dll'
ced = cedLib.open_library(lib_path)

#open data file
fhand = ced.S64Open(file_name)

channel_type = ced.S64ChanType(fhand, key_channel)
print('channel type = ' + str(channel_type))



no_mask = 0
max_events = 200

max_tick = ced.S64ChanMaxTime(fhand, key_channel)
start_tick = c_longlong(0)


text_marker = ced_class.S64Marker()


key_marker = (ced_class.S64Marker * max_events)()


t_pointer = POINTER(ced_class.S64Marker)

read_loop = True
key_list = []
time_list = []
loop_count = 0
while read_loop:
    events_read = ced.S64ReadMarkers(fhand, key_channel, t_pointer(key_marker), max_events, start_tick, max_tick, no_mask)
    print('events read  = ' + str(events_read))
    if events_read != max_events:
        read_loop = False
    else:
        for key_index in range(len(key_marker)):
            key_list.append(key_marker[key_index].m_Code1)
            key_list.append(key_marker[key_index].m_time)

    loop_count += 1
    start_tick = key_marker[events_read-1].m_time+1
    if loop_count > 2000:
        break

    print('current time  = ' + str(start_tick))
    print('loop count = ' + str(loop_count))



result = ced.S64Close(fhand)
print('file closed  = ' + str(result))
print('now explore the data')














result = ced.S64Close(fhand)
print('file closed  = ' + str(result))
print('now explore the data')
