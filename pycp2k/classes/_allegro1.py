from pycp2k.inputsection import InputSection


class _allegro1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Atoms = None
        self.Parm_file_name = None
        self.Unit_coords = None
        self.Unit_energy = None
        self.Unit_forces = None
        self.Unit_cell = None
        self._name = "ALLEGRO"
        self._keywords = {'Atoms': 'ATOMS', 'Parm_file_name': 'PARM_FILE_NAME', 'Unit_coords': 'UNIT_COORDS', 'Unit_energy': 'UNIT_ENERGY', 'Unit_forces': 'UNIT_FORCES', 'Unit_cell': 'UNIT_CELL'}
        self._aliases = {'Parmfile': 'Parm_file_name'}


    @property
    def Parmfile(self):
        """
        See documentation for Parm_file_name
        """
        return self.Parm_file_name

    @Parmfile.setter
    def Parmfile(self, value):
        self.Parm_file_name = value
