import numpy as np

class Waveform:
    __waveforms__ = {}
        
    def __init__(self, num_points):
        self.__dots__ = np.linspace(0, 2 * np.pi, num_points)
        base_waveform = np.array([
            [np.sin(7 * t), np.cos(5 * t + np.pi / 2)]
            for t in self.__dots__ 
        ])  
        self.__waveforms__['celtic1'] = base_waveform

        base_waveform = np.array([
           [np.sin(3 * t)*np.cos(2*t+np.pi/3), np.cos(4 * t)]
          for t in self.__dots__
        ])
        self.__waveforms__['butterfly'] = base_waveform

        twisted_rose = np.array([
        [np.sin(4 * t) * np.sin(t)**2, np.cos(6 * t + np.pi / 4) * np.cos(t)**2]
            for t in self.__dots__
        ])
        self.__waveforms__['twistedrose'] = twisted_rose

        ellipse = np.array([
            [np.sin(2*t), np.cos(t)]
            for t in self.__dots__
        ])
        self.__waveforms__['ellipse'] = ellipse

        Waveform = np.array([
            [np.sin(5*t) - np.cos(2*t+np.pi), np.cos(t)+np.sin(3*t+np.pi/4)]
            for t in self.__dots__
        ])
        self.__waveforms__['squiggle'] = Waveform

        Waveform = np.array([
            [t/3*(np.cos(t) + np.sin(2*t+np.pi/4))
             ,t/3*(np.cos(2*t+np.pi/4) + np.sin(t))]
            for t in self.__dots__
        ])
        self.__waveforms__['knot'] = Waveform
        R=5
        r=3
        d=5
        Waveform = np.array([
            [(R-r)*np.cos(t)+d*np.cos(R-r)/r*t,
             (R-r)*np.sin(t)-d*np.sin(R-r)/r*t]   
            for t in self.__dots__        

        ])
        self.__waveforms__['hypotrochoid'] = Waveform

        Waveform = np.array([
            [t*np.cos(7*t),t*np.sin(7*t)]
            for t in self.__dots__
        ])
        self.__waveforms__['spiral'] = Waveform
    

    def get_waveform(self, name):
        if name in self.__waveforms__:
            return self.__waveforms__[name]
        else:
            raise ValueError(f"Waveform '{name}' not found. Available waveforms: {list(self.__waveforms__.keys())}")

    def get_waveform_by_index(self,i:int):   
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