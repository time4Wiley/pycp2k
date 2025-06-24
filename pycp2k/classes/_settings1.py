from pycp2k.inputsection import InputSection


class _settings1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Always_update_wf = None
        self.Auto_enu_tol = None
        self.Fft_grid_size = None
        self.Fp32_to_fp64_rms = None
        self.Itsol_tol_min = None
        self.Itsol_tol_ratio = None
        self.Itsol_tol_scale = None
        self.Min_occupancy = None
        self.Mixer_rms_min = None
        self.Nprii_aug = None
        self.Nprii_beta = None
        self.Nprii_rho_core = None
        self.Nprii_vloc = None
        self.Radial_grid = None
        self.Sht_coverage = None
        self._name = "SETTINGS"
        self._keywords = {'Always_update_wf': 'ALWAYS_UPDATE_WF', 'Auto_enu_tol': 'AUTO_ENU_TOL', 'Fft_grid_size': 'FFT_GRID_SIZE', 'Fp32_to_fp64_rms': 'FP32_TO_FP64_RMS', 'Itsol_tol_min': 'ITSOL_TOL_MIN', 'Itsol_tol_ratio': 'ITSOL_TOL_RATIO', 'Itsol_tol_scale': 'ITSOL_TOL_SCALE', 'Min_occupancy': 'MIN_OCCUPANCY', 'Mixer_rms_min': 'MIXER_RMS_MIN', 'Nprii_aug': 'NPRII_AUG', 'Nprii_beta': 'NPRII_BETA', 'Nprii_rho_core': 'NPRII_RHO_CORE', 'Nprii_vloc': 'NPRII_VLOC', 'Radial_grid': 'RADIAL_GRID', 'Sht_coverage': 'SHT_COVERAGE'}

