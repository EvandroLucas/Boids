import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
import math
import random
import sys
import random
from random import randrange
from camera import *

from egl import *
from boid import *



boid_model = {
    "spine1" : (0,0,0),
    "spine2" : (0,1,0),
    "head1" : (1, 0.1, 0.05),
    "head2" : (1, -0.1, 0.05),
    "head3" : (1, 0, -0.1),
    "head4" : (1.2, 0, 0),
    "bodyEnd" : (0.6, 0, 0),
    "tail1" : (0.3, -0.1, 0),
    "tail2" : (0.3, 0.1, 0),
    "l_wing" : (0.5, 0.5, 0),
    "r_wing" : (0.5, -0.5, 0)
}

def transform_boid(pos_vec_1,pos_vec_2,boid):
    Q = np.asarray((pos_vec_1))
    P = np.asarray((pos_vec_2))
    # M = Q.dot(np.linalg.pinv(P))
    print("P : " + str(P))
    print("Q : " + str(Q))
    # print("M : " + str(M))


def draw_boid(boid):

    # transform_boid((0,1,0),(1,0,1),boid)

    bodyColor = "#E3E853"
    beakColor = "#A65000"
    b = boid.copy()

    eglLine(b["spine1"],b["spine2"],COLOR_YELLOW)

    eglTriangle(b["head1"],b["head2"],b["head4"],COLOR_ORANGE)
    eglTriangle(b["head1"],b["head3"],b["head4"],beakColor)
    eglTriangle(b["head1"],b["head2"],b["head3"],COLOR_RED)
    eglTriangle(b["head2"],b["head3"],b["head4"],beakColor)

    eglTriangle(b["head1"],b["head2"],b["bodyEnd"],bodyColor)
    eglTriangle(b["head1"],b["head3"],b["bodyEnd"],bodyColor)
    eglTriangle(b["head2"],b["head3"],b["bodyEnd"],bodyColor)

    eglTriangle(b["tail1"],b["tail2"],b["bodyEnd"],bodyColor)

    eglTriangle(b["head1"],b["head3"],b["l_wing"],bodyColor)
    eglTriangle(b["head1"],b["bodyEnd"],b["l_wing"],COLOR_YELLOW)
    eglTriangle(b["head3"],b["bodyEnd"],b["l_wing"],bodyColor)

    eglTriangle(b["head2"],b["head3"],b["r_wing"],bodyColor)
    eglTriangle(b["head2"],b["bodyEnd"],b["r_wing"],COLOR_YELLOW)
    eglTriangle(b["head3"],b["bodyEnd"],b["r_wing"],bodyColor)


def drawBoid(positionStart, positionEnd):
    # Spine of the boid
    eglLine(positionStart,positionEnd,COLOR_YELLOW)

    # Head
    dim = 0.1
    head1 = (positionEnd[0],positionEnd[1] + dim  ,positionEnd[2]  + (dim/2)   )
    head2 = (positionEnd[0],positionEnd[1] - dim  ,positionEnd[2]  + (dim/2))
    head3 = (positionEnd[0],positionEnd[1]   ,positionEnd[2] - dim )
    head4 = (positionEnd[0] + dim + 0.1,positionEnd[1],positionEnd[2])
    headColor = "#FF2337"
    eglTriangle(head1,head2,head4,COLOR_ORANGE)
    eglTriangle(head1,head3,head4,COLOR_ORANGE)
    eglTriangle(head1,head2,head3,COLOR_RED)
    eglTriangle(head2,head3,head4,COLOR_ORANGE)

    # Body 
    bodyColor = "#E3E853"
    bodyEnd = (0.6,0,0)
    eglTriangle(head1,head2,bodyEnd,bodyColor)
    eglTriangle(head1,head3,bodyEnd,bodyColor)
    eglTriangle(head2,head3,bodyEnd,bodyColor)

    # Tail
    tail1 = (0.3,-0.1,0)
    tail2 = (0.3,0.1,0)
    eglTriangle(tail1,tail2,bodyEnd,bodyColor)

    # Left Wing
    l_wing = (0.5,0.5,0)
    eglTriangle(head1,head3,l_wing,bodyColor)
    eglTriangle(head1,bodyEnd,l_wing,COLOR_YELLOW)
    eglTriangle(head3,bodyEnd,l_wing,bodyColor)

    # Right Wing
    r_wing = (0.5,-0.5,0)
    eglTriangle(head2,head3,r_wing,bodyColor)
    eglTriangle(head2,bodyEnd,r_wing,COLOR_YELLOW)
    eglTriangle(head3,bodyEnd,r_wing,bodyColor)

    print("head1 = " + str(head1))
    print("head2 = " + str(head2))
    print("head3 = " + str(head3))
    print("head4 = " + str(head4))
    print("bodyEnd = " + str(bodyEnd))
    print("tail1 = " + str(tail1))
    print("tail2 = " + str(tail2))
    print("l_wing = " + str(l_wing))
    print("r_wing = " + str(r_wing))


def draw_ground(size,color,height):
    eglSetHexColor(color)
    glBegin(GL_POLYGON)     
    glVertex3f(size,size*(-1),height)
    glVertex3f(size*(-1),size*(-1),height)
    glVertex3f(size*(-1),size,height)
    glVertex3f(size,size,height)
    glEnd()

def draw_cone():
    quadObj = gluNewQuadric()
    eglSetHexColor("#FF00FF")
    gluCylinder(quadObj, 3, 0, 10, 30, 30)


def draw_axis():
    axis_distance = 10000
    # X AXIS
    eglLine((0,0,0),(axis_distance,0,0),COLOR_BLUE)
    eglLine((0,0,0),((-1)*axis_distance,0,0),COLOR_LIGHT_BLUE)
    
    # Y AXIS
    eglLine((0,0,0),(0,axis_distance,0),COLOR_GREEN)
    eglLine((0,0,0),(0,(-1)*axis_distance,0),COLOR_LIGHT_GREEN)

    # Z AXIS 
    eglLine((0,0,0),(0,0,axis_distance),COLOR_RED)
    eglLine((0,0,0),(0,0,(-1)*axis_distance),COLOR_LIGHT_RED)

def draw_cage():
    eglLine((10,10,0),(10,10,10),"#2A713C")
    eglLine((10,-10,0),(10,-10,10),"#2A713C")
    eglLine((-10,10,0),(-10,10,10),"#2A713C")
    eglLine((-10,-10,0),(-10,-10,10),"#2A713C")
    eglLine((10,10,10),(10,-10,10),"#2A713C")
    eglLine((10,-10,10),(-10,-10,10),"#2A713C")
    eglLine((-10,-10,10),(-10,10,10),"#2A713C")
    eglLine((-10,10,10),(10,10,10),"#2A713C")

def draw_grid():
    repeat = 50
    size = 1

    height = 0.01

    for i in range(1,repeat):
        axis_distance = repeat
        origin_distance = size*i
        # Paralel to the X AXIS
        color = COLOR_BLACK
        eglLine((0,origin_distance,height),(axis_distance,origin_distance,height),color)
        eglLine((0,origin_distance,height),((-1)*axis_distance,origin_distance,height),color)
        eglLine((0,-origin_distance,height),(axis_distance,-origin_distance,height),color)
        eglLine((0,-origin_distance,height),((-1)*axis_distance,-origin_distance,height),color)

        # Paralel to the Y AXIS
        color = COLOR_BLACK
        eglLine((origin_distance,0,height),(origin_distance,axis_distance,height),color)
        eglLine((origin_distance,0,height),(origin_distance,(-1)*axis_distance,height),color)
        eglLine((-origin_distance,0,height),(-origin_distance,axis_distance,height),color)
        eglLine((-origin_distance,0,height),(-origin_distance,(-1)*axis_distance,height),color)
        

def IdentityMat44(): 
    return np.matrix(np.identity(4), copy=False, dtype='float32')


def random_goal():
    ri =9
    rx, ry, rz = random.uniform(ri,ri*(-1)),random.uniform(ri,ri*(-1)),random.uniform(ri,3)
    return Coord(rx,ry,rz)


def avoid_wall_points(b):

    p = b.pos.copy()
    wall_points = [
        Coord(p.x,p.y,0), # ground
        Coord(p.x,p.y,10),
        Coord(10,p.y,p.z),
        Coord(-10,p.y,p.z),
        Coord(p.x,10,p.z),
        Coord(p.x,-10,p.z),
    ]
    # Avoid walls
    for w in wall_points:
        b.avoid(w,2,0.1)

def main():

    print("Hello World!")
    display = (800,800)
    aspect_ratio = display[0]/display[1]
    fov = 45
    
    print ("Display: " + str(display))

    pygame.display.set_mode(display,DOUBLEBUF|OPENGL)
    pygame.mouse.set_visible(True)

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(fov, aspect_ratio, 0.1, 1000)
    view_mat = IdentityMat44()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glGetFloatv(GL_MODELVIEW_MATRIX, view_mat)
    glLoadIdentity()

    camera = Camera( (13,21,12) , (0,0,3) , (0,0,1) )
    camera.correct_aim()

    boids_speed = 0.1
    boids = []
    goal_boid = Boid(Coord(5,5,5),Coord(10,10,10),speed = boids_speed,color = COLOR_RED)
    goal_point = Coord(10,0,0)

    cone = Cone(Coord(0,0,0),3,0,8)

    allow_another_boid = True
    allow_speed_change = True
    paused = False
    while True:
        glMatrixMode(GL_MODELVIEW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_p:
                    paused = not paused

        speed = 0.1
        keys=pygame.key.get_pressed()
        if keys[K_a]:
            camera.move_left_to(camera.aim,step = speed)
        if keys[K_d]:     
            camera.move_right_to(camera.aim,step = speed)
        if keys[K_w]:     
            camera.move_to(camera.aim - camera.pos,step = speed)
        if keys[K_s]:     
            camera.move_against(camera.aim - camera.pos,step = speed)
        if keys[K_SPACE]: 
            camera.move_on_axis(0.2,"z")
        if keys[K_LCTRL]:  
            camera.move_on_axis(-0.2,"z")
        if keys[K_RIGHT]: 
            camera.look_right(2)
        if keys[K_LEFT]:  
            camera.look_left(2)
        if keys[K_UP]: 
            camera.look_up(0.5)
        if keys[K_DOWN]:  
            camera.look_down(0.5)
        if keys[K_m]:  
            camera.aim = goal_boid.pos
        if keys[K_DOWN]:  
            camera.look_down(0.5)
        if keys[K_PAGEUP] and allow_speed_change:  
            boids_speed += 0.2
            allow_speed_change = False
        if keys[K_PAGEDOWN] and allow_speed_change:
            boids_speed -= 0.2
            allow_speed_change = False
        if not keys[K_PAGEUP] and not keys[K_PAGEDOWN]:
            allow_speed_change = True
        if keys[K_KP_PLUS] and allow_another_boid:  
            bx = Boid(random_goal(),goal_boid.pos,speed = boids_speed)
            while cone.contains(bx.pos):
                bx = Boid(random_goal(),Coord(0,0,0),speed = boids_speed)
            boids.append(bx)
            allow_another_boid = False
        if keys[K_KP_MULTIPLY] and allow_another_boid:  
            bx = Boid(random_goal(),random_goal(),speed = boids_speed, anarchy=True, color = "#7926FF")
            while cone.contains(bx.pos):
                bx = Boid(random_goal(),Coord(0,0,0),speed = boids_speed, anarchy=True, color = "#7926FF")
            boids.append(bx)
            allow_another_boid = False
        if keys[K_KP_MINUS] and allow_another_boid:  
            boids.pop(random.randrange(len(boids))) 
            allow_another_boid = False
        if not keys[K_KP_PLUS] and not keys[K_KP_MULTIPLY] and not keys[K_KP_MINUS]:
            allow_another_boid = True

        glPushMatrix()
        glLoadIdentity()

        glMultMatrixf(view_mat)
        glGetFloatv(GL_MODELVIEW_MATRIX, view_mat)

        t = eglHexToTuple("#70CCFF")
        glClearColor(t[0],t[1],t[2],0.1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        camera.update()
        camera.look()

        # draw_axis()
        # draw_grid()
        draw_ground(1000,"#34CB5E",0.1)
        draw_ground(10,"#35904C",0.2)
        draw_cage()

        cone.draw()
        # draw_cone()

        if not paused:

            goal_boid.goal =random_goal()
            avoid_wall_points(goal_boid)
            goal_boid.speed = boids_speed
            goal_boid.move()  

            for i in range(len(boids)):
                b = boids[i]
                # All boids will avoid one another
                for j in range(i,len(boids)):
                    b2 = boids[j]
                    b.avoid(b2.pos,1,0.05)
                    b2.avoid(b2.pos,1,0.05)
                # All boids will avoid the cone
                b.avoid_thing(cone,2,0.05)
                # Non anarchist boids will follow the goal boid
                if not b.anarchy:
                    b.goal = goal_boid.pos
                # Anarchist boids will do their own thing
                else:
                    for j in range(i,len(boids)):
                        b2 = boids[j]
                        b.notice_boid(b2,2)
                        if b2.anarchy :
                            b2.notice_boid(b,2)

                    b.goal = random_goal()

                avoid_wall_points(b)

            for b in boids: 
                b.speed = boids_speed
                b.move()
                    

        goal_boid.draw()
        for b in boids: 
            b.draw()

        glPopMatrix()

        pygame.display.flip()
        # pygame.time.wait()
        pygame.event.pump()

if __name__ == "__main__":
    main()