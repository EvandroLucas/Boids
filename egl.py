from OpenGL.GL import *
from OpenGL.GLU import *

import math

COLOR_BLUE =        "#0000FF"
COLOR_GREEN =       "#00FF00"
COLOR_RED =         "#FF0000"
COLOR_YELLOW =      "#FFFF00"
COLOR_PINK =        "#FF00FF"
COLOR_CYAN =        "#00FFFF"
COLOR_ORANGE =      "#FF7A00"
COLOR_WHITE =       "#FFFFFF"
COLOR_BLACK =       "#000000"
COLOR_DARK_GREY =   "#202020"

COLOR_LIGHT_BLUE  = "#9A9AFF"
COLOR_LIGHT_GREEN = "#9AFF9A"
COLOR_LIGHT_RED   = "#FF9A9A"



def eglLine(tuple1 : tuple,tuple2 : tuple, hexColor : str):
    glBegin(GL_LINES)
    eglSetHexColor(hexColor)
    if len(tuple1) == 3:
        glVertex3fv(tuple1)
        glVertex3fv(tuple2)
    if len(tuple1) == 2:
        glVertex2fv(tuple1)
        glVertex2fv(tuple2)
    glEnd()
    eglSetHexColor("#FFFFFF")

def eglTriangle(tuple1 : tuple, tuple2 : tuple, tuple3 : tuple, hexColor : str):
    glBegin(GL_TRIANGLES)
    eglSetHexColor(hexColor)
    if len(tuple1) == 3:
        glVertex3fv(tuple1)
        glVertex3fv(tuple2)
        glVertex3fv(tuple3)
    if len(tuple1) == 2:
        glVertex2fv(tuple1)
        glVertex2fv(tuple2)
        glVertex2fv(tuple3)
    glEnd()
    eglSetHexColor("#FFFFFF")
    
def eglSetColor(colorTuple : tuple):
    glColor3f(colorTuple[0],colorTuple[1],colorTuple[2])

def eglSetHexColor(hex : str):
    eglSetColor(eglHexToTuple(hex))

def eglHexToTuple(hex : str):
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i + hlen // 3], 16)/255 for i in range(0, hlen, hlen // 3))


def eglPoint(tuple, hexColor : str):
    eglSetHexColor(hexColor)
    posx, posy = tuple[0],tuple[1]
    sides = 32    
    radius = 0.1    
    glBegin(GL_POLYGON)    
    for i in range(100):    
        cosine= radius * math.cos(i*2*math.pi/sides) + posx    
        sine  = radius * math.sin(i*2*math.pi/sides) + posy    
        glVertex3f(cosine,sine,tuple[2])
    glEnd()

def eglTringle(tuple1, tuple2, tuple3, hexColor : str):
    eglSetHexColor(hexColor)
    glBegin(GL_POLYGON)    
    glVertex3f(tuple1[0],tuple1[1],tuple1[2])
    glVertex3f(tuple2[0],tuple2[1],tuple2[2])
    glVertex3f(tuple3[0],tuple3[1],tuple3[2])
    glEnd()