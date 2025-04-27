import numpy as np
class Numwave:
    __num_points__ = 0
    __max__ = 2*np.pi
    __min__ = 0
    __dots__ = None

    __funcx__ = None
    __funcy__ = None
    __anin__ = 0
    __amax__ = np.pi*2
    __bmin__ = 0
    __bmax__ = np.pi*2
    __cmin__ = 0
    __cmax__ = np.pi*2

    def __init__(self, num_points,max,funcx,funcy):
        self.__num_points__ = num_points
        self.__max__ = max
        self.__dots__ = np.linspace(0, self.__max__, self.__num_points__)
        self.__funcx__ = funcx
        self.__funcy__ = funcy

    def get_linspace(self, a, b,c):
         t = np.linspace(0, self.__max__, self.__num_points__)
         x = self.__funcx__(t, a, b, c)
         y = self.__funcy__(t, a, b, c)
         return np.stack((x, y), axis=-1)  # <== THIS returns array of (x, y) points
    
    def get_arange(self):
        return (self.__anin__,self.__amax__)

    def set_arange(self, a, b):
        self.__anin__ = a
        self.__amax__ = b

    def get_brange(self):
        return (self.__bmin__,self.__bmax__)    
    
    def set_brange(self, a, b):
        self.__bmin__ = a
        self.__bmax__ = b

    def get_crange(self):
        return (self.__cmin__,self.__cmax__)
    
    def set_crange(self, a, b):
        self.__cmin__ = a
        self.__cmax__ = b   

    def get_a(self,input):
        return self.__anin__ + (self.__amax__ - self.__anin__) * input
    
    def get_b(self,input):
        return self.__bmin__ + (self.__bmax__ - self.__bmin__) * input
    
    def get_c(self,input):
        return self.__cmin__ + (self.__cmax__ - self.__cmin__) * input      
