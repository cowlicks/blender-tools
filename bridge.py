#EXECUTE
import math
import bpy, bmesh
from math import pi, sin

'''
This pattern, from `import sys` to `importlib.reload` is how we interactively reload the scad library.
'''

# add the local directory to sys.path (so modules in '.' can be imported
import sys
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

from scad import (
    cube, reset_blend, cylinder, rotate, vert_filter,
    z_mid_to, x_mid_to, obj_diff, z_min
)

import bpy
import bmesh
import math

try:
    run_count
except NameError:
    run_count = 0
else:
    run_count += 1

EPLSILON = 1e-5
# ------------------------------------------------------------------------------
# Utility Functions

def object_from_data(verts, faces, name='shape', scene=None, select=True):
    """ Create a mesh object and link it to a scene """

    scene = scene if scene is not None else bpy.context.scene
    scene = scene if scene is not None else bpy.context.scene

    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update(calc_edges=True)              # Update mesh with new data
    mesh.validate(verbose=True)


    obj = bpy.data.objects.new(name, mesh)
    scene.collection.objects.link(obj)

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)


    return obj

reset_blend()

length = 79.26
width = 5.24
top_width = 3.4
height = 16.1

top_length = 65.35
top_side_indention = (length - top_length) / 2


def bridge_frame():
    verts = [
        (0, 0, 0),
        (top_side_indention, 0, height),
        (0, width, 0),
        (top_side_indention, top_width, height),
        (length, 0, 0),
        (length - top_side_indention, 0, height),
        (length, width, 0),
        (length - top_side_indention, top_width, height),
    ]

    faces = [
        [0, 2, 6, 4],
        [1, 3, 7, 5],
        [0, 1, 3, 2],
        [4, 5, 7, 6],
        [0, 1, 5, 4],
        [2, 3, 7, 6],
    ]
    return object_from_data(verts, faces)



def string(dia, x):
    o = cylinder(radius=dia/2, depth=width*4, vertices=64)
    rotate(o, 0, pi/2)
    z_mid_to(o, height - EPLSILON)
    #z_mid_to(o, height)
    x_mid_to(o, x - EPLSILON)
    return o

WHICH_WAY_DOES_BRIDGE_GO = +1 # WHICH WAY DOES BRIDGE GO +/- 1 to reverse strings left to right

str_spacing = 10.2
middle = length / 2

two_str = .55
third_str = .65
fith_and_first_str = .44
fourth_str = .86

def make_bridge(wwdbg):
    one_str_loc = middle + wwdbg*2*str_spacing
    two_str_loc = middle + wwdbg*str_spacing
    third_str_loc = middle
    fourth_str_loc = middle - wwdbg*str_spacing
    fith_str_loc = middle - wwdbg*2*str_spacing

    b = bridge_frame()
    obj_diff(b, string(fith_and_first_str, one_str_loc))
    obj_diff(b, string(two_str, two_str_loc))
    obj_diff(b, string(third_str, third_str_loc))
    obj_diff(b, string(fourth_str, fourth_str_loc))
    obj_diff(b, string(fith_and_first_str, fith_str_loc))

    #min_z = z_min(b)
    #map(lambda v: v.select_set(True), vert_filter(b, lambda v: v[2] == min_z))

    return b

one = make_bridge(-1*WHICH_WAY_DOES_BRIDGE_GO)
