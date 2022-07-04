#EXECUTE
from pprint import pprint as print
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
    y_min_to, y_max_to, select_edges_filter,
    set_default_verticies, get_global_verticies, remove,
    duplicate,
                  )

import datetime

reset_blend()
set_default_verticies(128)

thing_name = 'lens-cap'

# mamiya press f3.5 100mm
#lens_id = 57.1         # front
#skin_depth= 1.6        # front
#lens_cap_depth=8.4     # front
#lens_id = 77.6         # back
#skin_depth= 2.7        # back
#lens_cap_depth=14.4    # back
lens_id = 77.7         # back
skin_depth= 2.7        # back
skin_depth= 2
lens_cap_depth=14.4    # back

lens_od = lens_id + skin_depth*2

import os
def export_stl(name=thing_name, location=None):
    location = location or os.path.join(os.path.dirname(os.path.realpath(__file__)), f'{thing_name}.stl')
    bpy.ops.export_mesh.stl(filepath=location)

def tube(outer_diameter: float, inner_diameter: float, length: float):
    obj = cylinder(radius=outer_diameter/2, depth=length)
    obj_diff(obj,
             cylinder(radius=inner_diameter/2, depth=length*2),
             )
    return obj

# main cover
out_obj = cylinder(radius=lens_od/2, depth=lens_cap_depth)
in_obj = cylinder(radius=lens_id/2, depth=lens_cap_depth)
z_min_to(out_obj, 0)
z_min_to(in_obj, skin_depth)
obj_diff(out_obj, in_obj)

eh_thickness_factor = 1.4
eh_thickness = skin_depth*eh_thickness_factor
eh_diameter = lens_cap_depth*2 - eh_thickness


# hole for attachments
eye_hole = tube(outer_diameter=eh_diameter, inner_diameter=eh_diameter-eh_thickness*2, length=eh_thickness)
z_min_to(eye_hole, 0)
rotate(eye_hole, 0, pi/2)

eye_hole_face = tube(outer_diameter=eh_diameter, inner_diameter=eh_diameter-eh_thickness*2, length=eh_thickness)
z_min_to(eye_hole_face, 0)

eye_hole = obj_join([eye_hole, eye_hole_face])

remove_frome_eye = cube(size=100)
z_max_to(remove_frome_eye, 0)
obj_diff(eye_hole, remove_frome_eye)
x_mid_to(eye_hole, lens_od/2)
z_min_to(eye_hole, 0)

rm_from_eh = cylinder(radius=lens_od/2, depth=lens_cap_depth*2)
z_min_to(rm_from_eh, 0)
obj_diff(eye_hole, rm_from_eh)

other_eye2 = duplicate(eye_hole)
rotate_around_cursor(other_eye2, 2*pi*(1/3), 2)
other_eye3 = duplicate(other_eye2)
rotate_around_cursor(other_eye3, 2*pi*(1/3), 2)
obj_join([out_obj, eye_hole, other_eye2, other_eye3])

export_stl()
