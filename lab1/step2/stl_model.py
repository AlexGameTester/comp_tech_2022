# STL model is made by mishkin2 https://www.thingiverse.com/mishkin2/designs
# Posted on https://www.thingiverse.com/thing:5203067/files
# And licensed under CC BY-NC 4.0 https://creativecommons.org/licenses/by-nc/4.0/

import gmsh
import math

gmsh.initialize()

gmsh.merge('Honeycomb_organizer.stl')

angle = 15

forceParametrizablePatches = False

includeBoundary = False

curveAngle = 180

gmsh.model.mesh.classifySurfaces(angle * math.pi / 180., includeBoundary,
                                 forceParametrizablePatches,
                                 curveAngle * math.pi / 180.)


gmsh.model.mesh.createGeometry()

s = gmsh.model.getEntities(2)
l = gmsh.model.geo.addSurfaceLoop([tag for (_, tag) in s])
gmsh.model.geo.addVolume([l])

gmsh.model.geo.synchronize()

size_fun = gmsh.model.mesh.field.add('MathEval')
gmsh.model.mesh.field.setString(size_fun, 'F', "10000/(1+(20-x)^2)")
gmsh.model.mesh.field.setAsBackgroundMesh(size_fun)

gmsh.model.mesh.generate(3)
gmsh.write('organizer.msh')

gmsh.fltk.run()

gmsh.finalize()

