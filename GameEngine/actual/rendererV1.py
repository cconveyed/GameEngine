import pygame
import numpy as np
from math import *
SCREENW = 1000
SCREENH = 1000
ARATIO = SCREENW/SCREENH

FOV = pi/1.3


FOVRAD = 1 / tan(FOV/2)
zfar = 1000
znear = 1
znorm = zfar / (zfar-znear)

dtheta = pi/5000

class Renderer():
    def __init__(self, all_vertices):
        self.test_points = all_vertices
        self.WIDTH, self.HEIGHT = 1000,600
        self.BLACK, self.WHITE = (0,0,0), (255,255,255)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        
        self.projection_matrix = np.array(
            ([ARATIO*FOVRAD,0,0,0],
            [0,FOVRAD,0,0],
            [0,0,znorm,1],
            [0,0,-1*znorm*znear,0])
            )

    def invert_y(self,screen_coords):
        return np.array([screen_coords[0], SCREENH - screen_coords[1]])
        
    def project(self, point):
        x,y,z,w = point
        point = np.array(([x,y,z,w]))
        return (np.matmul(point, self.projection_matrix) / w)[:2]
        # return ((point @ self.projection_matrix) / w)[:2]
        
    def run(self):
        self.running = True
        while self.running:
            pygame.event.get()
            self.screen.fill(self.BLACK)
            
            pygame.draw.line(self.screen, self.WHITE, self.project((300,300,300,1)), self.project((0,300,300,1)))
            pygame.draw.line(self.screen, self.WHITE, self.project((600,500,500,1)), self.project((800,700,1000,1)))
            pygame.draw.line(self.screen, self.WHITE, self.project((600,500,500,1)), self.project((700,700,1000,1)))
            
            
            pygame.display.flip()
        
        pygame.quit()        


game = Renderer(None)
game.run()