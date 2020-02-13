
from ctypes import *
import os
import numpy as np
# import

print(os.getcwd())
# lib = WinDLL("C:\\Henry\\PythonProjects\\CED\\CEDS64ML\\x64\\ceds64int.dll")
ced_lib = LibraryLoader(WinDLL).LoadLibrary("C:\\Henry\\PythonProjects\\CED\\CEDS64ML\\x86\\ceds64int.dll")


# s = "Hello, World"
# c_s = c_char_p(s)
print(ced_lib)

ced_lib.S64Open.argtypes = [POINTER(c_char)]
ced_lib.S64Close.argtypes = [c_int]

file_name = b"rub_190719_con_023.smr"

fhand = ced_lib.S64Open(file_name)
ced_lib.S64MaxChans.argtypes = [c_int]
new_title = b"place holder"


#set the input types for each function
ced_lib.S64SetChanTitle.argtypes = [c_int, c_int, POINTER(c_char)]
chan_num = 1
chan_buffer = ced_lib.S64GetChanTitle(fhand, chan_num, new_title, -1)
arr = bytes(chan_buffer)

get_title_result = ced_lib.S64GetChanTitle(fhand, chan_num, arr, chan_buffer)


current_title = arr.decode("utf-8")
print('channel title is  = ' + current_title)


# load spike times
# set mask mode
wave_mark = 1
mask_handle = 1
ced_lib.S64GetMaskMode.argtypes = [c_int, c_int]

iOk = ced_lib.S64GetMaskMode(mask_handle,0)

print('mask mode attempt   = ' + str(iOk))
mask = np.ones((256, 4)).astype('int8')
# mask = np.ones((256, 4))

mask[0:wave_mark, 0] = 0
mask[wave_mark+1:, 0] = 0

mask = mask.ctypes.data_as(POINTER(c_int))
ced_lib.S64SetMaskCodes.argtypes = [c_int, POINTER(c_int)]
ced_lib.S64SetMaskCodes(mask_handle, mask)

spike_channel = 3

ced_lib.S64ChanMaxTime.argtypes =[c_int, c_int]        #(const int nFid, const int nChan);
max_spike_tick = ced_lib.S64ChanMaxTime(fhand, spike_channel)
print('max spike tick  = ' + str(max_spike_tick))
max_events = 100


#create a numpy array of the correct value type
spike_data = -1*np.ones((max_events,), dtype=np.longlong)

#create a pointer to the array that will hold the spike data
s_pointer = spike_data.ctypes.data_as(POINTER(c_longlong))
# spike_data = c_longlong(10)
# s_pointer = pointer(spike_data)
ced_lib.S64ReadEvents.argtypes = [c_int, c_int, POINTER(c_longlong), c_int, c_longlong, c_longlong, c_int]


start_tick = c_longlong(0) #need to convert make sure these are in terms of ticks (i.e., samples)
#if the sampling rate is 30000, then 1 sec is = to 30000 ticks
end_tick = c_longlong(30000) #should be able to set this to -1, which means go to end of file
# start_tick = start_tick.ctypes.data_as(POINTER(c_longlong))
# end_tick = np.array([300000], dtype=np.longlong)
# end_tick = end_tick.ctypes.data_as(POINTER(c_longlong))
print('load spike times')
print('mask handle  =' + str(mask_handle))
ced_lib.S64ReadEvents(fhand, spike_channel, s_pointer, max_events, start_tick, end_tick, mask_handle)
# print(str(spike_data.data))
print('max events = ' + str(max_events))
print('start tick  = ' + str(start_tick))
print('end tick = ' + str(end_tick))
print('spike times loaded')
print('s_pointer = ' + str(s_pointer.contents))
print('fhand  =  ' + str(fhand))
print(np.max(spike_data))
result = ced_lib.S64Close(fhand)
print(result)



