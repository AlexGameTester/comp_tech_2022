from dolfin import *
import dolfin
import matplotlib.pyplot as plt

mesh = UnitSquareMesh(128, 128)
V = FunctionSpace(mesh, 'P', 1)


def boundary(x, on_boundary):
    return on_boundary


b_val = Constant(0)
bc = DirichletBC(V, b_val, boundary)
# Define variational problem
u = TrialFunction(V)
v = TestFunction(V)
# f = Expression("x[0] + 0.2", degree=2)
f = Constant(0)
g = 0
a = inner(grad(u), grad(v))*dx
L = f*v*dx

A, B = assemble_system(a, L, bc)

delta = PointSource(V, Point(0.1, 0.1, 0.), 20)
# delta2 = PointSource(V, Point(0.2, 0.3, 0.), 15)
delta.apply(B)
# delta2.apply(B)


# Compute solution
u = Function(V)
solve(A, u.vector(), B)

plot(u)
plt.savefig("u.png", dpi=600)

file = File("point_charge/test_01.pvd")
file << u
