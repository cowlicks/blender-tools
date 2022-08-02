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
from scad import (obj_union, reset_blend, active, obj_diff, cylinder, export_stl, tube,
    z_max_to, x_max_to, x_max, rotate, vert_filter, obj_join, clear_plane, z_max,
    z_min_to, mirror_z, x_min_to, x_mid_to, bevel, rotate_around_cursor, z_mid_to,
    set_default_verticies, get_global_verticies, remove, cart_from_cylinder_coords
                  )

import datetime
thing_name = 'your-thing-name'

# clear the scene
reset_blend()

# set default verticices on a cylinder
# ~32 is good for development, 128 - 256 is good for printing
set_default_verticies(128)


# measurements in mm
inner_diameter = 125

# choosen parameters
wall_thickness = 3
height = 5

# derive constants

outer_diameter = inner_diameter + wall_thickness

# create your geometry
obj = tube(outer_diameter, inner_diameter, height)


# save your thing as an stl
print('processed @ ', datetime.datetime.now())
obj.select_set(True)
export_stl(thing_name)

