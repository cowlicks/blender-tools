import bpy

def reset_blend():
    for o in bpy.data.objects:
        print(f'removing existing object named: {o.name}')
        bpy.data.objects.remove(o, do_unlink=True)

def active():
    return bpy.context.object

def obj_diff(a_obj, b_obj, remove_other=True, use_hole_tolerant=True, use_self=True):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = a_obj
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.context.object.modifiers['Boolean'].operation = 'DIFFERENCE'
    bpy.context.object.modifiers['Boolean'].use_hole_tolerant = use_hole_tolerant
    bpy.context.object.modifiers['Boolean'].use_self = use_self
    bpy.context.object.modifiers["Boolean"].object = b_obj
    bpy.ops.object.modifier_apply(modifier="Boolean")
    if remove_other:
        bpy.data.objects.remove(b_obj, do_unlink=True)

def obj_intersect(a_obj, b_obj, remove_other=True, use_hole_tolerant=True, use_self=True):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = a_obj
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.context.object.modifiers['Boolean'].operation = 'INTERSECT'
    bpy.context.object.modifiers['Boolean'].use_hole_tolerant = use_hole_tolerant
    bpy.context.object.modifiers['Boolean'].use_self = use_self
    bpy.context.object.modifiers["Boolean"].object = b_obj
    bpy.ops.object.modifier_apply(modifier="Boolean")
    if remove_other:
        bpy.data.objects.remove(b_obj, do_unlink=True)

def rotate(obj, axis, rads):
    bpy.ops.object.mode_set(mode = 'EDIT')
    obj.rotation_euler[axis] = rads
    bpy.ops.object.mode_set(mode = 'OBJECT')

def mirror_axis_i(i):
    bpy.ops.object.duplicate()
    bpy.context.object.location[i] = -bpy.context.object.location[i]
    return active()

def mirror_x():
    return mirror_axis_i(0)

def mirror_y():
    return mirror_axis_i(1)

def mirror_z():
    return mirror_axis_i(2)

def extreme_coordinates(obj) -> list[list[float]]:
    '''Return the extreme coordinates of an object in the form:
    [[min_x, max_x], [min_y, max_y], [min_z, max_z]]
    '''
    out = [[None, None], [None, None], [None, None]]
    for v in obj.data.vertices:
        global_vert = (obj.matrix_world @ v.co)
        for (i, val) in enumerate(global_vert):
            cur_min = out[i][0]
            cur_max = out[i][1]
            out[i][0] = min(val, cur_min if cur_min is not None else val)
            out[i][1] = max(val, cur_max if cur_max is not None else val)

    return out

def get_global_verticies(obj):
    return [obj.matrix_world @ v.co for v in obj.data.vertices]

def vert_filter(obj, func):
    return filter(func, get_global_verticies(obj))


def z_min(obj):
    return extreme_coordinates(obj)[2][0]

def z_max(obj):
    return extreme_coordinates(obj)[2][1]

def axis_extreme_to(obj, axis, extreme, target):
    bpy.ops.object.mode_set(mode = 'EDIT')
    ext_value = extreme_coordinates(obj)[axis][extreme]
    obj.location[axis] = (obj.location[axis] + target - ext_value)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    return active()

def axis_mid_to(obj, axis, target):
    [min_, max_] = extreme_coordinates(obj)[axis]
    length = max_ - min_
    axis_extreme_to(obj, axis, 0, target - length/2)

def x_min_to(obj, x=0):
    axis_extreme_to(obj, 0, 0, x)
def x_max_to(obj, x=0):
    axis_extreme_to(obj, 0, 1, x)
def x_mid_to(obj, x=0):
    return axis_mid_to(obj, 0, x)

def y_min_to(obj, y=0):
    axis_extreme_to(obj, 1, 0, y)
def y_max_to(obj, y=0):
    axis_extreme_to(obj, 1, 1, y)
def y_mid_to(obj, y=0):
    return axis_mid_to(obj, 1, y)

def z_min_to(obj, z=0):
    axis_extreme_to(obj, 2, 0, z)
def z_max_to(obj, z=0):
    axis_extreme_to(obj, 2, 1, z)
def z_mid_to(obj, z=0):
    return axis_mid_to(obj, 2, z)

def x_min(obj):
    return extreme_coordinates(obj)[0][0]

def x_max(obj):
    return extreme_coordinates(obj)[0][1]

def obj_join(objs):
    bpy.ops.object.select_all(action='DESELECT')

    for obj in objs:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
    bpy.ops.object.join()
    return active()


def cylinder(radius=1, depth=1, location=(0, 0, 0), scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius,
                                        depth=depth,
                                        location=location,
                                        scale=scale,
                                        enter_editmode=False, align='WORLD',
                                        )
    return active()

def cube(size=2, location=(0, 0, 0),
         length=1,
         width=1,
         height=1,
         ):
    bpy.ops.mesh.primitive_cube_add(
        size=size,
        location=location,
        scale=(length, width, height),
        enter_editmode=False,
        align='WORLD',
    )
    return active()

def clear_plane(obj, axis: int, sign: bool, plane_location=0, size=1000):
    c = cube(length=size, width=size, height=size)
    axis_extreme_to(c, axis, int(sign), plane_location)
    obj_diff(obj, c)

#if __name__ == '__main__':
reset_blend()
s=100
cube(length=s, width=s, height=s)
    