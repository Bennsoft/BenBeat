from abc import ABC, abstractmethod

class GeometricObject(ABC):
    __center__ = (0, 0)  
    __phase__ = 0
    __colour__ = (0, 0, 0)  # Default color (black)
    __colourset__ = False
    __num_points__= 0


    def __init__(self, center,p,num_points=1000):
        self.__num_points__ = num_points
        self.__center__ = center
        self.__phase__ = p

    def get_center(self):
        return self.__center__

    def get_color(self):
        return self.__color__
    
    def get_num_points(self):
        return self.__num_points__
    
    def set_color(self, color):
        self.__color__ = color
        __colourset__ = True


    def get_colourset(self):
        return self.__colourset__
    
    def get_phase(self):
        return self.__phase__
    


    