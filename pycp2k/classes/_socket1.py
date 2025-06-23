from pycp2k.inputsection import InputSection


class _socket1(InputSection):
    def __init__(self):
        InputSection.__init__(self)
        self.Inet = None
        self.Port = None
        self.Host = None
        self._name = "SOCKET"
        self._keywords = {'Inet': 'INET', 'Port': 'PORT', 'Host': 'HOST'}

