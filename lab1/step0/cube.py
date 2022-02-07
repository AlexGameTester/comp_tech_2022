import gmsh
import itertools

gmsh.initialize()

gmsh.model.add('cube')

#
# points = {}
# names = {1: "p", -1: "m"}
# cords = [-1, 1]
# for x in cords:
#     for y in cords:
#         for z in cords:
#             points[names[x] + names[y] + names[z]] =\
#                 gmsh.model.geo.addPoint(x, y, z, lc)
#
# lines = {}
# for (n1, n2) in itertools.combinations(points.keys(), 2):
#     lines[n1 + n2] = gmsh.model.geo.addLine(points[n1], points[n2])
#
#
# circ_names = ['mm', 'mp', 'pp', 'mm']
# surf_point_names = [[c[i:] + 'p' + c[:i] for c in circ_names]for i in range(3)]
# surf_point_names += [[c[i:] + 'm' + c[:i] for c in circ_names]for i in range(3)]
# surfs = []
# loops = []
#
# for surf_names in surf_point_names:
#     line_names = []
#     for i in range(len(surf_names)):
#         line_names.append(surf_names[i] + surf_names[(i + 1) % len(surf_names)])
#
#     loop = gmsh.model.geo.addCurveLoop([lines[ln] for ln in line_names])
#     loops.append(loop)
#     surfs.append(gmsh.model.geo.addPlaneSurface([loop]))
#
# vol = gmsh.model.geo.addVolume(surfs)

lc = 1e-1



gmsh.model.geo.synchronize()

gmsh.fltk.run()

gmsh.finalize()
