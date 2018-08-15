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
    global axes
    #print("x-axis = x:",round(axes["x"].x,2)," y:",round(axes["x"].y,2)," z:",round(axes["x"].z,2))
    #print("y-axis = x:",round(axes["y"].x,2)," y:",round(axes["y"].y,2)," z:",round(axes["y"].z,2))
    #print("z-axis = x:",round(axes["z"].x,2)," y:",round(axes["z"].y,2)," z:",round(axes["z"].z,2))

    layers = {}
    for x in ["R","L","U","D","F","B"]:
        layers[x] = [cube[center_loc[x]]]
        #print(x,"= x:",round(layers[x][0].pos.x,2)," y:",round(layers[x][0].pos.y,2)," z:",round(layers[x][0].pos.z,2))
    #for k,v in cube.items():
    #    print(k,"= x:",round(v.pos.x,2)," y:",round(v.pos.y,2)," z:",round(v.pos.z,2))
    R_c = layers["R"][0].pos
    L_c = layers["L"][0].pos
    U_c = layers["U"][0].pos
    D_c = layers["D"][0].pos
    F_c = layers["F"][0].pos
    B_c = layers["B"][0].pos

    for name,comp in cube.items():
        if math.isclose(comp.pos.dot(R_c),1,rel_tol=1e-2):
            layers["R"].append(comp)
        if math.isclose(comp.pos.dot(L_c),1,rel_tol=1e-2):
            layers["L"].append(comp)
        if math.isclose(comp.pos.dot(U_c),1,rel_tol=1e-2):
            layers["U"].append(comp)
        if(math.isclose(comp.pos.dot(D_c),1,rel_tol=1e-2)):
            layers["D"].append(comp)
        if(math.isclose(comp.pos.dot(F_c),1,rel_tol=1e-2)):
            layers["F"].append(comp)
        if(math.isclose(comp.pos.dot(B_c),1,rel_tol=1e-2)):
            layers["B"].append(comp)
    layers["M"] = list(set(layers["F"] + layers["U"] + layers["B"] + layers["D"]).difference(set(layers["L"])).difference(set(layers["R"])))
    layers["E"] = list(set(layers["F"] + layers["R"] + layers["B"] + layers["L"]).difference(set(layers["U"])).difference(set(layers["D"])))
    layers["S"] = list(set(layers["R"] + layers["U"] + layers["L"] + layers["D"]).difference(set(layers["F"])).difference(set(layers["B"])))
    return layers

def rotateLayer(layer, axis, angle=90, origin=None):
    if not origin:
        origin=layer[0].pos
    steps = angle//3
    for i in range(steps):
        sleep(0.000000000001)
        for comp in layer:
            comp.rotate(radians(3), axis = axis, origin = origin)

def rotateCube(axis, angle=90):
    global cube
    steps = angle//3
    for i in range(steps):
        sleep(0.000000000001)
        for name, comp in cube.items():
            comp.rotate(angle=radians(3),axis=axis, origin=vector(0,0,0))

def rotation(layer_name, axis, origin=None):
    global layers, axes, cube, center_loc
    ax = ""
    if(len(axis)==1):
        ax = axes[axis]
    else:
        if axis[0]=='-':
           ax = -axes[axis[1]]
        else:
            ax = axes[axis[1]]
    rotateLayer(layers[layer_name], ax, origin=origin)
    layers = recalculateLayers()

def U():
    rotation("U", "-y")

def U_():
    rotation("U", "y")

def D():
    rotation("D", "y")

def D_():
    rotation("D", "-y")

def E():
    rotation("E", "y", origin = vector(0,0,0))

def E_():
    rotation("E", "-y", origin = vector(0,0,0))

def R():
    rotation("R", "-x")

def R_():
    rotation("R", "x")

def L():
    rotation("L", "x")

def L_():
    rotation("L", "-x")

def M():
    rotation("M", "x", origin = vector(0,0,0))

def M_():
    rotation("M", "-x", origin = vector(0,0,0))

def F():
    rotation("F", "-z")

def F_():
    rotation("F", "z")

def B():
    rotation("B", "z")

def B_():
    rotation("B", "-z")

def S():
    rotation("S", "z", origin = vector(0,0,0))

def S_():
    rotation("S", "-z", origin = vector(0,0,0))

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
    scene2 = canvas(title="The Rubik's Cube", x=0, y=0, width=1000, height=500, center=vector(0,0,0), background=vector(0,0,0))
    scene2.camera.pos = vector(0,0,3)
    scene2.select()
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
        "x_loc": -5,
        "top": 2,
        "right": 1,
        "left": 0,
        "bottom": -1,
        "back": -2
    }

    generateLabels()
    for name,comp in cube.items():
        comp.rotate(angle=radians(45),axis=vector(0,-1,0), origin=vector(0,0,0))
        comp.rotate(angle=radians(20),axis=vector(1,0,0), origin=vector(0,0,0))
    for k,v in axes.items():
        axes[k] = v.rotate(angle=radians(45),axis=vector(0,-1,0))

    for k,v in axes.items():
        axes[k] = v.rotate(angle=radians(20),axis=vector(1,0,0))

    layers = recalculateLayers()
    #free_rotate(cube)
    
    while True:
        ev = scene2.waitfor('click keydown')
        if ev.event == 'click':
            if ev.pos.x < label_pos["x_loc"]+1 and ev.pos.x > label_pos["x_loc"]-1:
                if ev.pos.y < label_pos["top"]+0.5 and ev.pos.y > label_pos["top"]-0.5:
                    showTop()
                if ev.pos.y < label_pos["right"]+0.5 and ev.pos.y > label_pos["right"]-0.5:
                    showRight()
                if ev.pos.y < label_pos["left"]+0.5 and ev.pos.y > label_pos["left"]-0.5:
                    showLeft()
                if ev.pos.y < label_pos["bottom"]+0.5 and ev.pos.y > label_pos["bottom"]-0.5:
                    showBottom()
                if ev.pos.y < label_pos["back"]+0.5 and ev.pos.y > label_pos["back"]-0.5:
                    showBack()
        else:
            if ev.key=='r':
                R()
            if ev.key=='R':
                R_()
            if ev.key=='l':
                L()
            if ev.key=='L':
                L_()
            if ev.key=='m':
                M()
            if ev.key=='M':
                M_()
            if ev.key=='u':
                U()
            if ev.key=='U':
                U_()
            if ev.key=='d':
                D()
            if ev.key=='D':
                D_()
            if ev.key=='e':
                E()
            if ev.key=='E':
                E_()
            if ev.key=='f':
                F()
            if ev.key=='F':
                F_()
            if ev.key=='b':
                B()
            if ev.key=='B':
                B_()
            if ev.key=='s':
                S()
            if ev.key=='S':
                S_()
            

