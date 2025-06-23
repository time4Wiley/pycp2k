from pycp2k.inputsection import InputSection


class _sr_cutoff1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Element = None
        self.Radius = None
        self._name = "SR_CUTOFF"
        self._keywords = {'Element': 'ELEMENT', 'Radius': 'RADIUS'}

