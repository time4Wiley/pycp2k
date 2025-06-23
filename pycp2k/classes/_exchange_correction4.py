from pycp2k.inputsection import InputSection


class _exchange_correction4(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Block_size = None
        self.Use_hfx_implementation = None
        self._name = "EXCHANGE_CORRECTION"
        self._keywords = {'Block_size': 'BLOCK_SIZE', 'Use_hfx_implementation': 'USE_HFX_IMPLEMENTATION'}
        self._attributes = ['Section_parameters']

