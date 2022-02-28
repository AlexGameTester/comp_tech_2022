import dolfin as df
import math

s = 128
mesh = df.UnitSquareMesh(s, s)
V = df.FunctionSpace(mesh, 'P', 1)
c = 2
dt = 0.004
start_t = 0.0
end_t = 0.8

def boundary(x, on_boundary):
    return on_boundary


b_val = df.Constant(0)
bc = df.DirichletBC(V, b_val, boundary)

u0 = df.Constant(0)
u0 = df.interpolate(u0, V)
u_1 = df.Constant(0)
u_1 = df.interpolate(u_1, V)

v = df.TestFunction(V)
u = df.TrialFunction(V)
L = (2* u0 - u_1) * v * df.dx
a = (v * u + (c * dt)**2 * df.inner(df.grad(u), df.grad(v))) * df.dx

A, B = df.assemble_system(a, L, bc)

f = df.Constant(0)
v_inf = df.TestFunction(V)
u_inf = df.TrialFunction(V)
a_inf = df.inner(df.grad(u_inf), df.grad(v_inf))*df.dx
L_inf = f*v*df.dx

A_inf, B_inf = df.assemble_system(a_inf, L_inf, bc)


x0 = 0.5
y0 = 0.5
ampl = 0.008
omega = 24
# x = lambda t: x0 + ampl * math.cos(3 * t)
x = lambda t: x0
y = lambda t: y0 + 2 * ampl * math.sin(omega * t + math.pi / 4)
q = 1

t = start_t
u = df.Function(V)
u_inf = df.Function(V)
u_wave = df.Function(V)

q_f = lambda t: q * math.sin(omega * t + math.pi / 8)

file = df.File('wave/wave.pvd')
while t < end_t:
    B = df.assemble(L)
    print(f't = {t:.3f}')
    deltap = df.PointSource(V, df.Point(x(t), y(t), 0), q)
    deltam = df.PointSource(V, df.Point(x0, y0, 0), -q)
    deltap.apply(B)
    deltam.apply(B)

    # deltaq = df.PointSource(V, df.Point(x0, y0, 0), q_f(t))
    # deltaq.apply(B)
    # deltaq.apply(B_inf)

    df.solve(A, u.vector(), B)
    u0.assign(u)
    u_1.assign(u0)

    # deltam.apply(B_inf)
    # deltap.apply(B_inf)
    # df.solve(A_inf, u_inf.vector(), B_inf)

    # j = 0
    # small = 0.2
    # for i in u.vector():
    #     # i = min(small, i)
    #     # i = max(-small, i)
    #     if i < -small or i > small:
    #         i = 0
    #     u.vector()[j] = i
    #     j += 1

    # u_wave.assign(df.project(u + u_inf, V))
    # df.plot(u_wave, interactive=False)
    # file << u_wave

    df.plot(u, interactive=False)
    file << u

    t += dt
