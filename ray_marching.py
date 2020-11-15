from math import *
import numpy as np
import matplotlib.pyplot as plt

class Box:
    def __init__(self, pos_x, pos_y, width, height):
        self.pos_x  = pos_x
        self.pos_y  = pos_y
        self.width  = width
        self.height = height
    def dist_to_point(self, point):
        tmp_offset  = ( abs(point[0] - (self.pos_x + self.width/2)) - self.width/2, 
                        abs(point[1] - (self.pos_y + self.height/2)) - self.height/2)
        tmp_outside = sqrt(max(tmp_offset[0], 0)**2 + max(tmp_offset[1], 0)**2)
        tmp_inside  = max(min(tmp_offset[0], 0), min(tmp_offset[1], 0))
        tmp_dist = tmp_outside + tmp_inside
        return tmp_dist
    def dist_to_obj(self, obj):
        tmp_offset  = ( abs(obj.pos_x - (self.pos_x + self.width/2)) - self.width/2, 
                        abs(obj.pos_y - (self.pos_y + self.height/2)) - self.height/2)
        tmp_outside = sqrt(max(tmp_offset[0], 0)**2 + max(tmp_offset[1], 0)**2)
        tmp_inside  = max(min(tmp_offset[0], 0), min(tmp_offset[1], 0))
        tmp_dist = tmp_outside + tmp_inside
        return tmp_dist
    def draw(self, ax):
        tmp_shape = plt.Rectangle((self.pos_x, self.pos_y), self.width, self.height, edgecolor="k", facecolor="None")
        ax.add_patch(tmp_shape)
        ax.update_datalim(((self.pos_x, self.pos_y), (self.pos_x+self.width, self.pos_y+self.height)))
        self.shape = tmp_shape

class Circle:
    def __init__(self, pos_x, pos_y, radius):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
    def dist_to_point(self, point):
        tmp_dist = np.sqrt((point[0] - self.pos_x)**2 + (point[1] - self.pos_y)**2) - self.radius
        return tmp_dist
    def dist_to_obj(self, obj):
        tmp_dist = np.sqrt((obj.pos_x - self.pos_x)**2 + (obj.pos_y - self.pos_y)**2) - self.radius
        return tmp_dist
    def draw(self, ax):
        tmp_shape = plt.Circle((self.pos_x, self.pos_y), self.radius, edgecolor="k", facecolor="None")
        ax.add_patch(tmp_shape)
        ax.update_datalim(((self.pos_x-self.radius, self.pos_y-self.radius), (self.pos_x+self.radius, self.pos_y+self.radius)))
        self.shape = tmp_shape

class Camera:
    def __init__(self, pos_x, pos_y, ray_L, ray_ang_range, ray_count):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = 1/8
        self.ray_L = ray_L # not necessary
        self.ray_ang_range = ray_ang_range
        self.ray_count = ray_count
    def draw_rays(self, ax, objs, max_iter):
        ray_angs = np.linspace(self.ray_ang_range[0], self.ray_ang_range[1], self.ray_count)
        for ang in ray_angs:
            tmp_iter = 0
            ray_x = self.pos_x
            ray_y = self.pos_y
            tot_L = 0
            while (True):
                L = min([obj.dist_to_point((ray_x, ray_y)) if (obj.dist_to_point((ray_x, ray_y)) < self.ray_L) else self.ray_L for obj in objs])
                tmp_shape = plt.Circle((ray_x, ray_y), L, edgecolor="b", facecolor="None", linewidth=1/2, alpha=0.1)
                # ax.add_patch(tmp_shape)
                if ((L < 10**(-1)) or tmp_iter > max_iter):
                    break
                ray_x = ray_x + L*cos(ang)
                ray_y = ray_y + L*sin(ang)
                tot_L += L
                tmp_iter += 1
            if not(tmp_iter > max_iter):
                plt.plot([self.pos_x, self.pos_x+tot_L*cos(ang)], [self.pos_y, self.pos_y+tot_L*sin(ang)], color="b", linewidth=1/2, alpha=0.25)
            else:
                plt.plot([self.pos_x, self.pos_x+tot_L*cos(ang)], [self.pos_y, self.pos_y+tot_L*sin(ang)], color="r", linewidth=1/2, alpha=0.1)
    def draw_shape(self, ax):
        tmp_shape = plt.Circle((self.pos_x, self.pos_y), self.radius, edgecolor="k", facecolor="k")
        ax.add_patch(tmp_shape)
        ax.update_datalim(((self.pos_x-self.radius, self.pos_y-self.radius), (self.pos_x+self.radius, self.pos_y+self.radius)))
        self.shape = tmp_shape

if __name__ == "__main__":
    ## initialise figure canvas
    fig, ax = plt.subplots()
    ## create shapes
    square = Box(4, 10, 4, 4)
    rectangle = Box(-8, 7, 6, 3)
    circle = Circle(4, -4, 3)
    square.draw(ax)
    rectangle.draw(ax)
    circle.draw(ax)
    ## create camera
    cam = Camera(-10, 0, 10, (pi*5/2, pi*3/2), 100)
    cam.draw_shape(ax)
    cam.draw_rays(ax, (square, rectangle, circle), 100)
    ## show plot
    ax.axis('equal')
    ax.autoscale()
    plt.show()