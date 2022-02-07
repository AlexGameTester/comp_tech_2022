import gmsh
import numpy as np
import math

gmsh.initialize()

gmsh.model.add("circle")

lc = 1e-1
c = gmsh.model.geo.addPoint(0, 0, 0, lc)

n = 20
angles = np.linspace(0, 2 * np.pi - 2 * np.pi / n, n)
print(np.sin(angles))
print(np.cos(angles))
points = [gmsh.model.geo.addPoint(np.cos(a), np.sin(a), 0, lc) for a in angles]

circ_curves = []
circ_curves += [gmsh.model.geo.addCircleArc(points[i], c, points[(i+1) % len(points)]) for i in range(len(points))]

loop = gmsh.model.geo.addCurveLoop(circ_curves)
surf = gmsh.model.geo.addPlaneSurface([loop])

gmsh.model.geo.synchronize()

gmsh.model.mesh.generate(2)

gmsh.write("circ.msh")

gmsh.fltk.run()

gmsh.finalize()


