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
    
    
    def rx(self, point, centre_of_rot):
        #translates the point-to-be-rotated such that the pivot moves to the origin (via translating the PTBR by the difference between it and the pivot)
        #perform the rotation
        #translate the point-to-be-rotated back to its original location, after the rotation has been performed.
        x,y,z,w = point
        point = np.array([x,y,z,w])        
        x_centre, y_centre, z_centre, w = centre_of_rot        
        rx_matrix = np.array(
            (
                [1,0,0,0],
                [0,cos(dtheta/2),-sin(dtheta/2),0],
                [0,sin(dtheta/2),cos(dtheta/2),0],
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
            
        rotation_matrix = T_to_origin.dot(rx_matrix).dot(T_back)
        #change made here. .dot() will do matmul if the matrices are 2d and higher, but will do dot product if matrices are 1d      
        rotation_matrix = T_to_origin @ rx_matrix @ T_back
        #order of mat operations depends on whether your point is a row or column vector
        #engineer a development mistake by reversing the order of operations and observing the weird 3d behaviour
        #@ is the new standard for matmul
        return np.matmul(point, rotation_matrix)

    def rz(self, point, centre_of_rot):
        x,y,z,w = point
        point = np.array([x,y,z,w])
        x_centre, y_centre, z_centre, w = centre_of_rot
        rz_matrix = np.array(
            (
                [cos(dtheta/2),sin(dtheta/2),0,0],
                [-sin(dtheta/2),cos(dtheta/2),0,0],
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
            
            
        rotation_matrix = T_to_origin.dot(rz_matrix).dot(T_back)
        return np.matmul(point, rotation_matrix)

    def invert_y(self,screen_coords):
        return np.array([screen_coords[0], SCREENH - screen_coords[1]])
        
    def project(self, point):
        x,y,z,w = point
        point = np.array(([x,y,z,w]))
        return (np.matmul(point, self.projection_matrix) / w)[:2]

    def draw_triangle(self, tri_points):
        projected_points = [self.project(i) for i in tri_points]
        pygame.draw.line(self.screen, self.WHITE, projected_points[0], projected_points[1])
        pygame.draw.line(self.screen, self.WHITE, projected_points[1], projected_points[2])
        pygame.draw.line(self.screen, self.WHITE, projected_points[0], projected_points[2])
        
    
    def run(self):
        self.running = True
        
        self.rotation_point = (700,700,700,1)
        while self.running:
            # self.rotated_points = [self.rx(self.rz(i, self.rotation_point), self.rotation_point) for i in self.test_points]
            
            x_centre, y_centre, z_centre, w = self.rotation_point      
            rx_matrix = np.array(
                (
                    [1,0,0,0],
                    [0,cos(dtheta/2),-sin(dtheta/2),0],
                    [0,sin(dtheta/2),cos(dtheta/2),0],
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
                
            rotation_matrix = T_to_origin.dot(rx_matrix).dot(T_back)
            #change made here. .dot() will do matmul if the matrices are 2d and higher, but will do dot product if matrices are 1d      
            rotation_matrix = T_to_origin @ rx_matrix @ T_back
            
            
            self.rotated_points = np.array(self.test_points) @ rotation_matrix
            self.test_points = self.rotated_points
            pygame.event.get()
            self.screen.fill(self.BLACK)
            
            
            # self.draw_triangle([self.test_points[0],self.test_points[1],self.test_points[4]])
            # self.draw_triangle([self.test_points[4], self.test_points[1], self.test_points[5]])
            
            # self.draw_triangle([self.test_points[0],self.test_points[1],self.test_points[2]])
            # self.draw_triangle([self.test_points[0], self.test_points[2], self.test_points[4]])
            
            # self.draw_triangle([self.test_points[4],self.test_points[5],self.test_points[6]])
            # self.draw_triangle([self.test_points[5], self.test_points[6], self.test_points[7]])
            
            # self.draw_triangle([self.test_points[2],self.test_points[3],self.test_points[6]])
            # self.draw_triangle([self.test_points[6], self.test_points[3], self.test_points[7]])
            
            # self.draw_triangle([self.test_points[0],self.test_points[2],self.test_points[4]])
            # self.draw_triangle([self.test_points[2], self.test_points[4], self.test_points[6]])
            
            # self.draw_triangle([self.test_points[1],self.test_points[3],self.test_points[5]])
            # self.draw_triangle([self.test_points[1], self.test_points[5], self.test_points[7]])
            
            for (i0, i1, i2) in f:
                self.draw_triangle([
                    self.test_points[i0],
                    self.test_points[i1],
                    self.test_points[i2]
                ])
        
            
            
            pygame.display.flip()
        
        pygame.quit()        


cube = [
(1300,1300,1300,1),
(1300,1300,1400,1),
(1300,1400,1300,1),
(1300,1400,1400,1),
(1400,1300,1300,1),
(1400,1300,1400,1),
(1400,1400,1300,1),
(1400,1400,1400,1)]




def make_torus(R=200, r=80, num_major=24, num_minor=16):
    points = []
    # 1) Generate points
    for i in range(num_major):
        theta = 2*pi * i / num_major
        cos_t, sin_t = cos(theta), sin(theta)
        # center of this tube circle:
        cx, cz = R * cos_t, R * sin_t + 500
        for j in range(num_minor):
            phi = 2*pi * j / num_minor
            cos_p, sin_p = cos(phi), sin(phi)
            # point on tube circle, offset from ring center
            x = (R + r * cos_p) * cos_t + 500
            y = r * sin_p + 500
            z = (R + r * cos_p) * sin_t + 500
            points.append((x, y, z, 1))

    # 2) Build faces (two triangles per quad)
    faces = []
    for i in range(num_major):
        for j in range(num_minor):
            # index helpers with wrap‑around
            i_next = (i+1) % num_major
            j_next = (j+1) % num_minor

            # the four corners of this quad
            a = i * num_minor + j
            b = i_next * num_minor + j
            c = i * num_minor + j_next
            d = i_next * num_minor + j_next

            # two triangles: (a,b,c) and (b,d,c)
            faces.append((a, b, c))
            faces.append((b, d, c))

    return points, faces

p, f = make_torus(
    R=200, r=80,
    num_major=32,  # more segments → smoother
    num_minor=16
)

# In your draw routine, replace all those cube-triangle calls with:




game = Renderer(p)
game.run()