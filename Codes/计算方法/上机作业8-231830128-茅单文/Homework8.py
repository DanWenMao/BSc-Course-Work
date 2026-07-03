import numpy as np
import matplotlib.pyplot as plt

def Lorenz_func(x, y, z, b, s, r):
    dxdt = s * (y - x)
    dydt = x * (r - z) - y
    dzdt = x * y - b * z

    return dxdt, dydt, dzdt

# Fourth-order Runge-Kutta method
def my_RK4(func, x0, y0, z0, h):
    k1x, k1y, k1z = func(x0, y0, z0)
    k2x, k2y, k2z = func(x0 + 0.5 * h * k1x, y0 + 0.5 * h * k1y, z0 + 0.5 * h * k1z)
    k3x, k3y, k3z = func(x0 + 0.5 * h * k2x, y0 + 0.5 * h * k2y, z0 + 0.5 * h * k2z)
    k4x, k4y, k4z = func(x0 + h * k3x, y0 + h * k3y, z0 + h * k3z)

    x1 = x0 + (h / 6) * (k1x + 2 * k2x + 2 * k3x + k4x)
    y1 = y0 + (h / 6) * (k1y + 2 * k2y + 2 * k3y + k4y)
    z1 = z0 + (h / 6) * (k1z + 2 * k2z + 2 * k3z + k4z)

    return x1, y1, z1

def Lorenz_RK4(b, s, r, x0, y0, z0, h, n_steps):
    x = np.zeros(n_steps)
    y = np.zeros(n_steps)
    z = np.zeros(n_steps)

    x[0], y[0], z[0] = x0, y0, z0

    for i in range(1, n_steps):
        x[i], y[i], z[i] = my_RK4(lambda x, y, z: Lorenz_func(x, y, z, b, s, r), x[i-1], y[i-1], z[i-1], h)

    return x, y, z

# Fourth-order Adams multistep method
def my_multistep(func, x0, y0, z0, h, n_steps):
    x = np.zeros(n_steps)
    y = np.zeros(n_steps)
    z = np.zeros(n_steps)

    x[0], y[0], z[0] = x0, y0, z0

    for i in range(1, 4):
        x[i], y[i], z[i] = my_RK4(func, x[i-1], y[i-1], z[i-1], h)

    for i in range(4, n_steps):
        f1x, f1y, f1z = func(x[i-1], y[i-1], z[i-1])
        f2x, f2y, f2z = func(x[i-2], y[i-2], z[i-2])
        f3x, f3y, f3z = func(x[i-3], y[i-3], z[i-3])
        f4x, f4y, f4z = func(x[i-4], y[i-4], z[i-4])

        x[i] = x[i-1] + (h / 24) * (55 * f1x - 59 * f2x + 37 * f3x - 9 * f4x)
        y[i] = y[i-1] + (h / 24) * (55 * f1y - 59 * f2y + 37 * f3y - 9 * f4y)
        z[i] = z[i-1] + (h / 24) * (55 * f1z - 59 * f2z + 37 * f3z - 9 * f4z)

    return x, y, z

def Lorenz_multistep(b, s, r, x0, y0, z0, h, n_steps):
    return my_multistep(lambda x, y, z: Lorenz_func(x, y, z, b, s, r), x0, y0, z0, h, n_steps)

## Sensitivity Analysis: Calculation Parameters

x0, y0, z0 = 10.0, 10.0, 10.0
calc_list = [(0.01, 10000), (0.005, 20000), (0.001, 100000)]
para_list = [(8/3, 10.0, 28.0)]

for h, n in calc_list:
    for b, s, r in para_list:

        x_rk, y_rk, z_rk = Lorenz_RK4(b, s, r, x0, y0, z0, h, n)
        plt.figure(figsize=(10, 7))
        plt.plot(x_rk, z_rk, lw=0.5)
        plt.title(f'Calc: h={h} (RK4)')
        plt.xlabel('X')
        plt.ylabel('Z')
        plt.savefig(f'Calc_h{h}_RK4.png', dpi=300)
        plt.close()

        x_ms, y_ms, z_ms = Lorenz_multistep(b, s, r, x0, y0, z0, h, n)
        plt.figure(figsize=(10, 7))
        plt.plot(x_ms, z_ms, lw=0.5)
        plt.title(f'Calc: h={h} (Adams)')
        plt.xlabel('X')
        plt.ylabel('Z')
        plt.savefig(f'Calc_h{h}_Adams.png', dpi=300)
        plt.close()

## Sensitivity analysis: Initial Conditions

delta_list = [1e-6, 1e-8, 1e-10]
h, n = 0.001, 100000
b, s, r = 8/3, 10.0, 28.0

base_ic = np.array([10.0, 10.0, 10.0])

for delta in delta_list:

    ic_list = [
        base_ic,
        base_ic + np.array([delta, 0, 0]),
        base_ic + np.array([0, delta, 0]),
        base_ic + np.array([0, 0, delta]),
    ]

    traj = [Lorenz_RK4(b, s, r, *ic, h, n) for ic in ic_list]
    x0, y0, z0 = traj[0]

    t = np.arange(len(x0)) * h

    plt.figure(figsize=(8,5))
    for i in range(1,4):
        xi, yi, zi = traj[i]
        d = np.sqrt((x0-xi)**2 + (y0-yi)**2 + (z0-zi)**2)
        plt.semilogy(t, d, label=f'Perturb axis {i}')
    plt.xlabel("Time")
    plt.ylabel("Separation")
    plt.title(f'IC sensitivity: δ={delta}')
    plt.legend()
    plt.savefig(f'Init_delta{delta}.png', dpi=300)
    plt.close()

    plt.figure(figsize=(8,6))
    for i, (x,z) in enumerate([(x,z) for x,_,z in traj]):
        plt.plot(x, z, lw=0.5, label=f'IC{i}')
    plt.xlabel("X")
    plt.ylabel("Z")
    plt.title(f'XZ IC: δ={delta}')
    plt.legend()
    plt.savefig(f'XZ_Init_delta{delta}.png', dpi=300)
    plt.close()

## Sensitivity analysis: Parameters

# 基准参数
b0, s0, r0 = 8/3, 10.0, 28.0
h, n = 0.001, 100000
x0, y0, z0 = 10.0, 10.0, 10.0

delta_list = [1e-6, 1e-8]

param_list = ['b', 's', 'r']

for delta in delta_list:
    for pname in param_list:

        if pname == 'b':
            plist = [
                (b0, s0, r0),
                (b0 + delta, s0, r0)
            ]
        elif pname == 's':
            plist = [
                (b0, s0, r0),
                (b0, s0 + delta, r0)
            ]
        elif pname == 'r':
            plist = [
                (b0, s0, r0),
                (b0, s0, r0 + delta)
            ]

        traj = [Lorenz_RK4(b, s, r, x0, y0, z0, h, n) for (b,s,r) in plist]
        x0t, y0t, z0t = traj[0]
        x1t, y1t, z1t = traj[1]

        d = np.sqrt((x0t-x1t)**2 + (y0t-y1t)**2 + (z0t-z1t)**2)
        t = np.arange(len(d)) * h

        plt.figure(figsize=(8,5))
        plt.semilogy(t, d)
        plt.xlabel("Time")
        plt.ylabel("Separation")
        plt.title(f'Param sensitivity: {pname}, δ={delta}')
        plt.savefig(f'ParamSens_{pname}_delta{delta}.png')
        plt.close()

        plt.figure(figsize=(8,6))
        plt.plot(x0t, z0t, lw=0.5, label='Base')
        plt.plot(x1t, z1t, lw=0.5, label=f'{pname}+δ')
        plt.xlabel("X")
        plt.ylabel("Z")
        plt.title(f'XZ Param: {pname}, δ={delta}')
        plt.legend()
        plt.savefig(f'XZ_Param_{pname}_delta{delta}.png')
        plt.close()
