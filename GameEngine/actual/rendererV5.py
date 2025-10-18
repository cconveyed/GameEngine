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



ztes = (zfar+znear)/(zfar-znear)
ztes2 = 2*zfar*znear/(zfar-znear)

clock = pygame.time.Clock()

dtheta = pi/5000

class Renderer():
    def __init__(self, all_vertices):
        self.test_points = all_vertices
        self.WIDTH, self.HEIGHT = 1000,1000
        self.BLACK, self.WHITE = (0,0,0), (255,255,255)
        pygame.init()
        self.h = pygame.display.Info()
        self.screen = pygame.display.set_mode((self.h.current_w, self.h.current_h))
        self.ARATIO = self.HEIGHT/self.WIDTH
        
        self.projection_matrix = np.array(
            ([FOVRAD/ARATIO,0,0,0],
            [0,FOVRAD,0,0],
            [0,0,znorm,1],
            [0,0,-1*znorm*znear,0])
            )
        

        self.view_matrix = None

        self.yaw, self.pitch = 0, 0
        self.u = np.array([0,1,0])
        self.camera_position = np.array([1100,1100,1100])
        self.f = np.array([0,0,0])
        
        # self.projection_matrix = np.array(
        #     ([ARATIO*FOVRAD,0,0,0],
        #     [0,FOVRAD,0,0],
        #     [0,0,ztes,1],
        #     [0,0,1*ztes2,0])
        #     )
    
    
    def rx(self, point, centre_of_rot, v, dt):
        #translates the point-to-be-rotated such that the pivot moves to the origin (via translating the PTBR by the difference between it and the pivot)
        #perform the rotation
        #translate the point-to-be-rotated back to its original location, after the rotation has been performed.
        x,y,z,w = point
        point = np.array([x,y,z,w])        
        x_centre, y_centre, z_centre, w = centre_of_rot        
        rx_matrix = np.array(
            (
                [1,0,0,0],
                [0,cos(v*dt/2),-sin(v*dt/2),0],
                [0,sin(v*dt/2),cos(v*dt/2),0],
                [0,0,0,1]
            )
        )
        T_to_origin = np.array((
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x_centre, -y_centre, -z_centre, 1]
                    ))       
        T_back = np.array((
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [x_centre, y_centre, z_centre, 1]
                    ))     

        rotation_matrix = T_to_origin @ rx_matrix @ T_back
        #order of mat operations depends on whether your point is a row or column vector
        #engineer a development mistake by reversing the order of operations and observing the weird 3d behaviour
        #@ is the new standard for matmul
        # return np.matmul(point, rotation_matrix)
        return point @ rotation_matrix



    def rz(self, point, centre_of_rot, v, dt):
        x,y,z,w = point
        point = np.array([x,y,z,w])
        x_centre, y_centre, z_centre, w = centre_of_rot
        rz_matrix = np.array(
            (
                [cos(v*dt/2),sin(v*dt/2),0,0],
                [-sin(v*dt/2),cos(v*dt/2),0,0],
                [0,0,1,0],
                [0,0,0,1]
            )
        )
        T_to_origin = np.array((
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x_centre, -y_centre, -z_centre, 1]
                    ))
        T_back = np.array((
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [x_centre, y_centre, z_centre, 1]
                    ))
            
            
        # rotation_matrix = T_to_origin.dot(rz_matrix).dot(T_back)
        rotation_matrix = T_to_origin @ rz_matrix @ T_back
        # return np.matmul(point, rotation_matrix)
        return point @ rotation_matrix


    def invert_y(self,screen_coords):
        return np.array([screen_coords[0], SCREENH - screen_coords[1]])
        
    def project(self, point):
        x,y,z,w = point
        point = np.array(([x,y,z,w]))
        cam_space = point @ self.view_matrix
        clip_space = cam_space @ self.projection_matrix
        ndc = ((clip_space) / -clip_space[3])[:2]
        new = np.array([SCREENW*(ndc[0]+1)/2, SCREENH*(1-ndc[1])/2])
        return new

    def draw_triangle(self, tri_points):
        projected_points = [self.project(i) for i in tri_points]
        pygame.draw.line(self.screen, self.WHITE, projected_points[0], projected_points[1])
        pygame.draw.line(self.screen, self.WHITE, projected_points[1], projected_points[2])
        pygame.draw.line(self.screen, self.WHITE, projected_points[0], projected_points[2])
        
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


    def update_yaw_pitch(self, dx, dy):
        self.yaw -= dx * 0.002
        self.pitch -= dy * 0.002
        
        if self.pitch > 80/360 * 2 * pi:
            self.pitch = 80/360 * 2 * pi
        if self.pitch < -80/360 * 2 * pi:
            self.pitch = -80/360 * 2 * pi

    def run(self):
        self.running = True
        
        self.rotation_point = (1500,1500,1500,1)
        x0, y0 = 50, 50

        while self.running:
            dt = clock.tick(60) / 1000
    
            self.update_view()
            self.rotated_points = [self.rx(self.rz(i, self.rotation_point, 2, dt), self.rotation_point, 2, dt) for i in self.test_points]
            self.test_points = self.rotated_points
            pygame.event.get()
            self.screen.fill(self.BLACK)
            
            
            self.draw_triangle([self.test_points[0],self.test_points[1],self.test_points[4]])
            self.draw_triangle([self.test_points[4], self.test_points[1], self.test_points[5]])
            
            self.draw_triangle([self.test_points[0],self.test_points[1],self.test_points[2]])
            self.draw_triangle([self.test_points[0], self.test_points[2], self.test_points[4]])
            
            self.draw_triangle([self.test_points[4],self.test_points[5],self.test_points[6]])
            self.draw_triangle([self.test_points[5], self.test_points[6], self.test_points[7]])
            
            self.draw_triangle([self.test_points[2],self.test_points[3],self.test_points[6]])
            self.draw_triangle([self.test_points[6], self.test_points[3], self.test_points[7]])
            
            self.draw_triangle([self.test_points[0],self.test_points[2],self.test_points[4]])
            self.draw_triangle([self.test_points[2], self.test_points[4], self.test_points[6]])
            
            self.draw_triangle([self.test_points[1],self.test_points[3],self.test_points[5]])
            self.draw_triangle([self.test_points[1], self.test_points[5], self.test_points[7]])



            self.keys = pygame.key.get_pressed()
            if self.keys[pygame.K_w]:
                self.camera_position = self.camera_position + 10
            if self.keys[pygame.K_a]:
                self.camera_position = self.camera_position + (1000 * self.r * dt)
            if self.keys[pygame.K_d]:
                self.camera_position = self.camera_position - (1000 * self.r * dt)
            if self.keys[pygame.K_s]:
                self.camera_position = self.camera_position - 10
            x1, y1 = pygame.mouse.get_pos()
            dx, dy = x1 - x0, y1 - y0
            x0, y0 = x1, y1
            self.update_yaw_pitch(dx, dy)
            
            
            # pygame.draw.line(self.screen, self.WHITE, self.project(self.rotation_point), self.project(self.test_points[2]))
            # pygame.draw.line(self.screen, self.WHITE, self.project((300,300,300,1)), self.project((0,300,300,1)))
            # pygame.draw.line(self.screen, self.WHITE, self.project((600,500,500,1)), self.project((800,700,1000,1)))
            # pygame.draw.line(self.screen, self.WHITE, self.project((600,500,500,1)), self.project((700,700,1000,1)))
            
            
            pygame.display.flip()
        
        pygame.quit()        


cube = [
(1300,1300,1300,1),
(1300,1300,1700,1),
(1300,1700,1300,1),
(1300,1700,1700,1),
(1700,1300,1300,1),
(1700,1300,1700,1),
(1700,1700,1300,1),
(1700,1700,1700,1)]


game = Renderer(cube)
game.run()