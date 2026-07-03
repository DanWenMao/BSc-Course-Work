import numpy as np
import matplotlib.pyplot as plt

def func(p):
    return p**2 + 2*p - 100

def dfunc(p):
    return 2*p + 2

def ddfunc(p):
    return 2

def plot_function():
    x = np.linspace(-20, 100, 400)
    y = func(x)
    plt.plot(x, y, label='f(p) = p^2 + 2p - 100')
    plt.axhline(0, color='black', lw=0.5, ls='--')
    plt.xlabel('p')
    plt.ylabel('f(p)')
    plt.title('Function Plot')
    plt.legend()
    plt.grid()
    plt.savefig('fig1_function.png')

def my_bisection(func, a, b, epsilon=1e-3, max_iter=1000):
    if func(a) * func(b) >= 0:
        raise ValueError("Reselect a&b, let f(a)*f(b)<0")
    
    for iter in range(max_iter):
        c = (a + b) / 2
        if abs(func(c)) < epsilon:
            return c, iter+1
        if func(c) * func(a) < 0:
            b = c
        else:
            a = c
    return (a+b)/2, iter+1

def my_newton(func, dfunc, p0, epsilon=1e-3, max_iter=1000):
    #if func(p0) * ddfunc(p0) <= 0:
    #    raise ValueError("Reselect p0, let f(p0)*f''(p0)>0")

    p = p0
    p_history = [p0]

    for iter in range(max_iter):
        p_new = p - func(p) / dfunc(p)
        if abs(func(p_new)) < epsilon:
            return p_new, iter+1, p_history
        p = p_new
        p_history.append(p)

    return p, iter+1, p_history

plot_function()

sol_bisect, iter_bisect = my_bisection(func, 5, 15)

sol_newton__5, iter_newton__5, sol_history__5 = my_newton(func, dfunc, -5)
sol_newton_0, iter_newton_0, sol_history_0 = my_newton(func, dfunc, 0)
sol_newton_5, iter_newton_5, sol_history_5 = my_newton(func, dfunc, 5)
sol_newton_10, iter_newton_10, sol_history_10 = my_newton(func, dfunc, 10)
sol_newton_15, iter_newton_15, sol_history_15 = my_newton(func, dfunc, 15)
sol_newton_100, iter_newton_100, sol_history_100 = my_newton(func, dfunc, 100)

max_iter = max(iter_newton_5, iter_newton_10, iter_newton_15, iter_newton_0, iter_newton_100)
plt.figure()
plt.plot(range(iter_newton__5), np.array(sol_history__5), 'v-.', label='p0 = -5')
plt.plot(range(iter_newton_0), np.array(sol_history_0), '^-.', label='p0 = 0')
plt.plot(range(iter_newton_5), np.array(sol_history_5), 'o-', label='p0 = 5')
plt.plot(range(iter_newton_10), np.array(sol_history_10), 's--', label='p0 = 10')
plt.plot(range(iter_newton_15), np.array(sol_history_15), 'x-.', label='p0 = 15', alpha=0.6)
plt.plot(range(iter_newton_100), np.array(sol_history_100), 'd-.', label='p0 = 100', alpha=0.3)
plt.axhline(sol_bisect, color='black', lw=0.5, ls='--', label='Bisection Solution')
plt.xticks(range(max_iter))
plt.xlabel('Iteration')
plt.ylabel('Approximate Solution p')
plt.title("Newton's Method Convergence")
plt.legend()
plt.grid()
plt.savefig('fig2_newton_convergence.png')

print(f"Bisection Method: Solution = {sol_bisect:.3f}, Iterations = {iter_bisect}")
print(f"Newton's Method: Solution = {sol_newton__5:.3f}, Iterations = {iter_newton__5}, Init = -5")
print(f"Newton's Method: Solution = {sol_newton_0:.3f}, Iterations = {iter_newton_0}, Init = 0")
print(f"Newton's Method: Solution = {sol_newton_5:.3f}, Iterations = {iter_newton_5}, Init = 5")
print(f"Newton's Method: Solution = {sol_newton_10:.3f}, Iterations = {iter_newton_10}, Init = 10")
print(f"Newton's Method: Solution = {sol_newton_15:.3f}, Iterations = {iter_newton_15}, Init = 15")
print(f"Newton's Method: Solution = {sol_newton_100:.3f}, Iterations = {iter_newton_100}, Init = 100")