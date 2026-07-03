import numpy as np

def my_cholesky(M,b):
    n = M.shape[0]
    x = np.zeros_like(b)

    for i in range(1,n):
        M[i,0] = M[i,0]/M[0,0] # l_i1
        for j in range(1,i):
            sum1 = 0
            for k in range(0,j):
                sum1 += M[i,k]*M[j,k]*M[k,k]
            M[i,j] = (M[i,j]-sum1)/M[j,j] # l_ij
        sum2 = 0
        for k in range(0,i):
            sum2 += M[i,k]**2 * M[k,k]
        M[i,i] = M[i,i]-sum2 # d_i
    
    x[0] = b[0] # y_1
    for i in range(1,n):
        sum3 = 0
        for k in range(0,i):
            sum3 += M[i,k]*x[k]
        x[i] = b[i]-sum3
    
    x[n-1] = x[n-1]/M[n-1,n-1] # x_n
    for i in range(n-2,-1,-1):
        sum4 = 0
        for k in range(i+1,n):
            sum4 += M[k,i]*x[k]
        x[i] = x[i]/M[i,i]-sum4

    return x

def my_gauss_seidel(M,b,x0,tol=1e-6,max_iterations=1000):
    n = M.shape[0]
    x = np.zeros_like(x0)

    for iter in range(max_iterations):
        for i in range(n):
            sum1 = 0
            sum2 = 0
            for j in range(0,i):
                sum1 += M[i,j]*x[j]
            for j in range(i+1,n):
                sum2 += M[i,j]*x0[j]
            x[i] = (b[i]-sum1-sum2)/M[i,i]
        
        if np.linalg.norm(x-x0, ord=np.inf) < tol:
            return np.round(x,6), iter+1
        
        x0 = x.copy()
            

A = np.array([[2,-1,0,0,0],
            [-1,2,-1,0,0],
            [0,-1,2,-1,0],
            [0,0,-1,2,-1],
            [0,0,0,-1,2]], dtype=float)
b = np.array([1,1,1,1,1], dtype=float)

x0 = np.array([0,0,0,0,0], dtype=float)

x_chol= my_cholesky(A.copy(), b.copy())
r = np.linalg.norm(b - A.dot(x_chol), ord=np.inf)

x_gs, iters = my_gauss_seidel(A.copy(), b.copy(), x0)

print("Cholesky Solution:", x_chol)
print("Cholesky Residual:", r)
print("Gauss-Seidel Input:", x0)
print("Gauss-Seidel Solution:", x_gs)
print("Gauss-Seidel Iterations:", iters)