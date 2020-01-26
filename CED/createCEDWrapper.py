print("hello world")

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
print(ced_lib.S64Open.argtypes)  # this function opens .smr(x) files
file_name = b"A1_spa_000.smrx"
print(c_char_p(file_name))
result = ced_lib.S64Open(file_name)
print(result)