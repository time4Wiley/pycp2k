from pycp2k.inputsection import InputSection


class _ri_mp23(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Section_parameters = None
        self.Block_size = None
        self.Number_integration_groups = None
        self.Print_dgemm_info = None
        self._name = "RI_MP2"
        self._keywords = {'Block_size': 'BLOCK_SIZE', 'Number_integration_groups': 'NUMBER_INTEGRATION_GROUPS', 'Print_dgemm_info': 'PRINT_DGEMM_INFO'}
        self._aliases = {'Message_size': 'Block_size'}
        self._attributes = ['Section_parameters']


    @property
    def Message_size(self):
        """
        See documentation for Block_size
        """
        return self.Block_size

    @Message_size.setter
    def Message_size(self, value):
        self.Block_size = value
