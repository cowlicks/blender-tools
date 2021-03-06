#EXECUTE
'''
This should be copied and pasted into the script you are writing to enable live reloading of this script, and the scad library.
'''

from math import cos, sin, pi
import bpy, bmesh

import sys
# add the local directory to sys.path (so modules in '.' can be imported
# since we reload this file, don't re-add '.' if its already in sys.path
if ('.' not in sys.path):
    sys.path.append('.')

'''NB: the order is important. we import scad first, then reload it, so when
the the functions are imported from scad they are imported from the reloaded
module.
'''
# the local module
import scad
import importlib
# reload local module since we reload this interactively
importlib.reload(scad)

# re-load functions from the reloaded module
from scad import (obj_union, reset_blend, active, obj_diff, cylinder, cube, z_min, x_min,
    z_max_to, x_max_to, x_max, rotate, vert_filter, obj_join, clear_plane, z_max,
    z_min_to, mirror_z, x_min_to, x_mid_to, bevel, rotate_around_cursor, z_mid_to,
    set_default_verticies, get_global_verticies, remove,
                  )

import datetime

reset_blend()
set_default_verticies(32)


# measurements in mm
diameter = 6*25.4 # 4.5 inches
hole_diameter = 6
hole_radius = hole_diameter/2

radius = diameter / 2

# choosen
tray_depth = 10
floor_thickness = 2
wall_thickness = hole_diameter + 2*floor_thickness

n_holes = 3
n_ridges = 3
sigma =0.1

outer_radius = radius + wall_thickness

def cart_from_cylinder_coords(radius: float =0, radians: float =0, z: float =0):
    x = cos(radians) * radius
    y = sin(radians) * radius
    return x, y, z

#obj = cylinder(radius=outer_radius, depth=tray_depth)
obj = cylinder(radius=radius + wall_thickness/2, depth=tray_depth)

z_min_to(obj, 0)

indention = cylinder(radius=radius, depth=tray_depth*2)
z_min_to(indention, floor_thickness + sigma)

obj_diff(obj, indention)

h2 = cylinder(radius=hole_radius, depth=2*tray_depth)
z_min_to(h2, -1)

h3 = cylinder(radius=(hole_radius + floor_thickness)*.9, depth=(tray_depth+ floor_thickness))
z_min_to(h3, 0)
obj_diff(h3, h2)

neg_hole = cylinder(radius=hole_radius, depth=2*tray_depth)
z_min_to(neg_hole, -1)

print('create hole negatives')
for i in range(n_holes):
    hole_coords = cart_from_cylinder_coords(
        radius=((radius + outer_radius)/2),
        radians=((2*pi/n_holes) * i)
    )
    bpy.ops.object.select_all(action='DESELECT')
    neg_hole.select_set(True)
    bpy.context.view_layer.objects.active = neg_hole
    bpy.ops.object.duplicate()
    neg_hole_x = bpy.context.object
    neg_hole_x.location[0] = hole_coords[0]
    neg_hole_x.location[1] = hole_coords[1]
    obj_diff(obj, neg_hole_x)


print('create hole')
holes = []
for i in range(n_holes):
    hole_coords = cart_from_cylinder_coords(
        radius=((radius + outer_radius)/2),
        radians=((2*pi/n_holes) * i)
    )

    bpy.ops.object.select_all(action='DESELECT')
    h3.select_set(True)
    bpy.context.view_layer.objects.active = h3
    bpy.ops.object.duplicate()

    h_x = bpy.context.object
    h_x.location[0] = hole_coords[0]
    h_x.location[1] = hole_coords[1]

    holes.append(h_x)

print('join holes')
obj = obj_join([obj, *holes])

## ridges
less_than_radius = hole_radius*3
ridge_offset = ((2*pi) / n_holes) / 2
print('bevel')

print('add ridges')
ridges = []
for i in range(n_ridges):
    ridge = cylinder(
        depth=((radius - less_than_radius)),
        radius=floor_thickness * .8,
        )

    rotate(ridge, 1, rads=(pi/2))
    x_min_to(ridge, less_than_radius/2)
    rotate_around_cursor(ridge, ((2*pi)/n_ridges) * i + ridge_offset, 2)
    z_mid_to(ridge, floor_thickness)
    ridges.append(ridge)
    #obj_union(obj, ridge)

print('join ridges')
obj_union(obj, obj_join(ridges))
print('joined')



z_min_to(obj, 0)
remove(h3)
remove(neg_hole)

bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.select_mode(type='VERT')
bpy.ops.mesh.select_all(action = 'DESELECT')
bpy.ops.object.mode_set(mode = 'OBJECT')

print('selcting top vertices')
for (i, v) in enumerate(get_global_verticies(obj)):
    if (v[2] > sigma):
        obj.data.vertices[i].select = True

bpy.ops.object.mode_set(mode = 'EDIT')
print('beveling top verts')
bpy.ops.mesh.bevel(offset=.5,
                   segments=4,
                   affect='EDGES')

print('processed @ ', datetime.datetime.now())
print('save')
obj.select_set(True)
bpy.ops.export_mesh.stl(filepath='/home/blake/git/mason-blend/draintray.stl',
                        use_selection=True,
                        )
