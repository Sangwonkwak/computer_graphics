import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import copy 

Left_pressed = False
Right_pressed = False
degree1 = 0.
degree2 = 0.
init_pos = np.array([0,0])
eye = np.array([0.,0.,.1])
at = np.array([0.,0.,0.])
cameraUp = np.array([0.,1.,0.])
scale = 1.
trans = np.array([0.,0.,0.])
t1 = 0.
full_list = []

class Node:
    def __init__(self,name):
        self.name = name
        self.offset = np.zeros(3)
        self.tree_index = -1
        self.channel_count = 0
        self.channel = []
        self.child = []
        self.parent = ''
    
# Make tree structure for parsing hierarchical model
tree = []
motion_start = 0 
def make_tree():
    global full_list, tree, motion_start
    tree = []
    motion_start = 0
    i = 0
    pre_index = -1
    while True:
        temp = full_list[i].split(' ')
        if temp[0] == "JOINT" or temp[0] == "ROOT":
            temp_Node = Node(temp[1])
            tree.append(temp_Node)
            
            # parent, child add
            if temp[0] == "JOINT":
                tree[pre_index].child.append(temp_Node)
                temp_Node.parent = tree[pre_index]
            elif temp[0] == "ROOT":
                temp_Node.parent = None
            
            # offset
            temp1 = full_list[i+2].split(' ')
            temp_Node.offset = np.array([int(temp1[1]),int(temp1[2]),int(temp1[3])])
            
            # channel
            temp2 = full_list[i+3].split(' ')
            temp_Node.channel_count = int(temp2[1])
            for j in range(temp_Node.channel_count):
                if temp2[2+j] == "XROTATION":
                    temp_Node.channel.append("XROT")
                elif temp[2+j] == "YROTATION":
                    temp_Node.channel.append("YROT")
                elif temp[2+j] == "ZROTATION":
                    temp_Node.channel.append("ZROT")
                elif temp[2+j] == "XPOSITION":
                    temp_Node.channel.append("XPOS")
                elif temp[2+j] == "YPOSITION":
                    temp_Node.channel.append("YPOS")
                elif temp[2+j] == "ZPOSITION":
                    temp_Node.channel.append("ZPOS")
            # tree index
            pre_index += 1
            temp_Node.tree_index = pre_index
            i += 4
        elif temp[0] == "End":
            temp_Node = Node("__END__")
            tree[pre_index].child.append(temp_Node)
            temp_Node.parent = tree[pre_index]
            # offset
            temp1 = full_list[i+2].split(' ')
            temp_Node.offset = np.array([int(temp1[1]),int(temp1[2]),int(temp1[3])])
            # tree index
            pre_index += 1
            temp_Node.tree_index = pre_index
            i += 3
        elif temp[0] == '}':
            pre_index -= 1
            i += 1
        elif temp[0] == "MOTION":
            motion_start = i
            break

def Euler_X(angle):
    return np.array([])
def draw_Model(node,motion_data,motion_index):
    if node.channel_count == 0:
        glPushMatrix()
        glBegin(GL_LINES)
        glVertex3fv(0.,0.,0.)
        glTranslatef(node.offset[0],node.offset[1],node.offset[2])
        glVertex3fv(0.,0.,0.)
        glPopMatrix()
    else:
        M = np.zeros((4,4))
        glPushMatrix()
        glBegin(GL_LINES)
        glVertex3fv(0.,0.,0.)
        glTranslatef(node.offset[0],node.offset[1],node.offset[2])
        for i in node.channel:
            if i == "XROT":
                
        
        
        
    
def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-scale,scale,-scale,scale,-1,1)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    real_eye = eye + trans
    real_at = at + trans
    gluLookAt(real_eye[0],real_eye[1],real_eye[2],real_at[0],real_at[1],real_at[2],cameraUp[0],cameraUp[1],cameraUp[2])
    
    drawframe()
    drawgrid()
    # drawModel()

# draw grid
def drawgrid():
    for i in range(21):
        glPushMatrix()
        glBegin(GL_LINES)
        glColor3ub(80,80,80)
        glVertex3fv(np.array([-1.0+0.1*i,0.,1.0]))
        glVertex3fv(np.array([-1.0+0.1*i,0.,-1.0]))
        glVertex3fv(np.array([1.0,0.,-1.0+0.1*i]))
        glVertex3fv(np.array([-1.0,0.,-1.0+0.1*i]))
        glEnd()
        glPopMatrix()

def drawframe():
    glBegin(GL_LINES)
    glColor3ub(255,0,0)
    glVertex3fv(np.array([-.5,0.,0.]))
    glVertex3fv(np.array([.5,0.,0.]))
    glColor3ub(0,255,0)
    glVertex3fv(np.array([0.,-.5,0.]))
    glVertex3fv(np.array([0.,.5,0.]))
    glColor3ub(0,0,255)
    glVertex3fv(np.array([0.,0.,-.5]))
    glVertex3fv(np.array([0.,0.,.5]))
    glEnd()

def button_callback(window,button,action,mod):
    global Left_pressed,Right_pressed,init_pos
    if action == glfw.PRESS:
        init_pos = glfw.get_cursor_pos(window)
        print(init_pos)
        if button == glfw.MOUSE_BUTTON_LEFT:
            Left_pressed = True
        elif button == glfw.MOUSE_BUTTON_RIGHT:
            Right_pressed = True
    elif action == glfw.RELEASE:
        if button == glfw.MOUSE_BUTTON_LEFT:
            Left_pressed = False
        elif button == glfw.MOUSE_BUTTON_RIGHT:
            Right_pressed = False

def cursor_callback(window,xpos,ypos):
    global eye,at,degree1,degree2,trans,cameraUp
    if Left_pressed:
        degree1 += (init_pos[0] - xpos) * 0.02
        degree2 += (-init_pos[1] + ypos) * 0.02
        if degree2 >= 0.:
            degree2 %= 360.
        else:
            degree2 %= -360.
        
        if 90. <= degree2 and degree2 <= 270.:
            cameraUp[1] = -1.
        elif -90. >= degree2 and degree2 >= -270.:
            cameraUp[1] = -1.
        else:
            cameraUp[1] = 1.
        eye[0] = 0.1 * np.cos(np.radians(degree2)) * np.sin(np.radians(degree1))
        eye[1] = 0.1 * np.sin(np.radians(degree2))
        eye[2] = 0.1 * np.cos(np.radians(degree2)) * np.cos(np.radians(degree1))
        
    elif Right_pressed:
        cameraFront = eye - at
        temp1 = np.cross(cameraFront,cameraUp)
        u = temp1/np.sqrt(np.dot(temp1,temp1))
        temp2 = np.cross(u,cameraFront)
        w = temp2/np.sqrt(np.dot(temp2,temp2))
        trans += u *(-init_pos[0]+xpos)*0.0001
        trans += w *(-init_pos[1]+ypos)*0.0001
        
def scroll_callback(window,xoffset,yoffset):
    global scale
    if scale <= 0.1 and yoffset == 1:
        scale = 0.1
        return
    scale -= 0.1 * yoffset

def drop_callback(window,paths):
    global full_list
    
    file_name = ''.join(paths)
    file = open(file_name,'r')
    full_list = file.readlines()
    
    file.close()

def main():
    global t1
    if not glfw.init():
        return
    t1 = glfw.get_time()
    window = glfw.create_window(700,700,'2015004302', None,None)
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    glfw.set_cursor_pos_callback(window,cursor_callback)
    glfw.set_mouse_button_callback(window,button_callback)
    glfw.set_scroll_callback(window,scroll_callback)
    glfw.set_drop_callback(window,drop_callback)
    glfw.swap_interval(1)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()