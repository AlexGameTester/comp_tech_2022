import gmsh
import numpy as np

gmsh.initialize()

gmsh.model.add('torus')

lc = 0.2


def create_torus(r1, r2, n=4):
    def create_circle(n, r=1, height=0):
        c = gmsh.model.geo.addPoint(0, 0, height, lc)
        angles = np.linspace(0, 2 * np.pi - 2 * np.pi / n, n)
        points = [gmsh.model.geo.addPoint(r * np.cos(a), r * np.sin(a), height, lc) for a in angles]

        circ_curves = [gmsh.model.geo.addCircleArc(points[i], c, points[(i+1) % len(points)]) for i in range(len(points))]

        return points, circ_curves

    angles = np.linspace(0, 2 * np.pi - 2 * np.pi / n, n)
    points = []
    centers = []
    par_arcs = []
    for a in angles:
        radius = r1 + r2 * np.cos(a)
        height = r2 * np.sin(a)
        ps, c_curves = create_circle(n, radius, height)
        points.append(ps)
        centers.append(gmsh.model.geo.addPoint(r1 * np.cos(a), r1*np.sin(a), 0, lc))
        par_arcs += c_curves

    perp_arcs = []
    for i in range(n):
        for j in range(n):
            perp_arcs.append(gmsh.model.geo.addCircleArc(points[j][i], centers[i], points[(j + 1) % n][i]))

    surfs = []
    for i in range(len(par_arcs)):
    # for i in range(n):
        j = ((i%n) * n + i // n) % len(perp_arcs)
        # print(f'{par_arcs[i]}, {perp_arcs[(j+n) % len(perp_arcs)]}, {-par_arcs[(i+n) % len(par_arcs)]}, {-perp_arcs[j]}')
        loop = gmsh.model.geo.addCurveLoop([par_arcs[i], perp_arcs[(j+n) % len(perp_arcs)], -par_arcs[(i+n) % len(par_arcs)], -perp_arcs[j]])
        surfs.append(gmsh.model.geo.addSurfaceFilling([loop]))

    vol_loop = gmsh.model.geo.addSurfaceLoop(surfs)
    # vol = gmsh.model.geo.addVolume([vol_loop])
    return vol_loop


r1 = 6
r2 = 3
outer_loop = create_torus(r1, r2)
inner_loop = create_torus(r1, r2 - 3 * lc)

vol = gmsh.model.geo.addVolume([outer_loop, -inner_loop])

gmsh.model.geo.synchronize()

gmsh.model.mesh.generate(3)

gmsh.write("torus.msh")

gmsh.fltk.run()

gmsh.finalize()
