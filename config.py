class Config:
    __points_num__ = 720
    __smoothing_alpha__ = 0.09
    __radius__ = 200
    __thickness__ = 10
    __radband__ = 20
    __thickband__ = 10
    __spins__ = 2

    @property
    def points_num(self):
        return self.__points_num__
    
    @points_num.setter
    def points_num(self, newval):
        self.__points_num__ = newval

    @property
    def smoothing_alpha(self):
        return self.__smoothing_alpha__ 

    @smoothing_alpha.setter
    def smoothing_alpha(self, newval):
        self.__smoothing_alpha__ = newval
     
    @property
    def spins(self):
        return self.__spins__
    
    @spins.setter
    def spins(self, newval):
        self.__spins__ = newval

    @property
    def radius(self):
        return self.__radius__  
    
    @radius.setter
    def radius(self, newval):
        self.__radius__ = newval

    @property
    def thickness(self):
        return self.__thickness__  
     
    @thickness.setter
    def thickness(self, newval):
        self.__thickness__ = newval

    @property
    def radband(self):
        return self.__radband__
    
    @radband.setter
    def radband(self, newval):
        self.__radband__ = newval

    @property
    def thickband(self):
        return self.__thickband__
    
    @thickband.setter
    def thickband(self, newval):
        self.__thickband__ = newval