import bpy
import mathutils
import math

#
# cubic(coords, t)              # get point on bezier curve r(t)
# dt_cubic(coords, t)           # get point on r'(t)
# dt2_cubic(coords, t)          # get point on r''(t)
# dt3_cubic(coords, t)          # get point on r'''(t)
# deCasteljau(coords, t)        # calculate point using De Casteljau
# vectorMagnitude(vec)          # get magnitude of vector
# tangent_cubic(coords, t)      # get unit tangent vector at point of bezier
# binormal_cubic(coords, t)     # binormal vector at point
# normal_cubic(coords, t)       # cross product T x B
# curvature_cubic(coords, t)    # get curvature at point of bezier
# torsion(coords, t)            # get torsion at point
#
# moveSplinesTo_cubic(coords)       # move points of cubic bezier curve
# createBez_cubic(coords)           # create a cubic bezier curve
# pointOnBez_cubic(coords, t)       # place a point object in the scene
# 

    
    
# r(t)    
def cubic(coords, t):
    #calculate location at t from the explicit def of cubic bezier curve
    P0 = mathutils.Vector(coords[0])
    P1 = mathutils.Vector(coords[1])
    P2 = mathutils.Vector(coords[2])
    P3 = mathutils.Vector(coords[3])
    B = ((1-t)**3)*P0 + ((1-t)**2)*t*3*P1 + (1-t)*(t**2)*3*P2 + (t**3)*P3
    return B

# r'(t)
def dt_cubic(coords, t):
    #calculate first derivative at t from the explicit def of cubic bezier curve
    P0 = mathutils.Vector(coords[0])
    P1 = mathutils.Vector(coords[1])
    P2 = mathutils.Vector(coords[2])
    P3 = mathutils.Vector(coords[3])
    B_dt = ((1-t)**2)*3*(P1-P0) + (1-t)*t*6*(P2-P1) + (t**2)*3*(P3-P2)
    return B_dt
    
# r''(t)
def dt2_cubic(coords, t):
    #calculate first derivative at t from the explicit def of cubic bezier curve
    P0 = mathutils.Vector(coords[0])
    P1 = mathutils.Vector(coords[1])
    P2 = mathutils.Vector(coords[2])
    P3 = mathutils.Vector(coords[3])
    B_dt2 = (6*(1-t)*(P2-(2*P1)+P0) + 6*t*(P3-(2*P2)+P1))
    return B_dt2   

# r'''(t)
def dt3_cubic(coords, t):
    #calculate first derivative at t from the explicit def of cubic bezier curve
    P0 = mathutils.Vector(coords[0])
    P1 = mathutils.Vector(coords[1])
    P2 = mathutils.Vector(coords[2])
    P3 = mathutils.Vector(coords[3])
    B_dt3 = (6 * (P3 - (3*P2) + (3*P1) - P0))
    return B_dt3   
    
    
#calculate location at t using de Casteljau algorithm
def deCasteljau(coords, t):
    beta = [c for c in coords]
    n = len(beta)
    for i in range(0,n):
        for j in range(n-i):
            beta[j] = beta[j] * (1-t) + beta[j+1] *t
    return beta
    
    
def vectorMagnitude(vec):
    #get magnitude for vector
    x,y,z = vec
    return math.sqrt((x**2) + (y**2) + (z**2))
  
  
# T(t) = r'(t)/|r'(t)| - return unit tangent vector  
def tangent_cubic(coords, t):
    #calculate direction vector at point t
    vec = dt_cubic(coords, t)
    return vec/vectorMagnitude(vec)
    
# B(t)
def binormal_cubic(coords, t):
    r_dt = mathutils.Vector(dt_cubic(coords, t))
    r_dt2 = mathutils.Vector(dt2_cubic(coords, t))
    r = r_dt.cross(r_dt2)
    return r / vectorMagnitude(r)

# N(t)
def normal_cubic(coords, t):
    T = mathutils.Vector(tangent_cubic(coords, t))
    B = mathutils.Vector(binormal_cubic(coords, t))
    return T.cross(B)
        
# K(t) = |r' x r''|/|r'|^3 return curvature at point
def curvature_cubic(coords, t):
    r_dt = mathutils.Vector(dt_cubic(coords, t))
    r_dt2 = mathutils.Vector(dt2_cubic(coords, t))
    r = r_dt.cross(r_dt2)
    return vectorMagnitude(r) / vectorMagnitude(r_dt)**3


def torsion(coords, t):
    r_dt = mathutils.Vector(dt_cubic(coords, t))
    r_dt2 = mathutils.Vector(dt2_cubic(coords, t))
    r_dt3 = mathutils.Vector(dt3_cubic(coords, t))
    # scalar triple product
    num = r_dt.dot(r_dt2.cross(r_dt3))
    den = vectorMagnitude(r_dt.cross(r_dt2))**2
    return num/den

# This eq is missing element +((radius'/t)*B) but is close to correct point
def osculatingCenter(coords, t):
    # curvature, radius, x, torsion
    k = curvature_cubic(coords, t)
    r = 1/k
    x = cubic(coords, t)
    # find dir of curvature
    
    N = normal_cubic(coords, t) * -1

    return (r*N) + x
    
    
def moveSplinesTo_cubic(coords):
    #move cursor to origin
    bpy.context.scene.cursor_location = (0, 0, 0)
    bpy.ops.object.mode_set(mode='EDIT')
    curve = bpy.context.active_object
    
    bpy.ops.curve.handle_type_set(type='FREE_ALIGN')
    bpy.ops.curve.normals_make_consistent(calc_length=False)
    
    #get spline data from curve
    splines = curve.data.splines
    
    #create lists of endpoints and inner points
    endpoints = [coords[0], coords[len(coords)-1]]
    innerpoints = []
    for h in range(1, len(coords)-1):
        innerpoints.append(coords[h])
        print("Append to innerpoints: ", coords[h])
    
    size_i = len(splines)
    #move endpoints
    for i in range(0, size_i):
        #get point data from splines
        points = splines[i].bezier_points
        size_j = len(points)
        
        for j in range(0, size_j):
            #set points to pos vectors stored in endpoints list
            x, y, z = endpoints[j]
            a, b, c = innerpoints[j]
            points[j].co = (x, y, z)
            print("Spline", i, "Point", j, points[j].co)
            
            #set handles to pos vectors stored in innerpoints list
            points[j].handle_right = (a, b, c)
            points[j].handle_left = (a, b, c)
        
    bpy.ops.object.mode_set(mode='OBJECT')
    
    
def createBez_cubic(coords):
    for i in bpy.context.scene.objects:
        if i.name == 'myCurve':
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects['myCurve'].select = True
            bpy.ops.object.delete()

    bpy.ops.curve.primitive_bezier_curve_add()
    bpy.ops.object.mode_set(mode='OBJECT')
    curve = bpy.context.active_object
    curve.name = "myCurve"

    moveSplinesTo_cubic(coords)
    

def pointOnBez_cubic(coords, t):
    #create object at point on parametric (cubic bezier) curve, from points
    #create point at origin
    #mesh and object data:
    ob_name = "t = " + str(t) + " "
    me = bpy.data.meshes.new(ob_name + "Mesh")
    ob = bpy.data.objects.new(ob_name, me)
    #make a mesh from a list of vertices/edges/faces
    me.from_pydata([(0,0,0)], [], [])
    #display name and update the mesh
    ob.show_name = True
    me.update()
    #link object to the scene
    bpy.context.scene.objects.link(ob)
    
    bpy.ops.object.mode_set(mode='OBJECT')

    #calculate location of point at t
    B = cubic(coords, t)
    #move point to correct location
    ob.location = B 
    
def drawVector(coords, t, vec):
    ob_name = "t=" + str(t)
    me = bpy.data.meshes.new(ob_name + "Mesh")
    ob = bpy.data.objects.new(ob_name, me)
    #make a mesh from a list of vertices/edges/faces
    me.from_pydata([(0,0,0), vec], [(0,1)], [])
    #display name and update the mesh
    me.update()
    #link object to the scene
    bpy.context.scene.objects.link(ob)
    #move to location
    ob.location = cubic(coords, t)
    
    bpy.ops.object.mode_set(mode='OBJECT')

# Doesn't work
def drawOsculating(coords,t):
    c = osculatingCenter(coords,t)
    k = curvature_cubic(coords, t)
    r = 1/k
    
    sphere = bpy.ops.mesh.primitive_uv_sphere_add()
    bpy.context.scene.objects.active.location = c
    bpy.context.scene.objects.active.scale = (r, r, r)
    
#make copies on an object on path, 
#t = frequency 0<t<1 
#size = (1/k) 
def drawOnPath(coords, ob, t):
    return 0
    
    
    
    
