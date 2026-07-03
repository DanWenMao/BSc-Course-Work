import numpy as np
import matplotlib.pyplot as plt

# ---- float64 function ----
def function(x):
    if x == 0:
        return 0.0
    else:
        return np.sqrt(x)*np.log(x)

# ---- float64 trapezoid ----
def my_trapezoid(f, a, b, h):
    n = int((b-a)/h)
    h2 = (b-a)/n
    integral = 0.5*(f(a)+f(b))
    
    for i in range(1, n):
        integral += f(a+i*h2)
    
    integral *= h
    return integral, h2

# ---- float64 Simpson ----
def my_Simpson(f, a, b, h):    
    n = int((b-a)/h)
    if n%2==1:
        n += 1
    h2 = (b-a)/n
    integral = f(a)+f(b)

    for i in range(1, n-1, 2):
        integral += 4*f(a+i*h2)
    for i in range(2, n, 2):
        integral += 2*f(a+i*h2)        
    
    integral *= h2/3
    return integral, h2

# ---- ground truth----
groundtruth = -4/9

# ---- step sizes ----
h = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7]

# ---- evaluate ----
T_pairs = [my_trapezoid(function, 0, 1, step) for step in h]
T_res, h_T = zip(*T_pairs)

S_pairs = [my_Simpson(function, 0, 1, step) for step in h]
S_res, h_S = zip(*S_pairs)

T_err = [abs(groundtruth - result) for result in T_res]
S_err = [abs(groundtruth - result) for result in S_res]

# ---- save ----
data = np.column_stack((h_T, h_S, T_res, S_res, T_err, S_err))
np.savetxt("integration_results.csv",
           data,
           delimiter="\t",
           header="h_T\th_S\tT\tS\tT_err\tS_err")

# ---- plot ----
plt.figure(figsize=(10, 6))
plt.loglog(h_T, T_err, label='Trapezoid Error', marker='o')
plt.loglog(h_S, S_err, label='Simpson Error', marker='^')
plt.xlabel('Step size (h)')
plt.ylabel('Absolute Error')
plt.title('Error Analysis (float64)')
plt.legend()
plt.show()
