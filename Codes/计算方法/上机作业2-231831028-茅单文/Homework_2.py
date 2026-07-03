import numpy as np
import matplotlib.pyplot as plt

## Functions
# Func_Lagrange Interpolation
def lagrange_ip(x_points, y_points, x):
    n = len(x_points)
    res = 0.00
    for i in range(n):
        item = y_points[i]
        for j in range(n):
            if j != i:
                item = item * (x - x_points[j]) / (x_points[i] - x_points[j])
        res += item
    return res

# Func_Cubic Spline Interpolantion_periodic boundary condition
def cubic_spline_ip_period(x_points, y_points, x):
    n = len(x_points)
    h = np.diff(x_points) # 0,1,...,n-2
    miu = np.zeros(n-1)
    lam = np.zeros(n-1)
    g = np.zeros(n)
    
    for i in range(n-1): # 0,1,...,n-2
        miu[i] = h[i-1] / (h[i-1] + h[i]) # 0,1,...,n-2
        lam[i] = h[i] / (h[i-1] + h[i]) # 0,1,...,n-2
        g[i+1] = 6 / (h[i-1] + h[i]) * ((y_points[i+1] - y_points[i]) / h[i] - (y_points[i] - y_points[i-1]) / h[i-1]) # 0,1,...,n-2
    g[0] = 6 / (h[0] + h[n-2]) * ((y_points[1] - y_points[0]) / h[0] - (y_points[0] - y_points[n-1]) / h[n-2]) # periodic condition

    A = np.zeros((n,n)) # n*n
    for i in range(n-1): # 0,1,...,n-2
        A[i][i] = 2
        if i > 0: # 1,2,...,n-2
            A[i][i-1] = miu[i-1]
            A[i][i+1] = lam[i-1]
    A[n-1][n-2] = miu[n-2]
    A[n-1][0] = lam[n-2]
    A[0][1] = h[0]/(h[0]+h[n-2]) # periodic condition
    A[0][n-1] = h[n-2]/(h[0]+h[n-2]) # periodic condition

    m = np.linalg.solve(A, g) # 0,1,...,n-2
    m = np.append(m, m[0]) # 0,1,...,n-2,n-1=0

    for i in range(n-1):
        if x < x_points[0]:
            index = 0
            break
        if x_points[i] <= x <= x_points[i+1]:
            index = i
            break
        if x > x_points[n-1]:
            index = n-2
            break

    h_i = x_points[index+1] - x_points[index]
    a = (m[index+1] - m[index]) / (6 * h_i)
    b = m[index] / 2
    c = (y_points[index+1] - y_points[index]) / h_i - (2 * h_i * m[index] + h_i * m[index+1]) / 6
    d = y_points[index]
    return a * (x - x_points[index])**3 + b * (x - x_points[index])**2 + c * (x - x_points[index]) + d

# Func_Cubic Spline Interpolantion_free boundary condition
def cubic_spline_ip_free(x_points, y_points, x):
    n = len(x_points)
    h = np.diff(x_points) # 0,1,...,n-2
    miu = np.zeros(n-1)
    lam = np.zeros(n-1)
    g = np.zeros(n-1)
    
    for i in range(n-1): # 0,1,...,n-2
        miu[i] = h[i-1] / (h[i-1] + h[i]) # 0,1,...,n-2
        lam[i] = h[i] / (h[i-1] + h[i]) # 0,1,...,n-2
        g[i] = 6 / (h[i-1] + h[i]) * ((y_points[i+1] - y_points[i]) / h[i] - (y_points[i] - y_points[i-1]) / h[i-1]) # 0,1,...,n-2

    A = np.zeros((n-1,n-1)) # n*n
    for i in range(n-1): # 0,1,...,n-2
        A[i][i] = 2
        if i < n-2: # 0,1,...,n-3
            A[i][i+1] = lam[i]
        if i > 0: # 1,2,...,n-2
            A[i][i-1] = miu[i]

    m = np.linalg.solve(A, g) # 1,...,n-2
    m = np.insert(m, 0, 0) # 0,1,...,n-2
    m = np.append(m, m[0]) # 0,1,...,n-2,n-1=0

    for i in range(n-1):
        if x < x_points[0]:
            index = 0
            break
        if x_points[i] <= x <= x_points[i+1]:
            index = i
            break
        if x > x_points[n-1]:
            index = n-2
            break

    h_i = x_points[index+1] - x_points[index]
    a = (m[index+1] - m[index]) / (6 * h_i)
    b = m[index] / 2
    c = (y_points[index+1] - y_points[index]) / h_i - (2 * h_i * m[index] + h_i * m[index+1]) / 6
    d = y_points[index]
    return a * (x - x_points[index])**3 + b * (x - x_points[index])**2 + c * (x - x_points[index]) + d

## Application
# Data Points
x_points = np.array([0,2,4,6,8,10,12,14,16,18,20,22,24])
y_points = np.array([17.2,16.4,16.1,16.8,18.9,22.1,25.0,26.3,25.2,22.4,20.1,18.2,17.2])

# Uniform Sampling
x_vals = np.linspace(0, 24, 100)

## 1(1). Plot the interpolating polynomial using all data points
y_lagrange = [lagrange_ip(x_points, y_points, x) for x in x_vals]
y_cubic_spline = [cubic_spline_ip_period(x_points, y_points, x) for x in x_vals]

plt.figure(figsize=(10, 6))

fig1 = plt.subplot(2, 1, 1)
fig1.plot(x_vals, y_lagrange, label='Lagrange IP', color='blue')
fig1.scatter(x_points, y_points, label='Data Points', color='red', s=15, marker='p')
fig1.set_title('Lagrange Interpolation using all data points')
fig1.set_xlabel('time/h')
fig1.set_ylabel('temperatures/°C')
fig1.set_xticks(np.arange(0, 25, 2))

fig2 = plt.subplot(2, 1, 2)
fig2.plot(x_vals, y_cubic_spline, label='Cubic Spline IP', color='green')
fig2.scatter(x_points, y_points, label='Data Points', color='red', s=15, marker='p')
fig2.set_title('Cubic Spline Interpolation using all data points')
fig2.set_xlabel('time/h')
fig2.set_ylabel('temperatures/°C')
fig2.set_xticks(np.arange(0, 25, 2))
plt.tight_layout()
plt.savefig('fig_1_1.png', dpi=300)
plt.show()

## 1(2). Interpolate using partial data points
resser = 'res.csv'
with open(resser, 'w') as f:
    f.write("Results of Interpolation using partial data points and Error\n")
    f.write(f"x_point&y_origin&Lagrange IP res&Lagrange Error&Cubic Spline res&Cubic Spline Error\\\\\n")

n = len(x_points)

y_sublagrange= np.zeros(n-1)
y_subcubic_spline= np.zeros(n-1)
delta_lagrange = np.zeros(n-1)
delta_cubic_spline = np.zeros(n-1)

for i in range(n-1):
    x_subpoints = np.delete(x_points, i)
    y_subpoints = np.delete(y_points, i)

    y_sublagrange[i] = lagrange_ip(x_subpoints, y_subpoints, x_points[i])
    y_subcubic_spline[i] = cubic_spline_ip_period(x_subpoints, y_subpoints, x_points[i])
    delta_lagrange[i] = y_sublagrange[i] - y_points[i]
    delta_cubic_spline[i] = y_subcubic_spline[i] - y_points[i]
    with open(resser, 'a') as f:
        f.write(f"{x_points[i]}&{y_points[i]}&{y_sublagrange[i]:.1f}&{delta_lagrange[i]:.1f}&{y_subcubic_spline[i]:.1f}&{delta_cubic_spline[i]:.1f}\\\\\n")

plt.figure(figsize=(10, 6))
plt.scatter(np.delete(x_points,n-1), np.delete(y_points,n-1), color='red', label='Data Points', s=10, marker='p')
plt.scatter(np.delete(x_points,n-1), y_sublagrange, color='blue', label='Lagrange Interpolation', s=15, marker='x')
plt.scatter(np.delete(x_points,n-1), y_subcubic_spline, color='green', label='Cubic Spline Interpolation', s=15, marker='x')
plt.title(f'Interpolation using parital data points and Error')
plt.xlabel('time/h')
plt.ylabel('temperatures/°C')
plt.xticks(np.arange(0, 25, 2))
plt.legend()
plt.savefig('fig_1_2.png', dpi=300)
plt.show()

# Func_T(t)
def T(t):
    return 18+8*np.sin((np.pi/12)*(t-15))+2*np.sin((np.pi/6)*(t-17))

x_vals = np.linspace(0, 24, 100)

## 2(1). Uniform sampling
x_points_uni = np.linspace(0, 24, 31)
y_points_uni = [T(i) for i in x_points_uni]
y_lagrange_uni = [lagrange_ip(x_points_uni, y_points_uni, x) for x in x_vals]
y_cubic_spline_uni = [cubic_spline_ip_free(x_points_uni, y_points_uni, x) for x in x_vals]

## 2(2). Chebyshev sampling
x_points_cheb = np.zeros(31)
for i in range(31):
    x_points_cheb[i] = 12 + 12 * np.cos((2*i+1)/(2*32) * np.pi)
sort_idx = np.argsort(x_points_cheb)
x_points_cheb = x_points_cheb[sort_idx]
y_points_cheb = [T(i) for i in x_points_cheb]
y_lagrange_cheb = [lagrange_ip(x_points_cheb, y_points_cheb, x) for x in x_vals]
y_cubic_spline_cheb = [cubic_spline_ip_free(x_points_cheb, y_points_cheb, x) for x in x_vals]

# Stability Analysis
y_points_uni_perturb = y_points_uni + np.random.normal(0, 0.1, size=np.array(y_points_uni).shape)
y_lagrange_uni_perturb = [lagrange_ip(x_points_uni, y_points_uni_perturb, x) for x in x_vals]
y_cubic_spline_uni_perturb = [cubic_spline_ip_free(x_points_uni, y_points_uni_perturb, x) for x in x_vals]

y_points_cheb_perturb = y_points_cheb + np.random.normal(0, 0.1, size=np.array(y_points_cheb).shape)
y_lagrange_cheb_perturb = [lagrange_ip(x_points_cheb, y_points_cheb_perturb, x) for x in x_vals]
y_cubic_spline_cheb_perturb = [cubic_spline_ip_free(x_points_cheb, y_points_cheb_perturb, x) for x in x_vals]

# Error Analysis
y_true = [T(x) for x in x_vals]
error_lagrange_uni = np.array(y_lagrange_uni) - np.array(y_true)
error_lagrange_cheb = np.array(y_lagrange_cheb) - np.array(y_true)
error_cubic_spline_uni = np.array(y_cubic_spline_uni) -  np.array(y_true)
error_cubic_spline_cheb = np.array(y_cubic_spline_cheb) -  np.array(y_true)

error_lagrange_uni_perturb = np.array(y_lagrange_uni_perturb) - np.array(y_true)
error_lagrange_cheb_perturb = np.array(y_lagrange_cheb_perturb) - np.array(y_true)
error_cubic_spline_uni_perturb = np.array(y_cubic_spline_uni_perturb) -  np.array(y_true)
error_cubic_spline_cheb_perturb = np.array(y_cubic_spline_cheb_perturb) -  np.array(y_true)

def error_analyse(error_array):
    avg = np.mean(error_array)
    mse = np.mean(error_array ** 2)
    max_abs = np.max(np.abs(error_array))
    return avg, mse, max_abs

metrics = {
    "Lagrange_Uni": error_analyse(error_lagrange_uni),
    "Lagrange_Cheb": error_analyse(error_lagrange_cheb),
    "CubicSpline_Uni": error_analyse(error_cubic_spline_uni),
    "CubicSpline_Cheb": error_analyse(error_cubic_spline_cheb),
    "Lagrange_Uni_Perturb": error_analyse(error_lagrange_uni_perturb),
    "Lagrange_Cheb_Perturb": error_analyse(error_lagrange_cheb_perturb),
    "CubicSpline_Uni_Perturb": error_analyse(error_cubic_spline_uni_perturb),
    "CubicSpline_Cheb_Perturb": error_analyse(error_cubic_spline_cheb_perturb),
}

with open(resser, 'a') as f:
    f.write("\nError Analysis\n")
    f.write("Method & Average Error & MSE & Max Absolute Error\\\\\n")
for name, (avg, mse, max_abs) in metrics.items():
    with open(resser, 'a') as f:
        f.write(f"{name}& {avg:.6f} & {mse:.6f} & {max_abs:.6f}\\\\\n")

# plot
plt.figure(figsize=(10, 9))

fig1 = plt.subplot(3, 1, 2)
fig1.plot(x_vals, y_lagrange_uni, label='Lagrange IP_Uni', color='blue')
fig1.plot(x_vals, y_lagrange_cheb, label='Lagrange IP_Cheb', color='orange')
fig1.plot(x_vals, y_lagrange_uni_perturb, label='Lagrange IP_Uni_Perturb', color='blue', linestyle=':')
fig1.plot(x_vals, y_lagrange_cheb_perturb, label='Lagrange IP_Cheb_Perturb', color='orange', linestyle=':')
fig1.scatter(x_points_uni, y_points_uni, label='Uniform Sampling', color='blue', s=15, marker='p')
fig1.scatter(x_points_cheb, y_points_cheb, label='Chebyshev sampling', color='orange', s=15, marker='p')
fig1.set_title('Lagrange Interpolation')
fig1.set_xlabel('time/h')
fig1.set_ylabel('temperatures/°C')
fig1.set_xticks(np.arange(0, 25, 2))
fig1.legend()

fig3 = plt.subplot(3, 1, 1)
fig3.plot(x_vals, y_lagrange_uni, label='Lagrange IP_Uni', color='blue')
fig3.plot(x_vals, y_lagrange_cheb, label='Lagrange IP_Cheb', color='orange')
fig3.scatter(x_points_uni, y_points_uni, label='Uniform Sampling', color='blue', s=15, marker='p')
fig3.scatter(x_points_cheb, y_points_cheb, label='Chebyshev sampling', color='orange', s=15, marker='p')
fig3.set_title('Lagrange Interpolation')
fig3.set_xlabel('time/h')
fig3.set_ylabel('temperatures/°C')
fig3.set_xticks(np.arange(0, 25, 2))
fig3.legend()

fig2 = plt.subplot(3, 1, 3)
fig2.plot(x_vals, y_cubic_spline_uni, label='Cubic Spline IP_Uni', color='blue')
fig2.plot(x_vals, y_cubic_spline_cheb, label='Cubic Spline IP_Cheb', color='orange')
fig2.plot(x_vals, y_cubic_spline_uni_perturb, label='Cubic Spline IP_Uni_Perturb', color='blue', linestyle=':')
fig2.plot(x_vals, y_cubic_spline_cheb_perturb, label='Cubic Spline IP_Cheb_Perturb', color='orange', linestyle=':')
fig2.scatter(x_points_uni, y_points_uni, label='Uniform Sampling', color='blue', s=15, marker='p')
fig2.scatter(x_points_cheb, y_points_cheb, label='Chebyshev sampling', color='orange', s=15, marker='p')
fig2.set_title('Cubic Spline Interpolation')
fig2.set_xlabel('time/h')
fig2.set_ylabel('temperatures/°C')
fig2.set_xticks(np.arange(0, 25, 2))
fig2.legend()

plt.tight_layout()
plt.savefig('fig_2.png', dpi=300)
plt.show()