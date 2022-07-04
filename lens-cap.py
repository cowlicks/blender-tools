#EXECUTE
from pprint import pprint as print
'''
This should be copied and pasted into the script you are writing to enable live reloading of this script, and the scad library.
'''

from math import pi
from scad import (reset_blend, obj_diff, cylinder, cube, z_max_to, rotate,
                  obj_join, z_min_to, x_mid_to, rotate_around_cursor,
                  set_default_verticies, duplicate, tube, export_stl)
reset_blend()
set_default_verticies(128)

thing_name = 'lens-cap'

# mamiya press f3.5 100mm measurements for front and back
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

export_stl(thing_name)
