import numpy as np
class Numwave:
    __num_points__ = 0
    __max__ = 2*np.pi
    __min__ = 0
    __dots__ = None

    __funcx__ = None
    __funcy__ = None

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