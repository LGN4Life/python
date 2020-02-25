from ctypes import *
class S64Marker(Structure):
    _fields_ = [('m_time', c_int64),
                        ('m_Code1', c_uint8),
                        ('m_Code2', c_uint8),
                        ('m_Code3', c_uint8),
                        ('m_Code4', c_uint8)]
