import numpy as np

class Waveform:
    __waveforms__ = {}
        
    def __init__(self, num_points):
        self.__dots__ = np.linspace(0, 2 * np.pi, num_points)
        base_waveform = np.array([
            [np.sin(7 * t), np.cos(5 * t + np.pi / 2)]
            for t in self.__dots__ 
        ])  
        self.__waveforms__['Celtic1'] = base_waveform

        base_waveform = np.array([
           [np.sin(3 * t)*np.cos(2*t+np.pi/3), np.cos(4 * t)]
          for t in self.__dots__
        ])
        self.__waveforms__['butterfly'] = base_waveform

        base_waveform = np.array([
            [np.sin(7 * t)**2, np.cos(11 * t + np.pi / 2)**2]
            for t in self.__dots__
        ])
        self.__waveforms__['Celtic2'] = base_waveform

    def get_waveform(self, name):
        if name in self.__waveforms__:
            return self.__waveforms__[name]
        else:
            raise ValueError(f"Waveform '{name}' not found. Available waveforms: {list(self.__waveforms__.keys())}")

    def get_waveform(self,i):   
        if i in self.__waveforms__:
            return self.__waveforms__[i]
        else:
            raise ValueError(f"Waveform '{i}' not found. Available waveforms: {list(self.__waveforms__.keys())}")
        
    def get_waveformCount(self):
        return len(self.__waveforms__)