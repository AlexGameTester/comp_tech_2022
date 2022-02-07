import gmsh
import numpy as np

gmsh.initialize()

gmsh.model.add('cylinder')

lc = 1e-1

def create_circle(n, height = 0):
    c = gmsh.model.geo.addPoint(0, 0, height, lc)
    angles = np.linspace(0, 2 * np.pi - 2 * np.pi / n, n)
    points = [gmsh.model.geo.addPoint(np.cos(a), np.sin(a), height, lc) for a in angles]

    circ_curves = [gmsh.model.geo.addCircleArc(points[i], c, points[(i+1) % len(points)]) for i in range(len(points))]

    # lines = [gmsh.model.geo.addLine(points[i], points[(i+1) % len(points)]) for i in range(len(points))]

    loop = gmsh.model.geo.addCurveLoop(circ_curves)
    surf = gmsh.model.geo.addPlaneSurface([loop])
    return surf, points, circ_curves

n = 8
top_surf, top_points, top_curves = create_circle(n, 1)
bot_surf, bot_points, bot_curves = create_circle(n, 0)

side_lines = []
for i in range(n):
    side_lines.append(gmsh.model.geo.addLine(bot_points[i], top_points[i]))

surfs = [top_surf, bot_surf]
for i in range(n):
    loop = gmsh.model.geo.addCurveLoop([-top_curves[i], -side_lines[i], bot_curves[i], side_lines[(i + 1) % n]])
    surfs.append(gmsh.model.geo.addSurfaceFilling([loop]))


vol_loop = gmsh.model.geo.addSurfaceLoop(surfs)
gmsh.model.geo.addVolume([vol_loop])


gmsh.model.geo.synchronize()

gmsh.model.mesh.generate(3)
gmsh.fltk.run()

gmsh.finalize()

