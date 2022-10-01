import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import random

vertices=(
    (1,-1,-1),
    (1,1,-1),
    (-1,1,-1),
    (-1,-1,-1),
    (1,-1,1),
    (1,1,1),
    (-1,-1,1),
    (-1,1,1)
    )

edges=(
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

surfaces=(
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )


colors=(
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,0,0),
    (1,1,1),
    (1,0,0),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,0,0),
    (1,1,1),
    (1,0,0)
    )

##ground_vertices=(
##    (-10,-1.1,20),
##    (10,-1.1,20),
##    (-10,-1.1,-300),
##    (10,-1.1,-300),
##    )



def set_vertices(max_distance,min_distance=-20,camera_x=0,camera_y=0):

    camera_x=-1*int(camera_x)
    camera_y=-1*int(camera_y)

    x_value_change=random.randrange(camera_x-75,camera_x+75)
    y_value_change=random.randrange(camera_y-75,camera_y+75)
    z_value_change=random.randrange(-1*max_distance,min_distance)

    new_vertices =[]
    for vert in vertices:
       new_vert=[]

       new_x=vert[0]+x_value_change
       new_y=vert[1]+y_value_change
       new_z=vert[2]+z_value_change

       new_vert.append(new_x)
       new_vert.append(new_y)
       new_vert.append(new_z)
       print(new_z)
       new_vertices.append(new_vert)
    return new_vertices

def cube(vertices):
    glBegin(GL_QUADS)
    
    for surface in surfaces:
        x=0
        #print(surface)
        for vertex in surface:
            x+=1
            glColor3fv(colors[x])
           # print(vertex)
            glVertex3fv(vertices[vertex])
    glEnd()


##    glBegin(GL_LINES)
##    glColor3fv((0,1,0))
##    for edge in edges:
##        for vertex in edge:
##            glVertex3fv(vertices[vertex])
##    glEnd()

def main():
    pygame.init()
    display=(800,600)
    pygame.display.set_mode(display,DOUBLEBUF|OPENGL)
    max_distance=100


    
    gluPerspective(45,(display[0]/display[1]),0.1,max_distance)  # Clipping Plane. These are the values at which we stop seeing the objects 

   # glTranslatef(random.randrange(-5,5),random.randrange(-5,5),-40)            #(x,y,z)
    glTranslatef(0,0,-40)  
    #object_passed=False

    x_move=0
    y_move=0

    cur_x=0
    cur_y=0

    game_speed=3
    direction_speed=3
    
    cube_dict={}

    for x in range(50):
        cube_dict[x]=set_vertices(max_distance)
        
    
   # glRotate(25,2,1,0)

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                   # glTranslatef(0.5,0,0)
                    x_move=direction_speed
                if event.key==pygame.K_RIGHT:
                   # glTranslatef(-0.5,0,0)
                    x_move=-1*direction_speed
                if event.key==pygame.K_UP:
                    #glTranslatef(0,-1,0)
                    y_move=-1*direction_speed
                if event.key==pygame.K_DOWN:
                    #glTranslatef(0,1,0)
                    y_move=direction_speed


            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                   x_move=0.0
                
                if event.key==pygame.K_UP or   event.key==pygame.K_DOWN:
                    y_move=0.0
                
        



                    
#             if event.type==pygame.MOUSEBUTTONDOWN:
#                 if event.button==4:       #Scroll is moving Forward it is classified as 4
#                     glTranslatef(0.0,0.0,1.0)
#                 if event.button==5:       #Scroll is moving Backward it is classified as 5
#                     glTranslatef(0.0,0.0,-1.0)
                    
                    

        # glRotate(1,3,1,1)

        x=glGetDoublev(GL_MODELVIEW_MATRIX)
       # print(x)
        camera_x=x[3][0]    
        camera_y=x[3][1]
        camera_z=x[3][2]    

        cur_x+=x_move
        cur_y+=y_move
        # To move in z-axis
        cur_z+=z_move
        
        
        glTranslatef(x_move,y_move,game_speed)    
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

       # ground()
        
        for each_cube in cube_dict:
            cube(cube_dict[each_cube])


        for each_cube in cube_dict:
            if camera_z<=cube_dict[each_cube][0][2]:
                new_max=int(-1*(camera_z-(max_distance*2)))

                cube_dict[each_cube]=set_vertices(new_max,int(camera_z-max_distance),cur_x,cur_y, cur_z)
                        
        
    
        pygame.display.flip()
        #pygame.time.wait(10)

##        if camera_z<=0:
##            object_passed=True
        


main()
#glLoadIdentity()

pygame.quit()
quit()
