import numpy as np

# Jacobi Iteration Method
def my_jacobi(M, max_iter=100):
    M = M.astype(float)

    # Validation check
    if M.shape[0] != M.shape[1]:
        raise ValueError("NOT a square")
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if M[i][j] != M[j][i]:
                raise ValueError("NOT a symmetric matrix")
    
    n = M.shape[0]

    iter = -1
    P = np.eye(n)

    while True:
        iter += 1
        if iter > max_iter:
            raise ValueError("NOT converge within 100 iterations")
        
        L = [0,0,0]
        for i in range(n):
            for j in range(i):
                if abs(M[i][j]) > abs(L[2]):
                    L = [i,j,M[i][j]]
        # Convergence check
        if abs(L[2]) < 1e-4:
            return np.round(np.diag(M),3), np.round(P,4), iter
        
        # Find rotation angle
        theta = 0.5 * np.arctan2(2*L[2], M[L[0]][L[0]] - M[L[1]][L[1]])
        c = np.cos(theta)
        s = np.sin(theta)

        # Update M and P
        M_temp = np.copy(M)

        M_temp[L[0]][L[0]] = M[L[0]][L[0]]*c*c + M[L[1]][L[1]]*s*s + 2 * L[2]*s*c
        M_temp[L[1]][L[1]] = M[L[0]][L[0]]*s*s + M[L[1]][L[1]]*c*c - 2 * L[2]*s*c
        M_temp[L[0]][L[1]] = M_temp[L[1]][L[0]] = 0
        for k in range(n):
            if k != L[0] and k!= L[1]:
                M_temp[L[0]][k] = M[L[0]][k] * c + M[L[1]][k] * s
                M_temp[k][L[0]] = M_temp[L[0]][k]
                M_temp[L[1]][k] = - M[L[0]][k] * s + M[L[1]][k] * c
                M_temp[k][L[1]] = M_temp[L[1]][k]
        M = M_temp

        P_temp = np.eye(n)
        P_temp[L[0]][L[0]] = c
        P_temp[L[1]][L[1]] = c
        P_temp[L[0]][L[1]] = -s
        P_temp[L[1]][L[0]] = s
        P = P.dot(P_temp)

# Power Iteration Method
def my_power_iter(M,V,max_iter=100):
    M = M.astype(float)
    V = V.astype(float)

    # Validation check
    if M.shape[0] != M.shape[1]:
        raise ValueError("NOT a square")
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if M[i][j] != M[j][i]:
                raise ValueError("NOT a symmetric matrix")
    
    n = M.shape[0]
    iter = -1

    while True:
        iter += 1
        if iter > max_iter:
            raise ValueError("NOT converge within 100 iterations")
        
        # Update V
        V = V / np.linalg.norm(V)
        V_temp = M.dot(V)

        value_candi = []
        for i in range(n):
            value_candi.append(V_temp[i] / V[i])
        # Convergence check
        value_diff = np.diff(np.array(value_candi))
        if abs(max(value_diff) - min(value_diff)) < 1e-4:
            return np.round(value_candi[0],3), np.round(V_temp / np.linalg.norm(V_temp),4), iter

        V = V_temp 

A = np.array([[4,2,2,1],[2,5,1,3],[2,1,6,7],[1,3,7,5]])
V1 = np.array([1,1,1,1])
V2 = np.array([1,0,0])
V3 = np.array([0,1,0])
V4 = np.array([0,0,1])
V5 = np.array([0.539,0.515,0.667])
V6 = np.array([0.515,-0.539,0])
V7 = np.array([0.5149,-0.5387,0])
V8 = np.array([-0.3347,0.2562,0,0])

eigenvalues_jc, eigenvectors_jc, iter_jc = my_jacobi(A,100)
eigenvalues_pw, eigenvectors_pw, iter_pw = my_power_iter(A,V8,100)

print("Jacobi Iteraiton Method\n")
print("Eigenvalues:", eigenvalues_jc)
print("Eigenvectors:\n", eigenvectors_jc.T)
print("Iterations:", iter_jc)
print("\nPower Iteration Method\n")
print("Input Vector:", V8)
print("Eigenvalue_max:", eigenvalues_pw)
print("Eigenvector:\n", eigenvectors_pw)
print("Iterations:", iter_pw)
print(np.linalg.eigh(A)) # Compared with numpy.linalg.eigh