from GeometricObjects.geometric_object import GeometricObject
import numpy as np
import pygame
import colorsys

class Spiral(GeometricObject):
    __num_points__= 0


    def __init__(self, center,phase, num_points=1000):
        super().__init__(center, phase,num_points)
       

    
    def get_rotation_speed(self):
        return self.__rotation_speed__  
    
    def get_num_points(self):
        return self.__num_points__
    
    def draw(self,surface,t,color,rotation_speed,a,b):
        points = []
        max_theta = 6 * np.pi  # Spiral length (more = more coils)

        for i in range(self.__num_points__):
            theta = i * (max_theta / self.__num_points__)
            r = a + b * theta
            x = r * np.cos(theta + (t+self.__phase__) * rotation_speed)
            y = r * np.sin(theta + (t+ self.__phase__) * rotation_speed)
            points.append((self.__center__[0] + x, self.__center__[1] + y))

        spiralcolour = self.__color__ if self.__colourset__ else color

        if len(points) > 1:
            pygame.draw.lines(surface, spiralcolour, False, points, 2)