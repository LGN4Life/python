from ctypes import *
from ctypes import util
import os
import numpy as np
import struct
from matplotlib import pyplot as plt
import cedLib
file_name = b"rub_190719_con_023.smr"
spike_channel = c_int(3)
max_events = 100
wave_mark = 1
mask_handle = 1
mask_mode = 0



lib_path = 'C:/CEDMATLAB/CEDS64ML/x86/ceds64int.dll';
# ced = LibraryLoader(WinDLL).LoadLibrary(lib_path)
ced = cedLib.open_library(lib_path)
result = ced.S64IsOpen(1)
print('result  = ' + str(result))
fhand = ced.S64Open(file_name)
max_tick = ced.S64ChanMaxTime(fhand, spike_channel)

iOk = ced.S64GetMaskMode(mask_handle, mask_mode)
mask = cedLib.create_mask(wave_mark)
m_pointer = mask.ctypes.data_as(POINTER(c_int))
ced.S64SetMaskCodes(mask_handle, m_pointer)

data = cedLib.Spike2Data()

# data.load_spikes(ced, fhand, spike_channel, mask_handle)
#
# plt.plot(data.spike_times)
# plt.show()

fs = 1.0/(ced.S64ChanDivide(fhand, spike_channel)*ced.S64GetTimeBase(fhand));

result = ced.S64Close(fhand)
print(fhand)
print('sampling rate =  ' + str(fs))
print('max tick = ' + str(max_tick))
print('file closed  = ' + str(result))

