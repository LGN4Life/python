
from ctypes import *
import os
import sys
import struct
print(os.getcwd())
# lib = WinDLL("C:\\Henry\\PythonProjects\\CED\\CEDS64ML\\x64\\ceds64int.dll")
ced_lib = LibraryLoader(WinDLL).LoadLibrary("C:\\Henry\\PythonProjects\\CED\\CEDS64ML\\x86\\ceds64int.dll")

print(type(ced_lib))
# s = "Hello, World"
# c_s = c_char_p(s)
print(ced_lib)
print(ced_lib.S64Open.argtypes)  # this function opens .smr(x) files
ced_lib.S64Open.argtypes = [POINTER(c_char)]
ced_lib.S64Close.argtypes = [c_int]
print(ced_lib.S64Open.argtypes)  # this function opens .smr(x) files
file_name = b"rub_190719_con_023.smr"
print(c_char_p(file_name))
fhand = ced_lib.S64Open(file_name)
ced_lib.S64MaxChans.argtypes = [c_int]
new_title = b"place holder"

print('process start')
ced_lib.S64SetChanTitle.argtypes = [c_int, c_int,POINTER(c_char)]
chan_num = 25
chan_buffer = ced_lib.S64GetChanTitle(fhand, chan_num, new_title, -1)
arr = bytes(chan_buffer)
print('arr  = ' + str(arr))
print('type arr is ' + (str(type(arr))))
print('type new_title is ' + (str(type(new_title))))
get_title_result = ced_lib.S64GetChanTitle(fhand, chan_num, arr, chan_buffer)
print('process finished')
print("result of SetChan title  = " + str(arr))
print("get_title_result = " + str(get_title_result))

current_title = arr.decode("utf-8")
print('new string  = ' + current_title)
result = ced_lib.S64Close(fhand)


