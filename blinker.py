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
                  )

import datetime

reset_blend()
set_default_verticies(64)


# measurements
play = 1.0
cap_od = 28.5
#post_id = 7.
total_post_length = 83.
end_cap_length = 16.1

#mid_post_od = 22.6 

# faster printing
#end_cap_length = 6
post_id = 9
mid_post_od = 20
mid_post_length = total_post_length - (end_cap_length * 2)

sigma =0.1

tab_length = 7. + play
tab_width = 1. + play
tab_height = 4.2 + play
tab_to_tab_outside = 21.6 + play


def end_cap():
    y_tab = cube(size=1, length=tab_length, width=tab_width, height=tab_height)


    bpy.ops.object.select_all(action='DESELECT')
    y_tab.select_set(True)
    bpy.context.view_layer.objects.active = y_tab
    bpy.ops.object.duplicate()

    y_max_to(y_tab, tab_to_tab_outside/2)

    x_tab = bpy.context.object
    rotate(x_tab, 2, rads=(pi/2))
    x_max_to(x_tab, tab_to_tab_outside/2)

    bpy.ops.object.select_all(action='DESELECT')
    y_tab.select_set(True)
    bpy.context.view_layer.objects.active = y_tab
    bpy.ops.object.duplicate()
    y_neg_tab = bpy.context.object

    y_min_to(y_neg_tab, -tab_to_tab_outside/2)

    bpy.ops.object.select_all(action='DESELECT')
    x_tab.select_set(True)
    bpy.context.view_layer.objects.active = x_tab
    bpy.ops.object.duplicate()
    x_neg_tab = bpy.context.object
    x_min_to(x_neg_tab, -tab_to_tab_outside/2)

    tabs = obj_join([x_tab, x_neg_tab, y_tab, y_neg_tab])
    z_max_to(tabs, end_cap_length/2 + sigma)

    post = cylinder(radius=cap_od/2, depth=end_cap_length)
    post_hole = cylinder(radius=post_id/2, depth=end_cap_length + sigma)
    obj_diff(post, post_hole)
    obj_diff(post, tabs)


    def selector(edge):
        v_start = post.data.vertices[edge.vertices[0]]
        v_stop = post.data.vertices[edge.vertices[1]]
        start_r = (v_start.co[0]**2 + v_start.co[1]**2)**.5
        stop_r = (v_stop.co[0]**2 + v_stop.co[1]**2)**.5
        r_bound = cap_od/2 - sigma
        smallest_z = max(
            v_start.co[2],
            v_stop.co[2]
                         )
        return start_r >= r_bound and stop_r >= r_bound and smallest_z < 0

    select_edges_filter(post, selector)
    bpy.ops.mesh.bevel(offset=7, segments=12, affect='EDGES')
    return post



post = cylinder(radius=mid_post_od/2, depth=total_post_length - end_cap_length*2 + 3)
post_hole = cylinder(radius=post_id/2, depth=total_post_length + sigma)
obj_diff(post, post_hole)
cap = end_cap()
z_min_to(cap, mid_post_length/2 - sigma)
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = cap
cap.select_set(True)
bpy.ops.object.duplicate()
bottom_cap = active()
rotate_around_cursor(bottom_cap, pi, 0)

obj = obj_join([cap, post, bottom_cap])
