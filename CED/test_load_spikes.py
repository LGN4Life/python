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

spike_channel = c_int(3)
max_events = 5
wave_mark = 1
mask_handle = c_int(1)
mask_mode = 0



lib_path = 'C:/CEDMATLAB/CEDS64ML/x64/ceds64int.dll'
# ced = LibraryLoader(WinDLL).LoadLibrary(lib_path)
ced = cedLib.open_library(lib_path)
reset_mask = ced.S64ResetAllMasks()
print('reset mask ' + str(reset_mask))


result = ced.S64IsOpen(1)
print('result  = ' + str(result))
open_file_count = ced.S64CloseAll()
print('current number of open files  = ' + str(open_file_count))

fhand = ced.S64Open(file_name)
print('fhand = ' + str(fhand))



max_tick = ced.S64ChanMaxTime(fhand, spike_channel)

iOk = ced.S64SetMaskMode(mask_handle, mask_mode)
print('mask iOk  = ' + str(iOk))
mask = cedLib.create_mask(wave_mark)
m_pointer = mask.ctypes.data_as(POINTER(c_uint8))
ced.S64SetMaskCodes(mask_handle, m_pointer)

data = cedLib.Spike2Data()
data.spike_times = -1 * np.ones((max_events,), dtype=np.longlong)
data = data.load_spikes(ced, fhand, spike_channel, mask_handle)
print('max spike time  = ' + str(np.max(data.spike_times)))
fs = 1.0/(ced.S64ChanDivide(fhand, spike_channel)*ced.S64GetTimeBase(fhand))
result = ced.S64Close(fhand)
open_file_count = ced.S64CloseAll()
plt.plot(data.spike_times)
plt.show(block=True)
sleep(5)
print('fhand = ' + str(fhand))
print('current sampling rate  =  ' + str(fs))
print('max tick = ' + str(max_tick))
print('file closed  = ' + str(result))
print('max spike time  = ' + str(np.max(data.spike_times)))
print('current number of open files  = ' + str(open_file_count))


# sleep(5)
# plt.plot(data.spike_times)
# plt.show()









