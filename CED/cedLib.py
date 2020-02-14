from ctypes import *
import numpy as np
from time import sleep
def open_library(lib_path):

    # Load library
    ced = LibraryLoader(WinDLL).LoadLibrary(lib_path)

    # open file
    #input = [file_path]
    #output = [handle to open file]
    ced.S64Open.argtypes = [POINTER(c_char)]

    #check to see if file handle is pointed at open file
    #input = [file handle]
    #output =[ 1= handle in use, 0 =  not in use, -1 = invalid handle]
    ced.S64IsOpen.argtypes = [c_int];

    # close file
    # input = [handle to open file]
    # output = [result: 0 file sussesfully closed]
    ced.S64Close.argtypes = [c_int]

    # get max number channels
    #input = [handle to open file]
    #output = [max number of channels in this file type]
    ced.S64MaxChans.argtypes = [c_int]
    ced.S64MaxChans.argtypes = [c_int]

    #get the number pf ticks per sample CEDS64ChanDiv(fhand, data_channel)*CEDS64TimeBase(fhand));
    #input = [file handle, channel num]
    #output = [The sample interval in clock ticks]
    ced.S64ChanDivide.argtypes = [c_int, c_int]
    ced.S64ChanDivide.restype = c_longlong

    #get seconds per clock tick
    #input = [file handle]
    #output = [seconds per tick]
    ced.S64GetTimeBase.argtypes = [c_int]
    ced.S64GetTimeBase.restype = c_double




    # get channel title
    #input = [handle, channel num, string to hold chan title,
    #         nGetSize]
    #output = if nGetSize > 0, return title
    #         if nGetSize < 0, return length of title
    ced.S64GetChanTitle.argtypes = [c_int, c_int, POINTER(c_char), c_int]

    # create mask for spike extraction
    #input = [mask handle, mask mode]
    #mask mode: 0 = and ; 1 = or. We typically use 0 to restrict to a particular template
    #output = [outcome];
    # 0 = success
    ced.S64GetMaskMode.argtypes = [c_int, c_int]

    #set mask codes
    #input = [mask_handle, mask_codes]
    # output = [outcome];
    # 0 = success
    ced.S64SetMaskCodes.argtypes = [c_int, POINTER(c_int)]

    #get channel's max time
    #input = [file handle, channel number]
    #output  = [max time in ticks] (1 tick = 1 sample)
    ced.S64ChanMaxTime.argtypes = [c_int, c_int]  # (const int nFid, const int nChan);
    ced.S64ChanMaxTime.restypes = c_longlong

    #convert ticks to seconds
    #input  = [file handle, ticks]
    #output = seconds
    ced.S64TicksToSecs.argtypes = [c_int, c_longlong]
    ced.S64TicksToSecs.restypes = c_double

    #get events from a channel, including spike times
    #input  = [file_handle, channel number, pointer to spike data, max events,
    #         start tick, end tick, mask handle]
    #output = [spike times are written to the array pointed to by the 3rd input]
    ced.S64ReadEvents.argtypes = [c_int, c_int, POINTER(c_longlong), c_int, c_longlong, c_longlong, c_int]


    return ced

def create_mask(wave_mark):

    mask = np.ones((256, 4)).astype('int8')
    mask[0:wave_mark, 0] = 0
    mask[wave_mark + 1:, 0] = 0

    return mask

class Spike2Data:
    def __init__(self):
        self.spike_times = np.array([])
        self.parameters = dict([])
        self.completed_trials = dict([])
    def load_spikes(self, ced, fhand, channel, mask_handle):
        # do not know how many spikes exist before loading, so need to pick a relatively small number
        # and load until that max_events is not loaded
        max_events = 1000
        max_tick = ced.S64ChanMaxTime(fhand, channel)
        start_tick = c_longlong(0)

        # create a numpy array of the correct value type
        spike_data = -1 * np.ones((max_events,), dtype=np.longlong)
        # create a pointer to the array that will hold the spike data
        s_pointer = spike_data.ctypes.data_as(POINTER(c_longlong))

        running = True
        while running:
            events_read = ced.S64ReadEvents(fhand, channel, s_pointer, max_events, start_tick, max_tick, mask_handle)
            print('events read = ' + str(events_read))     
            # if events_read > 0:
            #     spike_data_sec = ced.S64TicksToSecs(fhand, 2);
            # else:
            #     spike_data_sec = [];
            self.spike_times = np.concatenate((self.spike_times, spike_data[0:events_read]))

            start_tick += spike_data[-1]+1

            if events_read != max_events:
                running = False



