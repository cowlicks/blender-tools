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
from scad import (obj_union, reset_blend, active, obj_diff, cylinder, export_stl,
    z_max_to, x_max_to, x_max, rotate, vert_filter, obj_join, clear_plane, z_max,
    z_min_to, mirror_z, x_min_to, x_mid_to, bevel, rotate_around_cursor, z_mid_to,
    set_default_verticies, get_global_verticies, remove, cart_from_cylinder_coords,
    duplicate,
                  )

import datetime
thing_name = 'draintray'

reset_blend()
set_default_verticies(128)


# measurements in mm
diameter = 125
hole_diameter = 6
hole_radius = hole_diameter/2

radius = diameter / 2

# choosen
tray_depth = 13
floor_thickness = .8
wall_thickness = 2.5

n_holes = 3
n_ridges = 3
sigma =0.1

outer_radius = radius + wall_thickness

# base tray obj
obj = cylinder(radius=radius + wall_thickness, depth=tray_depth)

z_min_to(obj, 0)

indention = cylinder(radius=radius, depth=tray_depth*2)
z_min_to(indention, floor_thickness + sigma)

obj_diff(obj, indention)


# through hole obj
h2 = cylinder(radius=hole_radius, depth=2*tray_depth)
z_min_to(h2, -1)

through_hole_tube_height = tray_depth + floor_thickness
through_hole_tube_radius = (hole_radius + wall_thickness)
h3 = cylinder(radius=through_hole_tube_radius, depth=through_hole_tube_height)
z_min_to(h3, 0)
obj_diff(h3, h2)

# cuts out space for through hole
neg_hole = cylinder(radius=through_hole_tube_radius, depth=2*tray_depth)
z_min_to(neg_hole, -1)

for i in range(n_holes):
    hole_coords = cart_from_cylinder_coords(
        radius=(radius + through_hole_tube_radius),
        radians=((2*pi/n_holes) * i)
    )

    bpy.ops.object.select_all(action='DESELECT')
    hole_x = duplicate(neg_hole)

    hole_x.location[0] = hole_coords[0]
    hole_x.location[1] = hole_coords[1]
    obj_diff(obj, hole_x)


holes = []
for i in range(n_holes):
    hole_coords = cart_from_cylinder_coords(
        radius=(radius + through_hole_tube_radius),
        radians=((2*pi/n_holes) * i)
    )

    bpy.ops.object.select_all(action='DESELECT')
    hole_x = duplicate(h3)

    hole_x.location[0] = hole_coords[0]
    hole_x.location[1] = hole_coords[1]

    holes.append(hole_x)

obj = obj_join([obj, *holes])

# ridges
less_than_radius = hole_radius*3
ridge_offset = ((2*pi) / n_holes) / 2

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

print('join ridges')
obj_union(obj, obj_join(ridges))
print('joined')



z_min_to(obj, 0)
remove(h3)
remove(neg_hole)

# select all vertices with z > 0
def bev():
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

#bev()
print('processed @ ', datetime.datetime.now())
print('save')
obj.select_set(True)
export_stl(thing_name)
