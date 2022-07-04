Herein lie tools for building models using Blender's Python API, and a [bunch](lens-cap.py) [of](draintray.py) [scripts](change-sorter.py) that create models.

The tools are part of a rather specific workflow which is intended to imitate [OpenSCAD](https://openscad.org/), where you can edit a file (in your own editor) and it is updated on the fly in Blender.

Below a short demonstrating me editing parameters of a python script in Vim, and the updating live in Blender.

[Screencast from 07-04-2022 03:28:24 PM.webm](https://user-images.githubusercontent.com/598099/177213774-7a372178-d986-40f3-b508-a27124327318.webm)

# Why?

## Why not OpenSCAD?
OpenSCAD is great for what it does. But because it uses it own domain-specific language, we can't easily use libraries  written in other languages. This workflow allows us to use Python, which means we can leverage a whole world of libraries, and in-turn include our code into other projects.

## Why not use Blender's built in Script editor?
As programmers we spend so much time learning how to be more productive with our own favorite editor, it really suck having to switch to the one integrated in Blender.
