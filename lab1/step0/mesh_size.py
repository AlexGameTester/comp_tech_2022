import gmsh

gmsh.initialize()

# central_p = gmsh.model.geo.addPoint(0, 0, 0, 3)

lc = 1e-1
p1 = gmsh.model.geo.addPoint(1, 1, 0, lc)
p2 = gmsh.model.geo.addPoint(1, -1, 0, lc)
p3 = gmsh.model.geo.addPoint(-1, -1, 0, lc)
p4 = gmsh.model.geo.addPoint(-1, 1, 0, lc)

c1 = gmsh.model.geo.addLine(p1, p2)
c2 = gmsh.model.geo.addLine(p2, p3)
c3 = gmsh.model.geo.addLine(p3, p4)
c4 = gmsh.model.geo.addLine(p4, p1)

curve_loop = gmsh.model.geo.addCurveLoop([c1, c2, c3, c4])
surf = gmsh.model.geo.addPlaneSurface([curve_loop])

gmsh.model.geo.synchronize()

gmsh.model.mesh.generate(2)

gmsh.write("t1.msh")

gmsh.fltk.run()

gmsh.finalize()
