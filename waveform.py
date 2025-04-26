import numpy as np
from numwave import Numwave
class Waveform:
    __waveforms__ = {}
        
    def __init__(self, num_points):
        self.__num_points__ = num_points
       # self.__waveforms__['sine'] = Numwave(self.__num_points__, 2 * np.pi, np.sin).get_linspace(0, 1, 0)
        #self.__waveforms__['square'] = Numwave(self.__num_points__, 2 * np.pi, np.sign).get_linspace(0, 1, 0)
        #self.__waveforms__['sawtooth'] = Numwave(self.__num_points__, 2 * np.pi, lambda x: (x / np.pi) - 1).get_linspace(0, 1, 0)
        #self.__waveforms__['triangle'] = Numwave(self.__num_points__, 2 * np.pi, lambda x: (2 / np.pi) * np.arcsin(np.sin(x))).get_linspace(0, 1, 0)
        
        spiral = Numwave(self.__num_points__, 2 * np.pi, lambda t,a,b,c: t*np.sin(a*t+b), lambda t,a,b,c: t*np.cos(a*t+c))
        spiral.set_arange(0, 10)
        spiral.set_brange(-np.pi/2,np.pi/2)
        spiral.set_crange(-np.pi/2,np.pi/2)
        self.__waveforms__['spiral'] = spiral
        lissajous = Numwave(self.__num_points__, 2 * np.pi, lambda t,a,b,c: a*np.sin(b*t+c), lambda t,a,b,c: a*np.sin(b*t))
        lissajous.set_arange(1, 10)
        lissajous.set_brange(1,10)
        lissajous.set_crange(-np.pi/2,np.pi/2)
        self.__waveforms__['lissajous'] = lissajous

      

    def get_waveform(self, name):
        if name in self.__waveforms__:
            return self.__waveforms__[name]
        else:
            raise ValueError(f"Waveform '{name}' not found. Available waveforms: {list(self.__waveforms__.keys())}")

    def get_waveform_by_index(self,i:int)->Numwave:  
        tick =0
        retform = None
        for w in self.__waveforms__:
            if i == tick:
               retform= self.__waveforms__[w]
               break
            else:
                tick += 1
        return retform
    
    def get_waveform_name(self,i:int):   
        tick =0
        retform = None
        for w in self.__waveforms__:
            if i == tick:
               retform= w
               break
            else:
                tick += 1
        return retform
    
    def get_waveform_blend(self, name1:str, name2:str,blend:float):
          if name1 in self.__waveforms__ and name2 in self.__waveforms__:
                waveform1 = self.__waveforms__[name1]
                waveform2 = self.__waveforms__[name2]
                if len(waveform1) == len(waveform2):
                    blended_waveform = (1 - blend) * waveform1 + blend * waveform2
                    return blended_waveform
                else:
                    raise ValueError(f"Waveforms '{name1}' and '{name2}' must have the same length for blending.")
          else:
                raise ValueError(f"Waveform '{name1}' or '{name2}' not found. Available waveforms: {list(self.__waveforms__.keys())}")
    
        
    def get_waveformCount(self):
        return len(self.__waveforms__)