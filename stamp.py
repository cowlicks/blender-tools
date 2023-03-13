#EXECUTE

'''
This should be copied and pasted into the script you are writing to enable live reloading of this script, and the scad library.
'''

import math
from math import cos, sin, pi
import bpy, bmesh
from pprint import pprint as print
import decimal

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
from scad import (obj_union, origin_to_3d_center, reset_blend, active, obj_diff, cylinder, cube, z_min, x_min,
    z_max_to, x_max_to, x_max, rotate, vert_filter, obj_join, clear_plane, z_max,
    z_min_to, mirror_z, x_min_to, x_mid_to, bevel, rotate_around_cursor, z_mid_to,
    y_min_to, y_mid_to, y_max_to, select_edges_filter,
    set_default_verticies, get_global_verticies, remove,
    duplicate, export_stl, select_vertices, scale,
                  )

import datetime

reset_blend()
set_default_verticies(256)

sigma = 10**-2
thing_name = 'stamp'

radius=22                               # outer radius
rim_thickness = 5                       # outer radius - inner radius
inner_radius = radius - rim_thickness   # inner radius


# line width is:    (ring_height - (2 * ring_offset)) * z_zcale
# line spacing is:  (2 * ring_offset) * z_scale
# inset radius is:  ring_offset

# so the angle of the print is angle = atan((ring_offset * z_scale)/ring_offset)
# or angle = atan(z_scale)

# or tan(angle) = z_scale

# if we reqire line_width == line_space
# ring_height - 2*ring_off = 2*ring_off
# so we require
# ring_height = 4*ring_off

# and we want line_width = 1 = (ring_height - (2 * ring_offset)) * z_scale
# lw = (4*ring_off - (2*ring_off)) * z_scale
# ring_off = lw/(2*z_scale)

#line_width = 1
#angle = 3/4
#
#z_scale = math.tan(angle)
#ring_offset = line_width / (2 * z_scale)
#ring_height = 4*ring_offset

# used for calculating bevels.
# line_width: equals the desired height of the beveled or non-beveled part (they are the same)
# angle: the angle of the beveled part
# outputs:
# ring height: height of face before bevel and scale
# ring_offset: passed to bevel
# z_scale: scales the final part
# angle in radians
def offset_height_and_z_scale_from_angle_and_line_width(line_width, angle):
    z_scale = math.tan(angle)
    ring_offset = line_width / (z_scale)
    ring_height = 2*ring_offset
    return (ring_height, ring_offset, z_scale)

# ring_off = 1 / (2 * z_scale)

# total number of stacked rings
n_rings = 12

line_width = 1
angle_radians = math.pi/8
angle_radians *= 3/4

# same as lw = 1, angle = math.pi/8
#ring_height = 4                         # single segment height
#ring_offset = 1                         # length on x or y of bevel cut
#z_scale = .50

(ring_height, ring_offset, z_scale) = offset_height_and_z_scale_from_angle_and_line_width(
    line_width, angle_radians
)
##print(ring_offset)
##print(ring_offset)
##print(z_scale)



# same as lw = 1, angle = math.pi/8
#ring_height = 4                         # single segment height
#ring_offset = 1                         # length on x or y of bevel cut
#z_scale = .50


# for setting total height. calculates n_rings for you
#total_height = 122
#n_rings = total_height // ring_height  # for setting total height

def  make_ring():
    obj = cylinder(radius=radius, depth=ring_height)

    def foo(i, v):
        print(f'{i}, {v}')
        return v[2] > sigma

    #select_vertices(obj, foo)

    #bpy.ops.mesh.bevel(offset=ring_offset, segments=1, affect='EDGES')

    select_vertices(obj, lambda _i, v: v[2] < sigma)

    bpy.ops.mesh.bevel(offset=ring_offset, segments=1, affect='EDGES')
    return obj

def make_rings():
    rings = []
    height = None
    #for i in range(6):
    for i in range(n_rings):
        r = make_ring()
        if height is None:
            z_min_to(r, 0)
        else:
            z_min_to(r, height)
        height = z_max(r)
        rings.append(r)

    return obj_join(rings)

rings = make_rings()
## uncomment
#rings = make_rings()
#
z_min_to(rings, 0)
origin_to_3d_center(rings)
# scale down
scale((1, 1, z_scale))
#
#
cutout = cylinder(radius=inner_radius, depth=(ring_height*n_rings*3))
obj_diff(rings, cutout)

print('done')
#build_tray()
export_stl(thing_name)
print(f'exported {thing_name}')

