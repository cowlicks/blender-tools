#EXECUTE
import math
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
    y_min_to, y_mid_to, y_max_to, select_edges_filter,
    set_default_verticies, get_global_verticies, remove,
    duplicate, export_stl,
                  )

import datetime

reset_blend()
set_default_verticies(10)

sigma = 10**-3
thing_name = 'change-sorter'

quarter_diameter = 23.9
nickel_diameter = 21.1
penny_diameter = 18.8
dime_diamer = 17.7

coins = [
    quarter_diameter,
    nickel_diameter,
    penny_diameter,
    dime_diamer,
]

coin_hole_diameter = (quarter_diameter + nickel_diameter) / 2
coin_hole_radius = coin_hole_diameter/2
half_coin_seperation = coin_hole_radius * .25

tray_skin_depth = 2
tray_length = (quarter_diameter + 2*half_coin_seperation)*3 # for draft
tray_length = (quarter_diameter + 2*half_coin_seperation)*5
tray_width = tray_length
tray_depth = 10 # for draft
tray_depth = 20


tray_i_length = tray_length - tray_skin_depth*2
tray_i_width = tray_width - tray_skin_depth*2

tray = cube(size=1, length=tray_length, width=tray_length, height=tray_depth)
z_min_to(tray, 0)
tray_hole = cube(size=1, length=tray_i_length, width=tray_i_width, height=tray_depth)
z_min_to(tray_hole, tray_skin_depth)

obj_diff(tray, tray_hole)

def cut_coin_hole(x, y):
    coin_hole = cylinder(radius=coin_hole_radius, depth=3*tray_skin_depth)
    z_min_to(coin_hole, 0 - sigma)
    x_mid_to(coin_hole, x)
    y_mid_to(coin_hole, y)
    obj_diff(tray, coin_hole)

coin_grid_size = (coin_hole_diameter + 2*half_coin_seperation)
n_length_coins = int(tray_i_length // coin_grid_size)
length_remainder = tray_i_length - (n_length_coins*coin_grid_size)
n_width_coins = int(tray_i_width // coin_grid_size)
width_remainder = tray_i_width - (n_width_coins*coin_grid_size)

print(f'n length coins {n_length_coins}')
for x_i in range(n_length_coins):
    for y_i in range(n_width_coins):
        x = x_i*coin_grid_size - tray_i_length/2 + half_coin_seperation + coin_hole_radius + length_remainder/2
        y = y_i*coin_grid_size - tray_i_width/2 + half_coin_seperation + coin_hole_radius + width_remainder/2
        print(f'cutting hole at ({x}, {y})')
        cut_coin_hole(x, y)


export_stl(thing_name)
