import bpy

P0 = bpy.data.objects["P0"]
P1 = bpy.data.objects["P1"]
P2 = bpy.data.objects["P2"]
P3 = bpy.data.objects["P3"]
    
#create array containing location of points
list = [P0.location, P1.location, P2.location, P3.location]
print(list)

list_prop = bpy.props.CollectionProperty(name='Bezier Coordinate List')