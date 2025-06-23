from pycp2k.inputsection import InputSection


class _acc1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Thread_buffers = None
        self.Avoid_after_busy = None
        self.Min_flop_process = None
        self.Stack_sort = None
        self.Min_flop_sort = None
        self.Process_inhomogenous = None
        self.Binning_nbins = None
        self.Binning_binsize = None
        self._name = "ACC"
        self._keywords = {'Thread_buffers': 'THREAD_BUFFERS', 'Avoid_after_busy': 'AVOID_AFTER_BUSY', 'Min_flop_process': 'MIN_FLOP_PROCESS', 'Stack_sort': 'STACK_SORT', 'Min_flop_sort': 'MIN_FLOP_SORT', 'Process_inhomogenous': 'PROCESS_INHOMOGENOUS', 'Binning_nbins': 'BINNING_NBINS', 'Binning_binsize': 'BINNING_BINSIZE'}

