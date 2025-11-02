#import necessary modules
import pygame as py
from math import *
import numpy as np


class Renderer():
    def __init__(self):
        #RGB colour identifiers
        self.BLACK, self.WHITE = (0,0,0), (255,255,255)
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




    def run(self):
        self.running = True
        #event/game loop
        while self.running:
            #establishes delta-time and regulates the refresh rate of the event loop
            dt = self.clock.tick(60) / 1000

            py.draw.line(self.screen, self.WHITE, projected_points[0], projected_points[1])

            #checks for input events
            for event in py.event.get():
                #if a user tries to terminate the window, the event loop will cease
                if event.type == py.QUIT:
                    self.running = False

            #sets the screen to black
            self.screen.fill(self.BLACK)
            #pygame's method of refreshing the screen 
            py.display.flip()
        #terminates the window once the event loop has ceased
        py.quit()

#instantiates the main class
engine = Renderer()
#performs the simulation
engine.run()
