#EXECUTE
'''
This should be copied and pasted into the script you are writing to enable live reloading of this script, and the scad library. The #EXECUTE above indicates to the live-link addon that this file should be run.
'''

import bpy, bmesh

import sys
# add the local directory to sys.path (so modules in '.' can be imported
# since we reload this file, don't re-add '.' if its already in sys.path
if ('.' not in sys.path):
    sys.path.append('.')

# This is how we'd include python dependencies from a local python environment
# in the current directory that was created with `python -m venv venv`. This is
# useful if we want NumPy, or use an external script that has external
# dependencies.
#venv_path = './venv/lib/python3.10/site-packages'
#if (venv_path not in sys.path):
#    sys.path.append(venv_path)

# NB: the order is important. we import scad first, then reload it, so when
# the the functions are imported from scad they are imported from the reloaded
# module. This is so we can edit the scad.py file, and get those updates on the next save of the <thing>.py file

# the local module
import scad
import importlib
# reload local module since we reload this interactively
importlib.reload(scad)

# re-load functions from the scad.py module
#from scad import (reset_blend, active, obj_diff, cylinder, cube, z_min, x_min,
#    z_max_to, x_max_to, x_max, rotate, vert_filter, obj_join, clear_plane, z_max,
#    z_min_to, mirror_z, x_min_to, x_mid_to)
#
#reset_blend()
