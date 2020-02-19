from ctypes import *
from ctypes import util
import os
import numpy as np
import struct
import sys
from matplotlib import pyplot as plt
import cedLib
from time import sleep
file_name = b"rub_190719_con_024.smr"

sys.path.append("C:/CEDMATLAB")

continuous_channel = 2
mask_handle = 0


lib_path = 'C:/CEDMATLAB/CEDS64ML/x64/ceds64int.dll'
ced = cedLib.open_library(lib_path)
reset_mask = ced.S64ResetAllMasks()


result = ced.S64IsOpen(1)
open_file_count = ced.S64CloseAll()

fhand = ced.S64Open(file_name)



max_tick = ced.S64ChanMaxTime(fhand, continuous_channel)
continuous_data = np.zeros((max_tick,), dtype=c_float)

c_pointer = continuous_data.ctypes.data_as(POINTER(c_float))

max_count = len(continuous_data)
start_tick = c_longlong(0)
max_tick = c_longlong(max_tick)
first_event = np.array([0], dtype=c_longlong)
# first_event = c_longlong(0)

f_pointer =  first_event.ctypes.data_as((POINTER(c_longlong)))
# f_pointer =  POINTER(c_longlong)

returned_ticks = ced.S64ReadWaveF(fhand, continuous_channel, c_pointer, max_count, start_tick, max_tick,\
                                  f_pointer, mask_handle)

plt.plot(continuous_data[1:30000])
plt.show()

print('returned ticks = ' + str(returned_ticks))

result = ced.S64Close(fhand)

print('file closed  = ' + str(result))