import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def my_iteration(phi0, D, dh, alpha):
    phi = phi0.copy()
    R = D.copy()
    ny, nx = phi0.shape

    for _ in range(1000):
        phi_old = phi.copy()
        for j in range(1, ny-1):
            for i in range(1, nx-1):
                R[j, i] = (phi_old[j+1, i] + phi_old[j, i+1] + phi[j-1, i] + phi[j, i-1] - 4 * phi_old[j, i]) / (dh ** 2) + D[j, i]
                phi[j, i] = phi_old[j, i] + alpha / 4 * (dh ** 2) * R[j, i]
        if np.max(np.abs(phi - phi_old)) < 1e-7:
            break
        
    return phi

def my_partial_derivative(f, axis, dx):
    df = np.zeros_like(f)
    if axis == 0:
        for j in range(1, f.shape[0]-1):
            for i in range(f.shape[1]):
                df[j, i] = (f[j+1, i] - f[j-1, i]) / (2 * dx)
        df[0, :] = (f[1, :] - f[0, :]) / dx
        df[-1, :] = (f[-1, :] - f[-2, :]) / dx
    elif axis == 1:
        for j in range(f.shape[0]):
            for i in range(1, f.shape[1]-1):
                df[j, i] = (f[j, i+1] - f[j, i-1]) / (2 * dx)
        df[:, 0] = (f[:, 1] - f[:, 0]) / dx
        df[:, -1] = (f[:, -1] - f[:, -2]) / dx
    return df

def my_divergence(u, v, dx, dy):
    dudx = my_partial_derivative(u, axis=1, dx=dx)
    dvdy = my_partial_derivative(v, axis=0, dx=dy)
    return dudx + dvdy

Input_u = pd.read_csv("WindField_u.csv", sep='\t', header=None).to_numpy()
Input_v = pd.read_csv("WindField_v.csv", sep='\t', header=None).to_numpy()

x = Input_u[0, 1:].astype(float)
y = Input_u[1:, 0].astype(float)
u = Input_u[1:, 1:].astype(float)
v = Input_v[1:, 1:].astype(float)

dx = dy = dh = 0.25
alpha = 1.6

D = my_divergence(u, v, dx, dy)

phi0 = np.zeros_like(D)
phi = my_iteration(phi0, D, dh, alpha)

du = -my_partial_derivative(phi, axis=1, dx=dx)
dv = -my_partial_derivative(phi, axis=0, dx=dy)

## save to csv
rows = []
for j in range(len(y)):
    for i in range(len(x)):
        rows.append([
            x[i],
            y[j],
            phi[j, i],
            du[j, i],
            dv[j, i]
        ])

df = pd.DataFrame(
    rows,
    columns=["x", "y", "phi", "u_div", "v_div"]
)

df.to_csv("Homework7_res.csv", index=False)

## plot
X, Y = np.meshgrid(x, y)

plt.figure(figsize=(7, 6))

pcm = plt.pcolormesh(
    X, Y, phi,
    shading="gouraud",
    cmap="viridis"
)
cbar = plt.colorbar(pcm, pad=0.02)
cbar.set_label(r"Velocity potential $\phi$")

step = 1
plt.quiver(
    X[::step, ::step],
    Y[::step, ::step],
    du[::step, ::step],
    dv[::step, ::step],
    scale=None,
    angles="xy",
    scale_units="xy",
    width=0.003,
    alpha=0.9
)

plt.xlabel("x")
plt.ylabel("y")
plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.title("Velocity Potential and Divergent Wind Field")
plt.axis("equal")
plt.tight_layout()

plt.savefig("Homework7_plot.png", dpi=300)
plt.show()
