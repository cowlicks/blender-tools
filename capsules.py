#EXECUTE

'''
This should be copied and pasted into the script you are writing to enable live reloading of this script, and the scad library.
'''

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
from scad import (obj_union, reset_blend, active, obj_diff, cylinder, cube, z_min, x_min,
    z_max_to, x_max_to, x_max, rotate, vert_filter, obj_join, clear_plane, z_max,
    z_min_to, mirror_z, x_min_to, x_mid_to, bevel, rotate_around_cursor, z_mid_to,
    y_min_to, y_mid_to, y_max_to, select_edges_filter,
    set_default_verticies, get_global_verticies, remove,
    duplicate, export_stl,
                  )

import datetime

reset_blend()
set_default_verticies(16)

sigma = 10**-3
thing_name = 'capsules'


body_diameter = 7.8
body_radius = body_diameter/2
half_hole_seperation = body_radius * .25
tray_depth = 15
tray_depth *= 0.5
tray_side = 50
wall_thickness=2
wall_height=tray_depth*3

def space_chunks(chunk_width, width, chunk_sep=None):
    chunk_sep = chunk_sep or chunk_width * 0.25

    if width <= chunk_width:
        raise ValueError("not enough space for a single chunk!")

    n_chunks = width // (chunk_width + chunk_sep)
    x = (chunk_width + chunk_sep) * n_chunks

    if x + chunk_width <= width:
        n_chunks += 1

    side_spacing = (width - (n_chunks * chunk_width + (n_chunks - 1) * chunk_sep)) / 2
    x = side_spacing + chunk_width/2

    yield x

    n_chunks -= 1

    while n_chunks:
        x += chunk_sep + chunk_width
        yield x
        n_chunks -= 1


def drange(x, y, jump):
  x = decimal.Decimal(x)
  y = decimal.Decimal(y)
  while x < y:
    yield float(x)
    x += decimal.Decimal(jump)

def diameter_test():
    tray = cube(size=1, length=tray_side, width=14, height=tray_depth)
    z_min_to(tray, 0)
    def cut_holes(rad, x, y):
        hole = cylinder(radius=rad, depth=3*tray_depth)
        z_min_to(hole, 0 - sigma)
        x_mid_to(hole, x)
        y_mid_to(hole, y)
        obj_diff(tray, hole)

    radius = body_radius
    print(f'initial body radius {radius}')
    for (i, x) in enumerate(drange(-tray_side/2 + body_diameter, tray_side/2 - body_diameter, body_diameter*1.3)):
        print(f'cutting hole i = {i} r = {radius}')
        radius += 0.02
        cut_holes(radius, x, 0)
    print('done cutting holes')

diameter_test()
def tray():
    tray = cube(size=1, height=tray_depth, length=tray_side, width=tray_side)
    for x in space_chunks(body_diameter, tray_side, chunk_sep=body_diameter*.5):
        x -= tray_side/2
        for y in space_chunks(body_diameter, tray_side, chunk_sep=body_diameter*.5):
            print(f'x ={x} y = {y}')
            y -= tray_side/2
            hole = cylinder(radius=body_radius, depth=3*tray_depth)
            x_mid_to(hole, x)
            y_mid_to(hole, y)
            obj_diff(tray, hole)

    walls = cube(size=1, length=tray_side + wall_thickness*2, width=tray_side + wall_thickness*2, height=wall_height)
    wall_cut = cube(size=1, length=tray_side, width=tray_side, height=wall_height*3)
    obj_diff(walls, wall_cut)

#tray()


#def build_tray():
#    tray_skin_depth = 2
#    tray_length = (body_diameter + 2*half_hole_seperation)*3 # for draft
#    tray_length = (body_diameter + 2*half_hole_seperation)*5
#    tray_width = tray_length
#    tray_depth = 10 # for draft
#    tray_depth = 20
#
#    tray_i_length = tray_length - tray_skin_depth*2
#    tray_i_width = tray_width - tray_skin_depth*2
#
#    tray = cube(size=1, length=tray_length, width=tray_length, height=tray_depth)
#    z_min_to(tray, 0)
#    tray_hole = cube(size=1, length=tray_i_length, width=tray_i_width, height=tray_depth)
#    z_min_to(tray_hole, tray_skin_depth)
#
#    obj_diff(tray, tray_hole)
#
#    def cut_holes(x, y):
#        hole = cylinder(radius=body_radius, depth=3*tray_skin_depth)
#        z_min_to(hole, 0 - sigma)
#        x_mid_to(hole, x)
#        y_mid_to(hole, y)
#        obj_diff(tray, hole)
#
#    grid_size = (body_diameter + 2*half_hole_seperation)
#    n_length_holes = int(tray_i_length // grid_size)
#    length_remainder = tray_i_length - (n_length_holes*grid_size)
#    n_width_holes = int(tray_i_width // grid_size)
#    width_remainder = tray_i_width - (n_width_holes*grid_size)
#
#    print(f'n length holes {n_length_holes}')
#    for x_i in range(n_length_holes):
#        for y_i in range(n_width_holes):
#            x = x_i*grid_size - tray_i_length/2 + half_hole_seperation + body_radius + length_remainder/2
#            y = y_i*grid_size - tray_i_width/2 + half_hole_seperation + body_radius + width_remainder/2
#            print(f'cutting hole at ({x}, {y})')
#            cut_holes(x, y)

export_stl(thing_name)
