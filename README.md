# Live Coding for Blender

Herein lie tools for *interactively* building 3D models using Blender's Python API.

You write code, in your favorite editor, and see the model updated when the file saved.
If you want to design a 3D model and:
* Have all the power general purpose programming language
* Have all the power of a mature 3D modeling application
* Have a tight feedback loop aka "live coding"
* Use your favorite text editor

Then I think this is the only existing way to do it, [right?](#Contributing)

Below a simple demonstration of editing a python script in Vim, showing the model updating live in Blender.

The script creates a lens cap I 3D printed for my Camera.
The models dimensions (like its diameter) are parameterized by some variables in the script.
I edit them, save the file, and see the lens update automatically in Blender.

[Screencast from 07-04-2022 03:28:24 PM.webm](https://user-images.githubusercontent.com/598099/177213774-7a372178-d986-40f3-b508-a27124327318.webm)

# Usage

You must first [install](https://docs.blender.org/manual/en/latest/editors/preferences/addons.html#installing-add-ons) and [enable](https://docs.blender.org/manual/en/latest/editors/preferences/addons.html#enabling-disabling-add-ons) the [`Script-LiveLink_V21.py` addon](Script-LiveLink_V21.py) to blender.

At this point, you should close blender and start it from the command line is this repo.
This allows blender resolve relative paths is these files, and allows you to see things printed stdout from python scripts.

Then go to "Scripting" tab. On the right hand side of the "Editor" panel should see the LiveLink side tab (you may need to expand the tab). There you can execute the script, or click "Start LiveLink" to have it run automatically on save. Shown below:
![image](https://user-images.githubusercontent.com/598099/177218836-20391fe6-a1c9-4ba8-8bfc-d7e6adf0afa6.png)

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

If you'd like to edit the `scad.py` file (or any other file) and have its changes take effect on the fly, you can add this prelude to your model script.
```python
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

# finally re-load functions from the reloaded module
from scad import * # or whatever your named functions are
```

# Tips

* Blender GUI interactions are recorded in the scripting tab. So you can create a file with the GUI, then copy-and-paste the code from the scripting tab to a file, and edit it.
* the [`reloadprelude.py`](reloadprelude.py) file has a demonstration of using an external python environmen, for if you need dependencies like NumPy.


# Why?

## Why not OpenSCAD?

OpenSCAD is great for what it does. But because it uses it own domain-specific language, we can't easily use libraries  written in other languages. This workflow allows us to use Python, which means we can leverage a whole world of libraries, and in-turn include our code into other projects.

## Why not use Blender's built in Script editor?

From my own selfish perspective: I want to use my own editor.
From a wider perspective, tools are better whene they are agnostic to editor, IDE, etc.

## Why write code instead of using Blender's GUI?

Writing a script to generates a model means that my final model is easily parameterized by the measurements that make it up.

# Contributing

Email me or create an issue if you have questions comments or concerns :yum:

# This should not exist

This is a hack. Blender could and should make this workflow easier. But, I haven't even asked them too yet. I guess I'll start [here](https://blender.stackexchange.com/questions/1190/best-place-to-put-feature-requests). [Contact me](#Contributing) if you want to help.

