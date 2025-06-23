from pycp2k.inputsection import InputSection


class _bs_subsystemsboundaries1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Default_keyword = []
        self._name = "BS.SUBSYSTEMSBOUNDARIES"
        self._repeated_default_keywords = {'Default_keyword': 'DEFAULT_KEYWORD'}
        self._attributes = ['Default_keyword']

