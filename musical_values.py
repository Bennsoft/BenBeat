class MusicalValues:
    __bass__ = 0
    __mids__ = 0
    __treble__ = 0
    __bassmax__ = 1e-10
    __midmax__ = 1e-10
    __trebmax__ = 1e-10
    __frequency__ = 0
    __frequency_min__ = 0
    __frequency_max__ = 0
    __smoothing_alpha__ = 0.1  # Smoothing factor for frequency
    

    def __init__(self, smoothing_alpha=0.1):
        self.__smoothing_alpha__ = smoothing_alpha

    @property
    def bass(self):
        return self.__bass__/self.__bassmax__
    @bass.setter
    def bass(self, newval):
        self.__bass__ = newval
        if newval > self.__bassmax__:
            self.__bassmax__ = newval

    @property
    def mids(self):
        return self.__mids__/self.__midmax__
    @mids.setter
    def mids(self, newval):
        self.__mids__ = newval
        if newval > self.__midmax__:
            self.__midmax__ = newval

    @property
    def treble(self):
        return self.__treble__/self.__trebmax__     
    @treble.setter
    def treble(self, newval):
        self.__treble__ = newval
        if newval > self.__trebmax__:
            self.__trebmax__ = newval

    @property
    def frequency(self):
        if self.__frequency_max__ == self.__frequency_min__:
            return 0.0
        else:                                                                                                           
            # Normalize frequency to a range of 0 to 1
            # Avoid division by zero
            # Normalize to a range of 0 to 1
            return (self.__frequency__ - self.__frequency_min__)/(self.__frequency_max__ - self.__frequency_min__)
    
    @frequency.setter
    def frequency(self, newval):
        self.__frequency__ = newval
        if newval > self.__frequency_max__:
            self.__frequency_max__ = newval
        if newval < self.__frequency_min__:
            self.__frequency_min__ = newval
    
    

    
   