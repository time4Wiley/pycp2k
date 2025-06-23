from pycp2k.inputsection import InputSection


class _deepmd1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Atoms = None
        self.Pot_file_name = None
        self.Atoms_deepmd_type = None
        self._name = "DEEPMD"
        self._keywords = {'Atoms': 'ATOMS', 'Pot_file_name': 'POT_FILE_NAME', 'Atoms_deepmd_type': 'ATOMS_DEEPMD_TYPE'}
        self._aliases = {'Parmfile': 'Pot_file_name'}


    @property
    def Parmfile(self):
        """
        See documentation for Pot_file_name
        """
        return self.Pot_file_name

    @Parmfile.setter
    def Parmfile(self, value):
        self.Pot_file_name = value
