print("hello world")

from ctypes import *
import os
import sys
import struct
print(os.getcwd())
# lib = WinDLL("C:\\Henry\\PythonProjects\\CED\\CEDS64ML\\x64\\ceds64int.dll")
LibraryLoader(WinDLL).LoadLibrary("C:\\Henry\\PythonProjects\\CED\\CEDS64ML\\x86\\ceds64int.dll")
# lib = WinDLL("C:\\CEDMATLAB\\CEDS64ML\\x64\\ceds64int.dll")