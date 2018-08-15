from vpython import *
import math

def cubelet(pos, side, Fcolor=color.black, Bcolor=color.black, Rcolor=color.black, Lcolor=color.black, Ucolor=color.black, Dcolor=color.black):
    pyramids = [
        #front
        pyramid(color=Fcolor, size=vector(side/2,side,side), pos=vector(pos.x,pos.y,pos.z+side/2), axis=vector(0,0,-1)),
        #back
        pyramid(color=Bcolor, size=vector(side/2,side,side), pos=vector(pos.x,pos.y,pos.z-side/2), axis=vector(0,0,1)),
        #right
        pyramid(color=Rcolor, size=vector(side/2,side,side), pos=vector(pos.x+side/2,pos.y,pos.z), axis=vector(-1,0,0)),
        #left
        pyramid(color=Lcolor, size=vector(side/2,side,side), pos=vector(pos.x-side/2,pos.y,pos.z), axis=vector(1,0,0)),
        #up
        pyramid(color=Ucolor, size=vector(side/2,side,side), pos=vector(pos.x,pos.y+side/2,pos.z), axis=vector(0,-1,0)),
        #down
        pyramid(color=Dcolor, size=vector(side/2,side,side), pos=vector(pos.x,pos.y-side/2,pos.z), axis=vector(0,1,0))
    ]
    return compound(pyramids)

def free_rotate():
    global cube
    while True:
        sleep(2)
        cube.rotate(angle=radians(45), axis=vector(1,0,0))
        cube.rotate(angle=radians(45), axis=vector(0,1,0))

def recalculateLayers():
    global cube
    global center_loc
    layers = {}
    for x in ["R","L","U","D","F","B"]:
        layers[x] = [cube[center_loc[x]]]
    R_c = round(layers["R"][0].pos.x)
    L_c = round(layers["L"][0].pos.x)
    U_c = round(layers["U"][0].pos.y)
    D_c = round(layers["D"][0].pos.y)
    F_c = round(layers["F"][0].pos.z)
    B_c = round(layers["B"][0].pos.z)
    
    for name,comp in cube.items():
        if(round(comp.pos.x)==R_c):
            layers["R"].append(comp)
        if(round(comp.pos.x)==L_c):
            layers["L"].append(comp)
        if(round(comp.pos.y)==U_c):
            layers["U"].append(comp)
        if(round(comp.pos.y)==D_c):
            layers["D"].append(comp)
        if(round(comp.pos.z)==F_c):
            layers["F"].append(comp)
        if(round(comp.pos.z)==B_c):
            layers["B"].append(comp)
    return layers

def rotateLayer(layer, axis, angle=90):
    steps = angle//3
    for i in range(steps):
        sleep(0.000000000001)
        for comp in layer:
            comp.rotate(radians(3), axis = axis, origin=layer[0].pos)

def rotateCube(axis, angle=90):
    global cube
    steps = angle//3
    for i in range(steps):
        sleep(0.000000000001)
        for name, comp in cube.items():
            comp.rotate(angle=radians(3),axis=axis, origin=vector(0,0,0))

def R():
    global layers, axes, cube, center_loc
    rotateLayer(layers["R"], -axes["x"])
    return recalculateLayers()
    
def U():
    global layers, axes, cube, center_loc
    rotateLayer(layers["U"], -axes["y"])
    return recalculateLayers()

def generateCube(cubelet_size):
    #centers
    white_center = cubelet(vector(0,-1,0),cubelet_size, Dcolor=color.white)
    yellow_center = cubelet(vector(0,1,0),cubelet_size,Ucolor=color.yellow)
    red_center = cubelet(vector(1,0,0),cubelet_size, Rcolor=color.red)
    orange_center = cubelet(vector(-1,0,0),cubelet_size, Lcolor=color.orange)
    green_center = cubelet(vector(0,0,-1),cubelet_size, Bcolor=color.green)
    blue_center = cubelet(vector(0,0,1),cubelet_size, Fcolor=color.blue)

    # Lower Layer
    w_r_b = cubelet(vector(1,-1,1),cubelet_size, Fcolor=color.blue, Rcolor=color.red, Dcolor=color.white)
    w_b = cubelet(vector(0,-1,1),cubelet_size, Fcolor=color.blue, Dcolor=color.white)
    w_b_o = cubelet(vector(-1,-1,1),cubelet_size, Fcolor=color.blue, Lcolor=color.orange, Dcolor=color.white)
    w_o = cubelet(vector(-1,-1,0),cubelet_size, Lcolor=color.orange, Dcolor=color.white)
    w_o_g = cubelet(vector(-1,-1,-1),cubelet_size, Lcolor=color.orange, Bcolor=color.green, Dcolor=color.white)
    w_g = cubelet(vector(0,-1,-1),cubelet_size, Bcolor=color.green, Dcolor=color.white)
    w_g_r = cubelet(vector(1,-1,-1),cubelet_size, Rcolor=color.red, Bcolor=color.green, Dcolor=color.white)
    w_r = cubelet(vector(1,-1,0),cubelet_size, Rcolor=color.red, Dcolor=color.white)

    #Middle Layer
    r_b = cubelet(vector(1,0,1),cubelet_size, Rcolor=color.red, Fcolor=color.blue)
    b_o = cubelet(vector(-1,0,1),cubelet_size, Lcolor=color.orange, Fcolor=color.blue)
    o_g = cubelet(vector(-1,0,-1),cubelet_size, Lcolor=color.orange, Bcolor=color.green)
    g_r = cubelet(vector(1,0,-1),cubelet_size, Rcolor=color.red, Bcolor=color.green)

    #Upper Layer
    y_r_b = cubelet(vector(1,1,1),cubelet_size, Fcolor=color.blue, Rcolor=color.red, Ucolor=color.yellow)
    y_b = cubelet(vector(0,1,1),cubelet_size, Fcolor=color.blue, Ucolor=color.yellow)
    y_b_o = cubelet(vector(-1,1,1),cubelet_size, Fcolor=color.blue, Lcolor=color.orange, Ucolor=color.yellow)
    y_o = cubelet(vector(-1,1,0),cubelet_size, Lcolor=color.orange, Ucolor=color.yellow)
    y_o_g = cubelet(vector(-1,1,-1),cubelet_size, Lcolor=color.orange, Bcolor=color.green, Ucolor=color.yellow)
    y_g = cubelet(vector(0,1,-1),cubelet_size, Bcolor=color.green, Ucolor=color.yellow)
    y_g_r = cubelet(vector(1,1,-1),cubelet_size, Rcolor=color.red, Bcolor=color.green, Ucolor=color.yellow)
    y_r = cubelet(vector(1,1,0),cubelet_size, Rcolor=color.red, Ucolor=color.yellow)
    
    #whole cube
    cube = {
        "w_c": white_center,
        "y_c": yellow_center,
        "r_c": red_center,
        "o_c": orange_center,
        "g_c": green_center,
        "b_c": blue_center,
        "w_r_b": w_r_b,
        "w_b": w_b,
        "w_b_o": w_b_o,
        "w_o": w_o,
        "w_o_g": w_o_g,
        "w_g": w_g,
        "w_g_r": w_g_r,
        "w_r": w_r,
        "r_b": r_b,
        "b_o": b_o,
        "o_g": o_g,
        "g_r": g_r,
        "y_r_b": y_r_b,
        "y_b": y_b,
        "y_b_o": y_b_o,
        "y_o": y_o,
        "y_o_g": y_o_g,
        "y_g": y_g,
        "y_g_r": y_g_r,
        "y_r": y_r
    }
    return cube

def generateLabels():
    global label_pos
    top_label = label(pos=vector(label_pos["x_loc"], label_pos["top"], 0), text='Show Top')
    right_label = label(pos=vector(label_pos["x_loc"], label_pos["right"], 0), text='Show Right')
    left_label = label(pos=vector(label_pos["x_loc"], label_pos["left"], 0), text='Show Left')
    bottom_label = label(pos=vector(label_pos["x_loc"], label_pos["bottom"], 0), text='Show Bottom')
    back_label = label(pos=vector(label_pos["x_loc"], label_pos["back"], 0), text='Show Back')

def showTop():
    global layers, center_loc, axes
    rotateCube(axes["x"])
    temp = center_loc.copy()
    temp["U"] = center_loc["B"]
    temp["D"] = center_loc["F"]
    temp["F"] = center_loc["U"]
    temp["B"] = center_loc["D"]
    center_loc = temp
    layers = recalculateLayers()

def showRight():
    global layers, center_loc, axes
    rotateCube(-axes["y"])
    temp = center_loc.copy()
    temp["F"] = center_loc["R"]
    temp["R"] = center_loc["B"]
    temp["B"] = center_loc["L"]
    temp["L"] = center_loc["F"]
    center_loc = temp
    layers = recalculateLayers()

def showLeft():
    global layers, center_loc, axes
    rotateCube(axes["y"])
    temp = center_loc.copy()
    temp["F"] = center_loc["L"]
    temp["R"] = center_loc["F"]
    temp["B"] = center_loc["R"]
    temp["L"] = center_loc["B"]
    center_loc = temp
    layers = recalculateLayers()

def showBottom():
    global layers, center_loc, axes
    rotateCube(-axes["x"])
    temp = center_loc.copy()
    temp["F"] = center_loc["D"]
    temp["D"] = center_loc["B"]
    temp["B"] = center_loc["U"]
    temp["U"] = center_loc["F"]
    center_loc = temp
    layers = recalculateLayers()

def showBack():
    showTop()
    showTop()

if __name__=="__main__":
    cubelet_size = 0.9

    #global
    axes = {
        "x": vector(1,0,0),
        "y": vector(0,1,0),
        "z": vector(0,0,1)
        }
    
    #global
    cube = generateCube(cubelet_size)

    #global
    center_loc = {
        "R":"r_c",
        "L":"o_c",
        "F":"b_c",
        "B":"g_c",
        "U":"y_c",
        "D":"w_c"
    }
    label_pos = {
        "x_loc": -3,
        "top": 2,
        "right": 1,
        "left": 0,
        "bottom": -1,
        "back": -2
    }

    generateLabels()
    #for name,comp in cube.items():
    #    comp.rotate(angle=radians(45),axis=vector(0,-1,0), origin=vector(0,0,0))
    #    comp.rotate(angle=radians(45),axis=vector(1,0,0), origin=vector(0,0,0))
    #for k,v in axes.items():
    #    axes[k] = v.rotate(angle=radians(45),axis=vector(0,-1,0))

    #for k,v in axes.items():
    #    axes[k] = v.rotate(angle=radians(45),axis=vector(1,0,0))

    layers = recalculateLayers()
    #free_rotate(cube)
    
    while True:
        ev = scene.waitfor('click keydown')
        if ev.event == 'click':
            if ev.pos.x < label_pos["x_loc"]+1 and ev.pos.x > label_pos["x_loc"]-1:
                if ev.pos.y < label_pos["top"]+0.3 and ev.pos.y > label_pos["top"]-0.3:
                    showTop()
                if ev.pos.y < label_pos["right"]+0.3 and ev.pos.y > label_pos["right"]-0.3:
                    showRight()
                if ev.pos.y < label_pos["left"]+0.3 and ev.pos.y > label_pos["left"]-0.3:
                    showLeft()
                if ev.pos.y < label_pos["bottom"]+0.3 and ev.pos.y > label_pos["bottom"]-0.3:
                    showBottom()
                if ev.pos.y < label_pos["back"]+0.3 and ev.pos.y > label_pos["back"]-0.3:
                    showBack()
        else:
            if ev.key=='r':
                layers = R()
            if ev.key=='u':
                layers = U()
            if ev.key=='t':
                layers = R()
            if ev.key=='i':
                layers = U()
            if ev.key=='g':
                layers = R()
                layers = U()
                layers = R()
                layers = U()

