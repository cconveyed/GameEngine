#import necessary modules
import pygame as py
from math import *
import numpy as np


class Renderer():
    def __init__(self):
        #RGB colour identifiers
        self.BLACK, self.WHITE, self.GREEN = (0,0,0), (255,255,255), (0,255,0)
        self.ORANGE, self.NAVY = (255,165,0), (0,0,128)
        #initialises pygame
        py.init()
        #instantiate the pygame clock object
        self.clock = py.time.Clock()        
        #get information about the current computer's display
        self.display_info = py.display.Info()

        #define screen width and height in pixels, from the above
        self.SCREENW = self.display_info.current_w
        self.SCREENH = self.display_info.current_h

        #instantiate a pygame screen
        self.screen = py.display.set_mode((self.SCREENW, self.SCREENH))

        self.ARATIO = self.SCREENW/self.SCREENH
        self.theta = pi/2
        self.fov = 1/tan(self.theta/2)

        self.zfar = 1000
        self.znear = 1
        self.znorm = self.zfar / (self.zfar - self.znear)

    def project(self, point):
        x, y, z, w = point[0], point[1], point[2], 1
        point = np.array([x,y,z,w])

        self.projection_matrix = np.array(
            ([self.fov/self.ARATIO,0,0,0],
            [0,self.fov,0,0],
            [0,0,self.znorm,1],
            [0,0,-1*self.znorm*self.znear,0])
            )
        
        clip_space = point @ self.projection_matrix
        return clip_space

    #draws 3 coloured lines between 3 specified vertices packed in a tuple tri_points
    # def draw_triangle(self, tri_points, colour):
    #     py.draw.line(self.screen, colour, tri_points[0], tri_points[1])
    #     py.draw.line(self.screen, colour, tri_points[1], tri_points[2])
    #     py.draw.line(self.screen, colour, tri_points[0], tri_points[2])


    #draws 3 coloured lines between 3 specified vertices packed in a tuple tri_points
    def draw_triangle(self, tri_points, colour):
        #projects all three points and stores them in a list projected_points
        projected_points = [self.project(i) for i in tri_points]
        py.draw.line(self.screen, colour, projected_points[0], projected_points[1])
        py.draw.line(self.screen, colour, projected_points[1], projected_points[2])
        py.draw.line(self.screen, colour, projected_points[0], projected_points[2])


    def run(self):
        self.running = True
        
        test_point = self.project((180,567,3420))
        print(test_point[0], test_point[1], test_point[2], test_point[3])
        
        #event/game loop
        while self.running:
            #establishes delta-time and regulates the refresh rate of the event loop
            dt = self.clock.tick(60) / 1000
            #checks for input events
            for event in py.event.get():
                #if a user tries to terminate the window, the event loop will cease
                if event.type == py.QUIT:
                    self.running = False
            #sets the screen to black
            self.screen.fill(self.NAVY)
            #draws a orange triangle by calling self.draw_triangle      
            self.draw_triangle(((100,100,100), (1000,1000,2000), (1300,600,5)), self.ORANGE)
            
            #pygame's method of refreshing the screen 
            py.display.flip()
        #terminates the window once the event loop has ceased
        py.quit()

#instantiates the main class
engine = Renderer()
#performs the simulation
engine.run()
