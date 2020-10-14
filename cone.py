from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import math
from egl import *
from coord import *
from thing import *

class Cone(Thing):

    def __init__(self,pos_coord,base_radius,top_radius,height,color="#FF00FF"):
        self.pos = pos_coord
        self.br = base_radius
        self.tr = top_radius
        self.h = height
        self.color = color

        self.g = math.sqrt( math.pow(self.h,2) + math.pow(self.br,2) )

    def radius_at_height(self,height):
        small_h = self.h - height 
        small_g = (self.g * small_h) / self.h
        return math.sqrt( math.pow(small_g,2) - math.pow(small_h,2) )

    def distance_from(self, coord):
        height = coord.z - self.pos.z
        r = self.radius_at_height(height)
        dist = coord - Coord(self.pos.x,self.pos.y,coord.z)
        d = dist.size() - r
        return dist.normalize() * d

    def contains(self, coord):
        height = coord.z - self.pos.z
        r = self.radius_at_height(height)
        dist = coord - Coord(self.pos.x,self.pos.y,coord.z)
        return dist.size() < r

    def draw(self):
        glPushMatrix();
        glTranslatef( self.pos.x,self.pos.y,self.pos.z );
        quadObj = gluNewQuadric()
        eglSetHexColor(self.color)
        gluCylinder(quadObj, self.br, self.tr, self.h, 30, 30)
        glPopMatrix();