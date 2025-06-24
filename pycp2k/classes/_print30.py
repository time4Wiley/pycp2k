from pycp2k.inputsection import InputSection


class _print30(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Self_energy = None
        self._name = "PRINT"
        self._keywords = {'Self_energy': 'SELF_ENERGY'}

