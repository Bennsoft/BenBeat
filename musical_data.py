import numpy as np
class musicalData:

    __volume__ = 0.0
    __fft_magnitude__ = 0
    __dominant_index__ = 0


    def __init__(self,blocksise):
        self.__fft_magnitude__ = np.zeros(blocksise // 2)

    @property
    def fft_magnitude(self):
        return self.__fft_magnitude__
    
    @fft_magnitude.setter
    def fft_magnitude(self,newval):
        self.__fft_magnitude__ = newval

    @property
    def volume(self):
        return self.__volume__
    
    @volume.setter
    def volume(self,newval):
        self.__volume__ = newval

    @property
    def dominant_index(self):
        return self.__dominant_index__
    
    @dominant_index.setter
    def dominant_index(self,newval):
        self.__dominant_index__ = newval

    
    
