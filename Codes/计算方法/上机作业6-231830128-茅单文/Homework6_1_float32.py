import numpy as np
import matplotlib.pyplot as plt

# ---- float32 function ----
def function(x):
    x = np.float32(x)
    if x == np.float32(0.0):
        return np.float32(0.0)
    else:
        return np.sqrt(x) * np.log(x)

# ---- float32 trapezoid ----
def my_trapezoid(f, a, b, h):
    a = np.float32(a)
    b = np.float32(b)
    h = np.float32(h)

    n = int((b - a) / h)
    h2 = np.float32((b - a) / np.float32(n))

    integral = np.float32(0.5) * (f(a) + f(b))

    for i in range(1, n):
        x = a + np.float32(i) * h2
        integral += f(x)

    integral *= h2
    return np.float32(integral), h2

# ---- float32 Simpson ----
def my_Simpson(f, a, b, h):
    a = np.float32(a)
    b = np.float32(b)
    h = np.float32(h)

    n = int((b - a) / h)
    if n % 2 == 1:
        n += 1

    h2 = np.float32((b - a) / np.float32(n))
    integral = f(a) + f(b)

    for i in range(1, n, 2):
        x = a + np.float32(i) * h2
        integral += np.float32(4.0) * f(x)

    for i in range(2, n, 2):
        x = a + np.float32(i) * h2
        integral += np.float32(2.0) * f(x)

    integral *= h2 / np.float32(3.0)
    return np.float32(integral), h2

# ---- ground truth (float32) ----
groundtruth = np.float32(-4.0/9.0)

# ---- step sizes (float32) ----
h = np.array([1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7], dtype=np.float32)

# ---- evaluate ----
T_pairs = [my_trapezoid(function, np.float32(0.0), np.float32(1.0), step) for step in h]
T_res, h_T = zip(*T_pairs)

S_pairs = [my_Simpson(function, np.float32(0.0), np.float32(1.0), step) for step in h]
S_res, h_S = zip(*S_pairs)

T_err = [abs(groundtruth - result) for result in T_res]
S_err = [abs(groundtruth - result) for result in S_res]

# ---- save ----
data = np.column_stack((h_T, h_S, T_res, S_res, T_err, S_err))
np.savetxt("integration_results_float32.csv",
           data,
           delimiter="\t",
           header="h_T\th_S\tT\tS\tT_err\tS_err")

# ---- plot ----
plt.figure(figsize=(10, 6))
plt.loglog(h_T, T_err, label='Trapezoid Error', marker='o')
plt.loglog(h_S, S_err, label='Simpson Error', marker='^')
plt.xlabel('Step size (h)')
plt.ylabel('Absolute Error')
plt.title('Error Analysis (float32)')
plt.legend()
plt.show()
