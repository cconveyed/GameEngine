#import necessary modules
import pygame as py
from math import *
import numpy as np

#The primary class that contains all of the functionality of the 3D space engine
class Renderer():
    def __init__(self, model):
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

        #class attribute for the model argument
        self.model = model

        #retrieves the list of vertices and triangles from the model

        #an offset vector is added to each vertex of the shape
        self.vertices = [i + np.array([100,50,100]) for i in self.model[0]]
        print(self.vertices)
        self.triangles = self.model[1]


        self.view_matrix = None
        self.yaw, self.pitch = 0, 0
        self.u = np.array([0,1,0])
        self.camera_position = np.array([1100,1100,1100])

    def project(self, point):
        x, y, z, w = point[0], point[1], point[2], 1
        point = np.array([x,y,z,w])

        self.projection_matrix = np.array(
            ([self.fov/self.ARATIO,0,0,0],
            [0,self.fov,0,0],
            [0,0,self.znorm,1],
            [0,0,-1*self.znorm*self.znear,0])
            )
        #camera space --> clip space
        clip_space = point @ self.projection_matrix
        #clip space --> ndc space
        ndc_space = clip_space / z
        #ndc space --> screen space
        screen_space = ndc_space[0]*self.SCREENW, ndc_space[1]*self.SCREENH
        screen_space = np.array([self.SCREENW*(ndc_space[0]+1)/2, self.SCREENH*(1-ndc_space[1])/2])
        return screen_space

    def update_view(self):
        self.fx = sin(self.yaw) * cos(self.pitch)
        self.fy = sin(self.pitch)
        self.fz = cos(self.yaw) * cos(self.pitch)

        self.f = np.array([self.fx, self.fy, self.fz]) / np.linalg.norm(np.array([self.fx, self.fy, self.fz]))
        self.r = np.cross(self.f, self.u) / np.linalg.norm(np.cross(self.f, self.u))
        self.u = np.cross(self.r, self.f) / np.linalg.norm(np.cross(self.r, self.f))
        self.c = self.camera_position 

        self.view_matrix = np.array(
            ([self.r[0],self.u[0],self.f[0],0],
            [self.r[1],self.u[1],self.f[1],0],
            [self.r[2],self.u[2],self.f[2],0],
            [-np.dot(self.r, self.c), -np.dot(self.u, self.c), -np.dot(self.f, self.c), 1]))

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
        
        test_point = [56,100,75, 1]
        self.update_view()
        print(self.view_matrix)
        print(test_point @ self.view_matrix)


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
            
            #draws an orange triangle that mostly occupies the z-plane     
            # self.draw_triangle(((100,100,100), (600,110,140000), (1100,100,5)), self.ORANGE)
            self.draw_triangle(((200,300,500), (100,300,500), (200,100,500)), self.ORANGE)

            #Runs a loop that draws every triangle that constitutes the shape/model
            # for tri in self.triangles:
            #     self.draw_triangle((self.vertices[tri[0]], self.vertices[tri[1]], self.vertices[tri[2]]), self.ORANGE)
            
            #pygame's method of refreshing the screen 
            py.display.flip()
        #terminates the window once the event loop has ceased
        py.quit()


#list containing information about a shape
#at the moment, this information consists of vertices and triangles 
cube = [[np.array([0,0,0]),  #relative x,y,z vertices in world-space
        np.array([0,0,10]), 
        np.array([0,10,0]), 
        np.array([0,10,10]),
        np.array([10,0,0]),
        np.array([10,0,10]),
        np.array([10,10,0]),
        np.array([10,10,10])],

       [[0,2,6],   #triangle information consisting of above vertex indices
        [0,6,4],
        [1,5,7],
        [1,7,3],
        [0,1,3],
        [0,3,2],
        [4,6,7],
        [4,7,5],
        [2,3,7],
        [2,7,6],
        [0,4,5],
        [0,5,1]]]

#instantiates the main class
engine = Renderer(cube)
#performs the simulation
engine.run()


