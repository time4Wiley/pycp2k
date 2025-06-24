from pycp2k.inputsection import InputSection


class _control2(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Beta_chunk_size = None
        self.Cyclic_block_size = None
        self.Fft_mode = None
        self.Gen_evp_solver_name = None
        self.Mpi_grid_dims = None
        self.Num_bands_to_print = None
        self.Ortho_rf = None
        self.Print_checksum = None
        self.Print_forces = None
        self.Print_hash = None
        self.Print_memory_usage = None
        self.Print_neighbors = None
        self.Print_performance = None
        self.Print_stress = None
        self.Print_timers = None
        self.Processing_unit = None
        self.Reduce_gvec = None
        self.Rmt_max = None
        self.Spglib_tolerance = None
        self.Std_evp_solver_name = None
        self.Use_second_variation = None
        self.Verbosity = None
        self.Verification = None
        self._name = "CONTROL"
        self._keywords = {'Beta_chunk_size': 'BETA_CHUNK_SIZE', 'Cyclic_block_size': 'CYCLIC_BLOCK_SIZE', 'Fft_mode': 'FFT_MODE', 'Gen_evp_solver_name': 'GEN_EVP_SOLVER_NAME', 'Mpi_grid_dims': 'MPI_GRID_DIMS', 'Num_bands_to_print': 'NUM_BANDS_TO_PRINT', 'Ortho_rf': 'ORTHO_RF', 'Print_checksum': 'PRINT_CHECKSUM', 'Print_forces': 'PRINT_FORCES', 'Print_hash': 'PRINT_HASH', 'Print_memory_usage': 'PRINT_MEMORY_USAGE', 'Print_neighbors': 'PRINT_NEIGHBORS', 'Print_performance': 'PRINT_PERFORMANCE', 'Print_stress': 'PRINT_STRESS', 'Print_timers': 'PRINT_TIMERS', 'Processing_unit': 'PROCESSING_UNIT', 'Reduce_gvec': 'REDUCE_GVEC', 'Rmt_max': 'RMT_MAX', 'Spglib_tolerance': 'SPGLIB_TOLERANCE', 'Std_evp_solver_name': 'STD_EVP_SOLVER_NAME', 'Use_second_variation': 'USE_SECOND_VARIATION', 'Verbosity': 'VERBOSITY', 'Verification': 'VERIFICATION'}

