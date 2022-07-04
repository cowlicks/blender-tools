Herein lie tools for building models using Blender's Python API, and a [bunch](lens-cap.py) [of](draintray.py) [scripts](change-sorter.py) that create models.

The tools are part of a rather specific workflow which is intended to imitate [OpenSCAD](https://openscad.org/), where you can edit a file (in your own editor) and it is updated on the fly in Blender. This includes an [addon](Script-LiveLink_V21.py) for handling file reloading. And a [library](scad.py) which contains functions for creating handling meshes.

Below a short demonstration of me editing parameters of a python script in Vim, and the updating live in Blender.
The script generates a lens cap I 3D printed and used for my Camera.
The script is written so that I can just change some values (like the lens diameter) to adjust it's size,
so I can easily make another lens cap for other lenses.

[Screencast from 07-04-2022 03:28:24 PM.webm](https://user-images.githubusercontent.com/598099/177213774-7a372178-d986-40f3-b508-a27124327318.webm)

# Usage

You must first [install](https://docs.blender.org/manual/en/latest/editors/preferences/addons.html#installing-add-ons) and [enable](https://docs.blender.org/manual/en/latest/editors/preferences/addons.html#enabling-disabling-add-ons) the [`Script-LiveLink_V21.py` addon](Script-LiveLink_V21.py) to blender.

Create a python file in this directory, alongside the [`scad.py`](scad.py) file. The first line MUST start with `#EXECUTE`. This is an example file that generates a cube.

```python
#EXECUTE  # This MUST be on the first line

from scad import reset_blend, cube, export_stl

# this file is run everytime we save, so we should delete the existing objects each time
reset_blend()

# your code here
cube(size=25)

# save the cube
export_stl('my-cube')
```
![image](https://user-images.githubusercontent.com/598099/177218836-20391fe6-a1c9-4ba8-8bfc-d7e6adf0afa6.png)


Then go to "Scripting" tab. On the right hand side of the "Editor" panel should see the LiveLink side tab (you may need to expand the tab). There you can execute the script, or click "Start LiveLink" to have it run automatically on save.

# Why?

## Why not OpenSCAD?
OpenSCAD is great for what it does. But because it uses it own domain-specific language, we can't easily use libraries  written in other languages. This workflow allows us to use Python, which means we can leverage a whole world of libraries, and in-turn include our code into other projects.

## Why not use Blender's built in Script editor?
As programmers we spend so much time learning how to be more productive with our own favorite editor, it really suck having to switch to the one integrated in Blender.

## Why not just model things directly in Blender

Writing a script to generates a model means that my final model is easily parameterized by the measurements that make it up. 
