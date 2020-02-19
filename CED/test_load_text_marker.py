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

text_channel = 30
mask_handle = 0

#open library
lib_path = 'C:/CEDMATLAB/CEDS64ML/x64/ceds64int.dll'
ced = cedLib.open_library(lib_path)

#open data file
fhand = ced.S64Open(file_name)

ced.S64ChanType(fhand, text_channel)
