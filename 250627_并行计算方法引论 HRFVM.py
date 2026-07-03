import glob
import numpy as np
from mpi4py import MPI
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import time

# MPI 初始化
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# 物理常数和参数
# 介质参数
H1, H2 = 50.0, 100.0
rho10, rho20, rho30 = 2700, 2800, 3200
beta1, beta2, beta3 = 1.5e-4, 1.2e-5, 1.2e-4
E1, E3 = 7.0e10, 9.0e10
nu0 = 0.25
lambda_l = 2.5e10
eta0 = 5  # 粘滞系数，被刻意放大，用以模拟长距离效应

# 数值参数
R_max = 25.0
Z_max = 200.0
Nr = 25
Nz = 200
t_max = 0.01
CFL = 1

# 源项参数
P0 = 1e4

# 压力源
def source_func(r, z, t):
    """外部压力源函数"""
    dist2 = r**2 + z**2
    time_scale = 0.005 # 衰减至e^-1的时标
    rz_scale = 1.0 # 衰减至e^-1的空间尺度
    return P0 * np.exp(- dist2 / rz_scale**2) * np.exp(- t**2 / time_scale**2 )

# 网格生成
def generate_grid():
    """生成计算网格, MPI域分解"""
    # 均匀划分
    r_edges = np.linspace(0, R_max, Nr+1)
    z_edges = np.linspace(0, Z_max, Nz+1)
    
    # z方向，分解 (每个进程负责一段连续的z层)
    chunk_size = Nz // size
    remainder = Nz % size

    z_start_idx = rank * chunk_size + min(rank, remainder)
    z_end_idx = z_start_idx + chunk_size + (1 if rank < remainder else 0)
    
    local_z_edges = z_edges[z_start_idx:z_end_idx+1]
    
    r_centers = 0.5 * (r_edges[1:] + r_edges[:-1])
    z_centers = 0.5 * (local_z_edges[1:] + local_z_edges[:-1])
    
    dr = r_edges[1] - r_edges[0]
    dz = local_z_edges[1] - local_z_edges[0]
    
    return {
        'r_edges': r_edges, # 一维数组，Nr+1，全局r方向的网格边界坐标
        'z_edges': local_z_edges,   # 一维数组，local_Nz+1，当前进程在z方向的局部网格边界坐标
        'r_centers': r_centers, # 一维数组，Nr，全局 r 方向的网格中心坐标
        'z_centers': z_centers, # 一维数组，local_Nz，当前进程在 z 方向的局部网格中心坐标
        'dr': dr,   # r方向网格间距
        'dz': dz,   # z方向网格间距
    }

# 材料属性计算
def material_properties(z):
    """输入深度, 返回材料属性"""
    rho = np.zeros_like(z)
    lam = np.zeros_like(z)
    mu = np.zeros_like(z)
    
    # 上层固体
    solid1_mask = (z <= H1)
    rho[solid1_mask] = rho10 * np.exp(beta1 * z[solid1_mask])
    lam[solid1_mask] = (E1 * nu0) / ((1 + nu0) * (1 - 2 * nu0))
    mu[solid1_mask] = E1 / (2 * (1 + nu0))
    
    # 液体层
    liquid_mask = (z > H1) & (z <= H2)
    rho[liquid_mask] = rho20 * np.exp(beta2 * (z[liquid_mask] - H1))
    lam[liquid_mask] = lambda_l
    mu[liquid_mask] = 0.0
    
    # 下层固体
    solid2_mask = (z > H2)
    rho[solid2_mask] = rho30 * np.exp(beta3 * (z[solid2_mask] - H2))
    lam[solid2_mask] = (E3 * nu0) / ((1 + nu0) * (1 - 2 * nu0))
    mu[solid2_mask] = E3 / (2 * (1 + nu0))
    
    # 波速计算
    cp = np.sqrt((lam + 2 * mu) / rho)
    
    return rho, lam, mu, cp

# 初始条件
def initial_conditions(grid):
    """初始化场变量"""
    r_centers = grid['r_centers']
    z_centers = grid['z_centers']
    Nr = len(r_centers)
    Nz = len(z_centers)
    
    # 初始化守恒变量: Q的一个维度对应[ρv_r, ρv_z, σ_rr, σ_θθ, σ_zz, σ_rz]
    Q = np.zeros((6, Nz, Nr))
    
    return Q

# WENO重构
# 此函数存在大量重复的代码，由Deepseek辅助生成
def weno5_reconstruct(u, axis):
    """
    参数:
        u: 输入变量 (3D数组, 形状为(6, Nz, Nr))
        axis: 重构方向 (0: z方向, 1: r极向)
    返回:
        uL, uR: 界面左右状态 (重构轴长度 = 输入长度 + 1)
    """
    epsilon = 1e-40  # 防止除零
    
    n_vars, nz, nr = u.shape
    
    if axis == 0:
        uL_full = np.full((n_vars, nz + 1, nr), np.nan, dtype=u.dtype)
        uR_full = np.full_like(uL_full, np.nan)
    else:
        uL_full = np.full((n_vars, nz, nr + 1), np.nan, dtype=u.dtype)
        uR_full = np.full_like(uL_full, np.nan)
    
    # z方向重构
    if axis == 0:
        # 内部区域
        for i in range(2, nz - 2):
            # 左侧状态重构
            cells = u[:, i-2:i+3, :]
            v0 = (2*cells[:,0] - 7*cells[:,1] + 11*cells[:,2]) / 6.0
            v1 = (-cells[:,1] + 5*cells[:,2] + 2*cells[:,3]) / 6.0
            v2 = (2*cells[:,2] + 5*cells[:,3] - cells[:,4]) / 6.0
            
            s0 = 13/12*(cells[:,0]-2*cells[:,1]+cells[:,2])**2 + 0.25*(cells[:,0]-4*cells[:,1]+3*cells[:,2])**2
            s1 = 13/12*(cells[:,1]-2*cells[:,2]+cells[:,3])**2 + 0.25*(cells[:,1]-cells[:,3])**2
            s2 = 13/12*(cells[:,2]-2*cells[:,3]+cells[:,4])**2 + 0.25*(3*cells[:,2]-4*cells[:,3]+cells[:,4])**2
            
            alpha = [0.1/(epsilon+s0)**2, 0.6/(epsilon+s1)**2, 0.3/(epsilon+s2)**2]
            wsum = alpha[0] + alpha[1] + alpha[2]
            w0 = alpha[0] / wsum
            w1 = alpha[1] / wsum
            w2 = alpha[2] / wsum
            
            uL_full[:, i] = w0*v0 + w1*v1 + w2*v2

            # 右侧状态重构
            if i < nz - 3:
                cells = u[:, i-1:i+4, :]
                v0 = (2*cells[:,0] - 7*cells[:,1] + 11*cells[:,2]) / 6.0
                v1 = (-cells[:,1] + 5*cells[:,2] + 2*cells[:,3]) / 6.0
                v2 = (2*cells[:,2] + 5*cells[:,3] - cells[:,4]) / 6.0
                
                s0 = 13/12*(cells[:,0]-2*cells[:,1]+cells[:,2])**2 + 0.25*(cells[:,0]-4*cells[:,1]+3*cells[:,2])**2
                s1 = 13/12*(cells[:,1]-2*cells[:,2]+cells[:,3])**2 + 0.25*(cells[:,1]-cells[:,3])**2
                s2 = 13/12*(cells[:,2]-2*cells[:,3]+cells[:,4])**2 + 0.25*(3*cells[:,2]-4*cells[:,3]+cells[:,4])**2
                
                alpha = [0.1/(epsilon+s0)**2, 0.6/(epsilon+s1)**2, 0.3/(epsilon+s2)**2]
                wsum = alpha[0] + alpha[1] + alpha[2]
                w0 = alpha[0] / wsum
                w1 = alpha[1] / wsum
                w2 = alpha[2] / wsum
                
                uR_full[:, i] = w0*v0 + w1*v1 + w2*v2

        # 边界处理: 线性重构, 或最近的值
        # 下边界处理
        for i in [0, 1]:
            if i + 1 < nz:
                uR_full[:, i] = (u[:, i] + u[:, i+1]) / 2.0
            else:
                uR_full[:, i] = u[:, min(i, nz-1)]
            
            if i == 0:
                uL_full[:, 0] = u[:, 0]
        
        # 上边界处理
        for i in [nz-1, nz]:
            if i - 1 >= 0:
                uL_full[:, i] = (u[:, i-1] + u[:, min(i, nz-1)]) / 2.0
            else:
                uL_full[:, i] = u[:, min(i, nz-1)]
            
            if i == nz:
                uR_full[:, nz] = uL_full[:, nz]
    
    # r方向重构
    elif axis == 1:
        # 内部区域
        for j in range(2, nr - 2):
            # 左侧状态重构
            cells = u[:, :, j-2:j+3] 
            v0 = (2*cells[:,:,0] - 7*cells[:,:,1] + 11*cells[:,:,2]) / 6.0
            v1 = (-cells[:,:,1] + 5*cells[:,:,2] + 2*cells[:,:,3]) / 6.0
            v2 = (2*cells[:,:,2] + 5*cells[:,:,3] - cells[:,:,4]) / 6.0
            
            s0 = 13/12*(cells[:,:,0]-2*cells[:,:,1]+cells[:,:,2])**2 + 0.25*(cells[:,:,0]-4*cells[:,:,1]+3*cells[:,:,2])**2
            s1 = 13/12*(cells[:,:,1]-2*cells[:,:,2]+cells[:,:,3])**2 + 0.25*(cells[:,:,1]-cells[:,:,3])**2
            s2 = 13/12*(cells[:,:,2]-2*cells[:,:,3]+cells[:,:,4])**2 + 0.25*(3*cells[:,:,2]-4*cells[:,:,3]+cells[:,:,4])**2
            
            alpha = [0.1/(epsilon+s0)**2, 0.6/(epsilon+s1)**2, 0.3/(epsilon+s2)**2]
            wsum = alpha[0] + alpha[1] + alpha[2]
            w0 = alpha[0] / wsum
            w1 = alpha[1] / wsum
            w2 = alpha[2] / wsum
            
            uL_full[:, :, j] = w0*v0 + w1*v1 + w2*v2

            # 右侧状态重构
            if j < nr - 3:
                cells = u[:, :, j-1:j+4]
                v0 = (2*cells[:,:,0] - 7*cells[:,:,1] + 11*cells[:,:,2]) / 6.0
                v1 = (-cells[:,:,1] + 5*cells[:,:,2] + 2*cells[:,:,3]) / 6.0
                v2 = (2*cells[:,:,2] + 5*cells[:,:,3] - cells[:,:,4]) / 6.0
                
                s0 = 13/12*(cells[:,:,0]-2*cells[:,:,1]+cells[:,:,2])**2 + 0.25*(cells[:,:,0]-4*cells[:,:,1]+3*cells[:,:,2])**2
                s1 = 13/12*(cells[:,:,1]-2*cells[:,:,2]+cells[:,:,3])**2 + 0.25*(cells[:,:,1]-cells[:,:,3])**2
                s2 = 13/12*(cells[:,:,2]-2*cells[:,:,3]+cells[:,:,4])**2 + 0.25*(3*cells[:,:,2]-4*cells[:,:,3]+cells[:,:,4])**2
                
                alpha = [0.1/(epsilon+s0)**2, 0.6/(epsilon+s1)**2, 0.3/(epsilon+s2)**2]
                wsum = alpha[0] + alpha[1] + alpha[2]
                w0 = alpha[0] / wsum
                w1 = alpha[1] / wsum
                w2 = alpha[2] / wsum
                
                uR_full[:, :, j] = w0*v0 + w1*v1 + w2*v2
        
        # r轴边界处理 (r=0 和 r=R_max)
        # 下边界 (r=0) - 轴对称轴
        for j in range(0, min(3, nr)):
            if j + 1 < nr:
                uR_full[:, :, j] = (u[:, :, j] + u[:, :, j+1]) / 2.0
            else:
                uR_full[:, :, j] = u[:, :, min(j, nr-1)]
            
            # 对于r=0处的左侧状态，使用对称性
            if j == 0:
                uL_full[:, :, 0] = uR_full[:, :, 0]
        
        # 上边界 (r=R_max)
        for j in range(max(0, nr-3), nr):
            if j - 1 >= 0:
                uL_full[:, :, j] = (u[:, :, j-1] + u[:, :, min(j, nr-1)]) / 2.0
            else:
                uL_full[:, :, j] = u[:, :, min(j, nr-1)]
            
            if j == nr - 1:
                uR_full[:, :, j] = uL_full[:, :, j]
    
    # 填充未重构的界面 (安全机制)
    if axis == 0:
        for i in range(nz + 1):
            if np.any(np.isnan(uL_full[:, i])):
                ref_idx = min(i, nz - 1)
                uL_full[:, i] = u[:, ref_idx]
            if np.any(np.isnan(uR_full[:, i])):
                ref_idx = min(i, nz - 1)
                uR_full[:, i] = u[:, ref_idx]
    else:
        for j in range(nr + 1):
            if np.any(np.isnan(uL_full[:, :, j])):
                ref_idx = min(j, nr - 1)
                uL_full[:, :, j] = u[:, :, ref_idx]
            if np.any(np.isnan(uR_full[:, :, j])):
                ref_idx = min(j, nr - 1)
                uR_full[:, :, j] = u[:, :, ref_idx]
    
    return uL_full, uR_full

# HLLC求解器
def hllc_solver(QL, QR, rho_L, rho_R, lam_L, lam_R, mu_L, mu_R, axis):
    """
    参数:
        QL, QR: 界面左右状态 [ρv_r, ρv_z, σ_rr, σ_θθ, σ_zz, σ_rz]
        rho_L, rho_R: 左右侧密度
        lam_L, lam_R: 左右侧拉梅常数
        mu_L, mu_R: 左右侧剪切模量
        axis: 通量方向 (0: z方向, 1: r方向)
    返回:
        F_star: 界面通量
    """
    # 波速
    cp_L = np.sqrt((lam_L + 2*mu_L) / rho_L)
    cp_R = np.sqrt((lam_R + 2*mu_R) / rho_R)
    cs_L = np.sqrt(mu_L / rho_L)
    if mu_L == 0:
        cs_L = 0
    cs_R = np.sqrt(mu_R / rho_R)
    if mu_R == 0:
        cs_R = 0

    # 提取左右状态变量
    v_rL = QL[0] / rho_L
    v_zL = QL[1] / rho_L
    s_rrL = QL[2]
    s_ttL = QL[3]
    s_zzL = QL[4]
    s_rzL = QL[5]
    
    v_rR = QR[0] / rho_R
    v_zR = QR[1] / rho_R
    s_rrR = QR[2]
    s_ttR = QR[3]
    s_zzR = QR[4]
    s_rzR = QR[5]
    
    # 根据方向选择法向速度
    if axis == 0:  # z方向: 法向速度 = v_z
        v_nL = v_zL
        v_nR = v_zR
        v_tL = v_rL  # 切向速度
        v_tR = v_rR
        # 法向和切向应力分量
        s_nnL = s_zzL
        s_nnR = s_zzR
        s_ttL = s_rrL  # 切向正应力
        s_ttR = s_rrR
        s_ntL = s_rzL  # 切向-法向剪应力
        s_ntR = s_rzR
    else:  # r方向: 法向速度 = v_r
        v_nL = v_rL
        v_nR = v_rR
        v_tL = v_zL  # 切向速度
        v_tR = v_zR
        # 法向和切向应力分量
        s_nnL = s_rrL
        s_nnR = s_rrR
        s_ttL = s_zzL  # 切向正应力
        s_ttR = s_zzR
        s_ntL = s_rzL  # 切向-法向剪应力
        s_ntR = s_rzR
    
    # 波速估计
    SL = np.minimum(np.minimum(v_nL - cp_L, v_nR - cp_R), np.minimum(v_nL - cs_L, v_nR - cs_R))
    SR = np.maximum(np.maximum(v_nL + cp_L, v_nR + cp_R), np.maximum(v_nL + cs_L, v_nR + cs_R))
    
    # 防止除零
    denominator = rho_L * (SL - v_nL) - rho_R * (SR - v_nR)
    denominator = np.where(np.abs(denominator) < 1e-12, np.sign(denominator)+1e-12, denominator)
    
    SM = rho_R * v_nR * (SR - v_nR) - rho_L * v_nL * (SL - v_nL) -s_nnL + s_nnR
    SM /= denominator

    # 数组定义
    F_star = np.zeros_like(QL)
    
    FL = flux(QL, rho_L, lam_L, mu_L, axis)
    FR = flux(QR, rho_R, lam_R, mu_R, axis)
    
    QL_star = np.zeros_like(QL)
    QR_star = np.zeros_like(QR)
    
    # 中间状态
    # 左侧中间状态 (j = L)
    denom_L = SL - SM
    denom_L = np.where(np.abs(denom_L) < 1e-6, np.sign(denom_L)*1e-6, denom_L)
    factor_L = (SL - v_nL) / denom_L
    
    comp0_L = factor_L * rho_L * v_tL
    comp1_L = factor_L * rho_L * SM
    comp2_L = factor_L * (s_nnL + rho_L * (SL - v_nL) * (SM - v_nL))
    comp3_L = factor_L * s_ttL  # σ_θθ分量
    comp4_L = factor_L * (s_ttL + rho_L * v_tL * (SL - v_nL))
    comp5_L = factor_L * s_ntL
    
    # 右侧中间状态 (j = R)
    denom_R = SR - SM
    denom_R = np.where(np.abs(denom_R) < 1e-6, np.sign(denom_R)*1e-6, denom_R)
    factor_R = (SR - v_nR) / denom_R
    
    comp0_R = factor_R * rho_R * v_tR
    comp1_R = factor_R * rho_R * SM
    comp2_R = factor_R * (s_nnR + rho_R * (SR - v_nR) * (SM - v_nR))
    comp3_R = factor_R * s_ttR  # σ_θθ分量
    comp4_R = factor_R * (s_ttR + rho_R * v_tR * (SR - v_nR))
    comp5_R = factor_R * s_ntR
    
    if axis == 0:  # z方向
        QL_star[0] = comp0_L  # ρv_r
        QL_star[1] = comp1_L  # ρv_z
        QL_star[2] = comp4_L  # σ_rr
        QL_star[3] = comp3_L  # σ_θθ
        QL_star[4] = comp2_L  # σ_zz
        QL_star[5] = comp5_L  # σ_rz
        
        QR_star[0] = comp0_R  # ρv_r
        QR_star[1] = comp1_R  # ρv_z
        QR_star[2] = comp4_R  # σ_rr
        QR_star[3] = comp3_R  # σ_θθ
        QR_star[4] = comp2_R  # σ_zz
        QR_star[5] = comp5_R  # σ_rz
    else:  # r方向
        QL_star[0] = comp1_L  # ρv_r
        QL_star[1] = comp0_L  # ρv_z
        QL_star[2] = comp2_L  # σ_rr
        QL_star[3] = comp3_L  # σ_θθ
        QL_star[4] = comp4_L  # σ_zz
        QL_star[5] = comp5_L  # σ_rz
        
        QR_star[0] = comp1_R  # ρv_r
        QR_star[1] = comp0_R  # ρv_z
        QR_star[2] = comp2_R  # σ_rr
        QR_star[3] = comp3_R  # σ_θθ
        QR_star[4] = comp4_R  # σ_zz
        QR_star[5] = comp5_R  # σ_rz
    
    F_star = np.zeros_like(QL)
    
    # 区域判断
    region1 = (0 <= SL)
    region2 = (SL < 0) & (0 <= SM)
    region3 = (SM < 0) & (0 <= SR)
    region4 = (SR < 0)
    
    # 根据区域选择通量
    for i in range(6):
        F_star[i, region1] = FL[i, region1]
        F_star[i, region2] = FL[i, region2] + SL[region2] * (QL_star[i, region2] - QL[i, region2])
        F_star[i, region3] = FR[i, region3] + SR[region3] * (QR_star[i, region3] - QR[i, region3])
        F_star[i, region4] = FR[i, region4]
    
    return F_star

def flux(Q, rho, lam, mu, axis):
    """hllc_solver函数中, 两侧通量的计算"""
    v_r = Q[0] / rho
    v_z = Q[1] / rho
    s_rr = Q[2]
    s_zz = Q[4]
    s_rz = Q[5]
    
    F = np.zeros_like(Q)
    
    if axis == 0:  # z方向通量
        F[0] = -s_rz
        F[1] = -s_zz
        F[2] = -lam * v_z
        F[3] = -lam * v_z
        F[4] = -(lam + 2*mu) * v_z
        F[5] = -mu * v_r
        
    else:  # r方向通量
        F[0] = -s_rr
        F[1] = -s_rz
        F[2] = -(lam + 2*mu) * v_r
        F[3] = -lam * v_r
        F[4] = -lam * v_r
        F[5] = -mu * v_z
        
    return F

# 边界条件
def apply_axisymmetric_boundary(Q):
    """
    应用轴对称边界条件
    Q: 守恒量 [6, nz, nr]
    """
    # 在r=0处 (i=0)
    Q[0, :, 0] = 0.0  # ρv_r = 0
    
    # 设置剪切应力分量为0 (σ_rz = 0)
    Q[5, :, 0] = 0.0  # σ_rz = 0
    
    # 轴向速度和应力使用对称条件
    Q[1, :, 0] = Q[1, :, 1]  # ρv_z对称
    Q[2, :, 0] = Q[2, :, 1]  # σ_rr对称  
    Q[3, :, 0] = Q[2, :, 0]  # σ_θθ = σ_rr (轴对称)
    Q[4, :, 0] = Q[4, :, 1]  # σ_zz对称
    
    return Q

def apply_free_surface_boundary(Q):
    """自由表面边界条件"""
    if rank == 0:
            # 自由表面条件：剪切应力为0
            Q[5, 0, :] = 0.0  # σ_rz = 0
    
    return Q

def apply_radiation_boundary(Q, cp, dt, dr, dz, Q_prev, grid):
    """辐射边界条件"""
    z_edges = grid['z_edges']
    nz, nr = Q.shape[1], Q.shape[2]
    
    # 右边界 (r = r_max)
    for j in range(nz):
        c = cp[j, -1]
        for var in range(6):
            Q[var, j, -1] = Q[var, j, -2] * c*dt / (dr + c*dt) + Q_prev[var, j, -1] * dr / (dr + c*dt)
    
    # 底部边界 (z = z_max)
    if len(z_edges) > 0 and abs(z_edges[-1] - Z_max) < 1e-6:  # z_edges[-1] ≈ Z_max
        
        for i in range(nr):
            c = cp[-1, i]
            for var in range(6):
                Q[var, -1, i] = Q[var, -2, i] * c*dt / (dz + c*dt) + Q_prev[var, -1, i] * dz / (dz + c*dt)
    
    return Q

def apply_material_interface(Q, H1, H2, z_edges, dz, rho, comm):
    """
    材料界面连续条件
    """
    nr = Q.shape[2]
    
    # 确保物理界面等同于数值处理时的界面
    has_H1 = False
    has_H2 = False
    k_H1 = None
    k_H2 = None
    
    # 检查H1是否在当前进程区域内
    if len(z_edges) > 0:
        if min(z_edges) <= H1 <= max(z_edges):
            # 找到最近的网格边界
            dist = np.abs(z_edges - H1)
            k = np.argmin(dist)
            if dist[k] <= dz/2:  # 确保在容差范围内
                has_H1 = True
                k_H1 = k
    
    # 检查H2是否在当前进程区域内
    if len(z_edges) > 0:
        if min(z_edges) <= H2 <= max(z_edges):
            dist = np.abs(z_edges - H2)
            k = np.argmin(dist)
            if dist[k] <= dz/2:
                has_H2 = True
                k_H2 = k
    
    # 处理H1界面
    if has_H1 and 0 < k_H1 < len(z_edges)-1:
        # 界面位于k_H1边界上，两侧网格索引为k_H1-1和k_H1
        for i in range(nr):
            j_left = k_H1 - 1
            j_right = k_H1
            
            rho_left = rho[j_left, i]
            rho_right = rho[j_right, i]
            
            # 速度连续条件
            v_r_interface = (Q[0, j_left, i] + Q[0, j_right, i]) / (rho_left + rho_right)
            v_z_interface = (Q[1, j_left, i] + Q[1, j_right, i]) / (rho_left + rho_right)
            
            Q[0, j_left, i] = rho_left * v_r_interface
            Q[0, j_right, i] = rho_right * v_r_interface
            Q[1, j_left, i] = rho_left * v_z_interface
            Q[1, j_right, i] = rho_right * v_z_interface
            
            # 数值上，取平均值，满足应力连续条件
            sig_zz_interface = 0.5 * (Q[4, j_left, i] + Q[4, j_right, i])
            sig_rz_interface = 0.5 * (Q[5, j_left, i] + Q[5, j_right, i])
            
            Q[4, j_left, i] = sig_zz_interface
            Q[4, j_right, i] = sig_zz_interface
            Q[5, j_left, i] = sig_rz_interface
            Q[5, j_right, i] = sig_rz_interface
    
    # 处理H2界面
    if has_H2 and 0 < k_H2 < len(z_edges)-1:
        for i in range(nr):
            j_left = k_H2 - 1
            j_right = k_H2
            
            rho_left = rho[j_left, i]
            rho_right = rho[j_right, i]
            
            v_r_interface = (Q[0, j_left, i] + Q[0, j_right, i]) / (rho_left + rho_right)
            v_z_interface = (Q[1, j_left, i] + Q[1, j_right, i]) / (rho_left + rho_right)
            
            Q[0, j_left, i] = rho_left * v_r_interface
            Q[0, j_right, i] = rho_right * v_r_interface
            Q[1, j_left, i] = rho_left * v_z_interface
            Q[1, j_right, i] = rho_right * v_z_interface
            
            sig_zz_interface = 0.5 * (Q[4, j_left, i] + Q[4, j_right, i])
            sig_rz_interface = 0.5 * (Q[5, j_left, i] + Q[5, j_right, i])
            
            Q[4, j_left, i] = sig_zz_interface
            Q[4, j_right, i] = sig_zz_interface
            Q[5, j_left, i] = sig_rz_interface
            Q[5, j_right, i] = sig_rz_interface
    
    comm.Barrier()
    
    return Q

# 通量计算函数
def compute_H_flux(Q, rho, lam, mu):
    """计算r方向的通量"""
    num_vars, nz, nr = Q.shape
    
    # 界面重构
    QL_r, QR_r = weno5_reconstruct(Q, 1)  # r方向
    
    F_r = np.zeros((num_vars, nz, nr-1))
    for j in range(nz):
        for i in range(nr-1):
            rho_L = rho[j, i]
            rho_R = rho[j, i+1]
            lam_L = lam[j, i]
            lam_R = lam[j, i+1]
            mu_L = mu[j, i]
            mu_R = mu[j, i+1]
            
            # 计算通量
            F_r[:, j, i] = hllc_solver(
                QL_r[:, j, i], QR_r[:, j, i], 
                rho_L, rho_R, lam_L, lam_R, mu_L, mu_R, 
                axis=1
            )
    
    return F_r

def compute_G_flux(Q, rho, lam, mu):
    """计算z方向的通量"""
    num_vars, nz, nr = Q.shape
    
    # 界面重构
    QL_z, QR_z = weno5_reconstruct(Q, 0)  # z方向
    
    # 计算通量
    F_z = np.zeros((num_vars, nz-1, nr))
    for i in range(nr):
        for j in range(nz-1):
            rho_L = rho[j, i]
            rho_R = rho[j+1, i]
            lam_L = lam[j, i]
            lam_R = lam[j+1, i]
            mu_L = mu[j, i]
            mu_R = mu[j+1, i]
            
            # 计算通量
            F_z[:, j, i] = hllc_solver(
                QL_z[:, j, i], QR_z[:, j, i], 
                rho_L, rho_R, lam_L, lam_R, mu_L, mu_R, 
                axis=0
            )
    
    return F_z

# 源项计算
# 此段函数代码参考了Deepseek的建议
def compute_source(Q, rho, lam, r_centers, t, eta0, rank, size):
    """轴对称1/r项的源项计算"""
    num_vars, nz, nr = Q.shape
    S = np.zeros_like(Q)
    
    # 粘滞阻尼项
    S[0] = -eta0 * rho * (Q[0] / rho)
    S[1] = -eta0 * rho * (Q[1] / rho)
    
    # 计算全局z坐标
    chunk_size = Nz // size
    remainder = Nz % size
    z_start_idx = rank * chunk_size + min(rank, remainder)
    
    # 几何源项，轴对称处理
    dr = r_centers[1] - r_centers[0] if nr > 1 else 1.0
    
    for j in range(nz):
        global_z_idx = z_start_idx + j
        global_z = global_z_idx * (Z_max / Nz)
        
        for i in range(nr):
            r = r_centers[i]
            
            if i == 0:  # 轴心处特殊处理
                # 使用L'Hôpital规则和轴对称性质
                
                # 1. 动量方程中的 (σ_rr - σ_θθ)/r 项
                # 在轴对称情况下，σ_rr = σ_θθ 在r=0处，所以这一项为0
                # 但数值上可能不完全相等，使用导数形式
                if nr > 2:
                    # lim(r→0) (σ_rr - σ_θθ)/r = d(σ_rr - σ_θθ)/dr|_{r=0}
                    # 使用前向差分近似
                    dstress_diff_dr = ((Q[2, j, 1] - Q[3, j, 1]) - (Q[2, j, 0] - Q[3, j, 0])) / dr
                    S[0, j, 0] += dstress_diff_dr
                else:
                    S[0, j, 0] += 0.0
                
                # 2. 动量方程中的 σ_rz/r 项
                # 由于轴对称边界条件 σ_rz(r=0) = 0，且σ_rz在r=0附近应该是线性的
                # lim(r→0) σ_rz/r = dσ_rz/dr|_{r=0}
                if nr > 2:
                    dsrz_dr = (Q[5, j, 1] - Q[5, j, 0]) / dr
                    S[1, j, 0] += dsrz_dr
                else:
                    S[1, j, 0] += 0.0
                
                # 3. 应力方程中的 λv_r/r 项
                # lim(r→0) v_r/r = dv_r/dr|_{r=0}
                if nr > 2:
                    dvr_dr = ((Q[0, j, 1]/rho[j, 1]) - (Q[0, j, 0]/rho[j, 0])) / dr
                    S[2, j, 0] += -lam[j, i] * dvr_dr
                    S[3, j, 0] += -lam[j, i] * dvr_dr
                    S[4, j, 0] += -lam[j, i] * dvr_dr
                else:
                    S[2, j, 0] += 0.0
                    S[3, j, 0] += 0.0
                    S[4, j, 0] += 0.0
                
                S[5, j, 0] += 0.0  # σ_rz方程无1/r项
                
            elif i == 1 and r_centers[0] < 1e-6:  # 第二个点，如果第一个点很接近轴心
                # 对于非常接近轴心的点，使用插值方法避免数值不稳定
                r_small = r_centers[i]
                
                # 使用泰勒展开：f(r)/r ≈ f'(0) + f''(0)*r/2 + ...
                # 简化为线性插值
                if nr > 2:
                    # 动量方程
                    stress_diff_0 = Q[2, j, 0] - Q[3, j, 0]  # 轴心处应该为0
                    stress_diff_1 = Q[2, j, 1] - Q[3, j, 1]
                    stress_diff_2 = Q[2, j, 2] - Q[3, j, 2]
                    
                    # 使用二阶差分估计导数
                    d2stress_dr2 = (stress_diff_2 - 2*stress_diff_1 + stress_diff_0) / (dr*dr)
                    S[0, j, i] += stress_diff_1/r_small * 0.5 + d2stress_dr2 * r_small * 0.5
                    
                    # 类似处理其他项...
                    S[1, j, i] += Q[5, j, i]/r_small * 0.5
                    
                    vr_term = (Q[0, j, i] / rho[j, i]) / r_small * 0.5
                    S[2, j, i] += -lam[j, i] * vr_term
                    S[3, j, i] += -lam[j, i] * vr_term
                    S[4, j, i] += -lam[j, i] * vr_term
                else:
                    # 如果点数不够，使用标准处理但加上限制
                    if r_small > 1e-12:
                        S[0, j, i] += (Q[2, j, i] - Q[3, j, i]) / r_small
                        S[1, j, i] += Q[5, j, i] / r_small
                        S[2, j, i] += -lam[j, i] * (Q[0, j, i] / rho[j, i]) / r_small
                        S[3, j, i] += -lam[j, i] * (Q[0, j, i] / rho[j, i]) / r_small
                        S[4, j, i] += -lam[j, i] * (Q[0, j, i] / rho[j, i]) / r_small
                
            else:  # 远离轴心的正常点
                if r > 1e-12:
                    S[0, j, i] += (Q[2, j, i] - Q[3, j, i]) / r
                    S[1, j, i] += Q[5, j, i] / r
                    S[2, j, i] += -lam[j, i] * (Q[0, j, i] / rho[j, i]) / r
                    S[3, j, i] += -lam[j, i] * (Q[0, j, i] / rho[j, i]) / r
                    S[4, j, i] += -lam[j, i] * (Q[0, j, i] / rho[j, i]) / r
                    S[5, j, i] += 0.0
            
            # 外部压力源
            S[1, j, i] += source_func(r, global_z, t)
    
    return S

# MPI通信
def exchange_ghost_cells(Q, comm):
    """Ghost cell交换"""
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    nghost = 3
    num_vars, nz, nr = Q.shape
    
    # 检查数组大小
    if nz <= 2 * nghost:
        print(f"[WARNING] Process {rank}: nz={nz} too small for ghost exchange")
        return Q
    
    reqs = []
    
    # 发送和接收缓冲区
    if rank > 0:
        # 向上游进程发送我的前nghost层，接收用于更新我的前nghost层的数据
        send_to_prev = Q[:, :nghost, :].copy()
        recv_from_prev = np.zeros((num_vars, nghost, nr), dtype=np.float64)
        
        reqs.append(comm.Isend(send_to_prev, dest=rank-1, tag=100))
        reqs.append(comm.Irecv(recv_from_prev, source=rank-1, tag=200))
    
    if rank < size-1:
        # 向下游进程发送我的后nghost层，接收用于更新我的后nghost层的数据
        send_to_next = Q[:, -nghost:, :].copy()
        recv_from_next = np.zeros((num_vars, nghost, nr), dtype=np.float64)
        
        reqs.append(comm.Isend(send_to_next, dest=rank+1, tag=200))
        reqs.append(comm.Irecv(recv_from_next, source=rank+1, tag=100))
    
    MPI.Request.Waitall(reqs)
    
    # 更新ghost cells
    if rank > 0:
        Q[:, :nghost, :] = recv_from_prev
    
    if rank < size-1:
        Q[:, -nghost:, :] = recv_from_next
    
    return Q

# SSP-RK3时间积分
def ssp_rk3(Q, dt, t, grid, rho, lam, mu, cp, eta0, comm, Q_prev):
    """
    SSP-RK(3,3) 时间积分方法
    """
    
    # 第一阶段
    L0 = compute_rhs(Q_prev, Q_prev, dt, t, grid, rho, lam, mu, cp, eta0, comm)
    Q1 = Q + dt * L0

    # 第二阶段
    L1 = compute_rhs(Q1, Q_prev, dt, t + dt, grid, rho, lam, mu, cp, eta0, comm)
    Q2 = (3/4)*Q + (1/4)*Q1 + (1/4)*dt*L1

    # 第三阶段
    L2 = compute_rhs(Q2, Q_prev, dt, t + 0.5*dt, grid, rho, lam, mu, cp, eta0, comm)
    Q_new = (1/3)*Q + (2/3)*Q2 + (2/3)*dt*L2

    return Q_new

def compute_rhs(Q, Q_prev, dt, t, grid, rho, lam, mu, cp, eta0, comm):
    """计算SSP-RK中间解L0、L1、L2"""
    r_centers = grid['r_centers']
    z_centers = grid['z_centers']
    dr, dz = grid['dr'], grid['dz']
    num_variables, nz, nr = Q.shape
    
    # 交换Ghost cells
    Q = exchange_ghost_cells(Q, comm)
    
    # 边界条件
    Q = apply_axisymmetric_boundary(Q)
    Q = apply_free_surface_boundary(Q)
    Q = apply_radiation_boundary(Q, cp, dt, grid['dr'], grid['dz'], Q_prev, grid)
    Q = apply_material_interface(Q, H1, H2, grid['z_edges'], dz, rho, comm)
    
    # 通量
    F_r = compute_H_flux(Q, rho, lam, mu)
    F_z = compute_G_flux(Q, rho, lam, mu)
    
    # 源项
    S = compute_source(Q, rho, lam, z_centers, t, eta0, rank, size)
    
    # 中间项
    dQdt = np.zeros_like(Q)
    
    # 内部点
    for var in range(num_variables):
        for j in range(1, nz-1):
            for i in range(1, nr-1):
                dFrdr = (F_r[var, j, i] - F_r[var, j, i-1]) / (r_centers[i]*dr)
                dFzdz = (F_z[var, j, i] - F_z[var, j-1, i]) / dz
                
                dQdt[var, j, i] = -dFrdr - dFzdz + S[var, j, i]
    # 边界点
    for var in range(num_variables):
        for i in range(1, nr-1):
            
            # 底部边界 (j=0)
            if nz > 1:
                # r方向通量散度
                dFrdr = (F_r[var, 0, i] - F_r[var, 0, i-1]) / (r_centers[i] * dr)
                # z方向通量散度：只有上边界通量
                dFzdz = F_z[var, 0, i] / dz  # 下边界通量为0（边界条件）
                dQdt[var, 0, i] = -dFrdr - dFzdz + S[var, 0, i]
            
            # 顶部边界 (j=nz-1)
            if nz > 1:
                # r方向通量散度
                dFrdr = (F_r[var, nz-1, i] - F_r[var, nz-1, i-1]) / (r_centers[i] * dr)
                # z方向通量散度：只有下边界通量
                if nz > 1:
                    dFzdz = -F_z[var, nz-2, i] / dz  # 上边界通量为0（边界条件）
                else:
                    dFzdz = 0
                dQdt[var, nz-1, i] = -dFrdr - dFzdz + S[var, nz-1, i]
    
    for var in range(num_variables):
        for j in range(1, nz-1):  # z方向仍然是内部点
            # 轴心边界 (i=0, r=0)
            # 轴对称边界：r=0处的通量散度需要特殊处理
            if nr > 1:
                # 在r=0处，使用L'Hopital规则：lim(r→0) (1/r)(∂F_r/∂r) = ∂²F_r/∂r²|_{r=0}
                # 简化处理：使用右侧差分
                dFrdr = 2 * F_r[var, j, 0] / dr  # 轴对称特殊处理
                # z方向通量散度
                dFzdz = (F_z[var, j, 0] - F_z[var, j-1, 0]) / dz
                dQdt[var, j, 0] = -dFrdr - dFzdz + S[var, j, 0]
            
            # 外边界 (i=nr-1)
            if nr > 1:
                # r方向通量散度：只有左边界通量
                dFrdr = -F_r[var, j, nr-2] / (r_centers[nr-1] * dr)  # 右边界通量为0（辐射边界）
                # z方向通量散度
                dFzdz = (F_z[var, j, nr-1] - F_z[var, j-1, nr-1]) / dz
                dQdt[var, j, nr-1] = -dFrdr - dFzdz + S[var, j, nr-1]
    
    for var in range(num_variables): 
        # 左下角 (i=0, j=0)
        if nr > 1 and nz > 1:
            dFrdr = 2 * F_r[var, 0, 0] / dr  # 轴对称处理
            dFzdz = F_z[var, 0, 0] / dz
            dQdt[var, 0, 0] = -dFrdr - dFzdz + S[var, 0, 0]
        
        # 右下角 (i=nr-1, j=0)
        if nr > 1 and nz > 1:
            dFrdr = -F_r[var, 0, nr-2] / (r_centers[nr-1] * dr)
            dFzdz = F_z[var, 0, nr-1] / dz
            dQdt[var, 0, nr-1] = -dFrdr - dFzdz + S[var, 0, nr-1]
        
        # 左上角 (i=0, j=nz-1)
        if nr > 1 and nz > 1:
            dFrdr = 2 * F_r[var, nz-1, 0] / dr
            dFzdz = -F_z[var, nz-2, 0] / dz
            dQdt[var, nz-1, 0] = -dFrdr - dFzdz + S[var, nz-1, 0]
        
        # 右上角 (i=nr-1, j=nz-1)
        if nr > 1 and nz > 1:
            dFrdr = -F_r[var, nz-1, nr-2] / (r_centers[nr-1] * dr)
            dFzdz = -F_z[var, nz-2, nr-1] / dz
            dQdt[var, nz-1, nr-1] = -dFrdr - dFzdz + S[var, nz-1, nr-1]
    
    return dQdt

def monitor_solution_stability(Q, step, stage=""):
    max_momentum = np.max(np.abs(Q[:2]))  # 前两个分量是动量
    max_stress = np.max(np.abs(Q[2:]))    # 后四个分量是应力
    
    # 估算最大速度（假设最小密度为2000）
    estimated_max_velocity = max_momentum / 2000.0
    
    # 输出条件
    should_output = (
        step % 5 == 0 or  # 每5步输出一次
        estimated_max_velocity > 1e6 or  # 速度过大
        np.any(np.isnan(Q)) or np.any(np.isinf(Q))  # 出现NaN/Inf
    )
    
    if should_output:
        print(f"[STABILITY] Step {step}{stage}: Max momentum={max_momentum:.2e}, Max stress={max_stress:.2e}")
        print(f"  Estimated max velocity: {estimated_max_velocity:.2e}")
        if np.any(np.isnan(Q)):
            print(f"  WARNING: NaN detected!")
        if np.any(np.isinf(Q)):
            print(f"  WARNING: Inf detected!")

def main_solver():
    """主求解函数"""
    grid = generate_grid()
    z_centers = grid['z_centers']
    dr, dz = grid['dr'], grid['dz']
    local_Nr = len(grid['r_centers'])
    
    rho, lam, mu, cp = material_properties(z_centers)
    rho_grid = np.outer(rho, np.ones(local_Nr))
    lam_grid = np.outer(lam, np.ones(local_Nr))
    mu_grid = np.outer(mu, np.ones(local_Nr))
    cp_grid = np.outer(cp, np.ones(local_Nr))
    
    Q = initial_conditions(grid)
    Q_prev = Q.copy()
    
    cfl_dt = 0.5 * min(dr, dz) / np.max(cp)
    dt = cfl_dt * CFL
    num_steps = int(t_max / dt)
    
    save_interval = 10
    
    if rank == 0:
        r_centers_global = np.linspace(0, R_max, Nr)
        z_centers_global = np.linspace(0, Z_max, Nz)
    
    start_time = time()
    for step in range(num_steps):
        t = step * dt
        
        monitor_solution_stability(Q, step, " (before)")
        
        Q_new = ssp_rk3(Q, dt, t, grid, rho_grid, lam_grid, mu_grid, cp_grid, eta0, comm, Q_prev)

        monitor_solution_stability(Q_new, step, " (after)")

        Q_prev = Q.copy()
        Q = Q_new
        
        if step % save_interval == 0:
            all_Q = comm.gather(Q, root=0)
            
            if rank == 0:
                full_Q = np.concatenate(all_Q, axis=1)
                filename = f'wave_propagation_result_step_{step:05d}.npz'
                np.savez(filename, Q=full_Q, r_centers=r_centers_global, z_centers=z_centers_global, time=t)
                
                print(f"Saved results for step {step}, time={t:.4f}s to {filename}")
            
            # 阻塞同步
            comm.Barrier()
        
        if rank == 0 and step % 10 == 0:
            elapsed = time() - start_time
            print(f"Step {step}/{num_steps}, Time={t:.4f}s, dt={dt:.6f}s, Elapsed={elapsed:.2f}s")
    
    if rank == 0:
        print("Simulation completed. Final results saved.")
    
    return Q

def visualize_results():
    """可视化所有保存的时间步结果，生成动画"""
    if rank != 0:
        return
    
    # 查找所有结果文件
    result_files = sorted(glob.glob('wave_propagation_result_step_*.npz'))
    if not result_files:
        print("No result files found for visualization.")
        return
    
    # 准备动画数据
    all_data = []
    for file in result_files:
        data = np.load(file)
        all_data.append({
            'Q': data['Q'],
            'r_centers': data['r_centers'],
            'z_centers': data['z_centers'],
            'time': data['time']
        })
    
    fig = plt.figure(figsize=(16, 12))
    
    ax1 = plt.subplot(2, 3, 1)  # 垂向速度场
    ax2 = plt.subplot(2, 3, 2)  # 垂向应力场
    ax3 = plt.subplot(2, 3, 3)  # 能量密度场
    ax4 = plt.subplot(2, 3, 4)  # 近场监测
    ax5 = plt.subplot(2, 3, 5)  # 远场监测
    ax6 = plt.subplot(2, 3, 6)  # 深度监测
    
    plt.tight_layout(pad=3.0)
    
    # 初始化数据
    r_centers = all_data[0]['r_centers']
    z_centers = all_data[0]['z_centers']
    rho, lam, mu, cp = material_properties(z_centers)
    rho_grid = np.outer(rho, np.ones(len(r_centers)))
    lam_grid = np.outer(lam, np.ones(len(r_centers)))
    mu_grid = np.outer(mu, np.ones(len(r_centers)))
    
    # 计算初始物理量
    Q_init = all_data[0]['Q']
    v_r = Q_init[0] / (rho_grid + 1e-10)
    v_z = Q_init[1] / (rho_grid + 1e-10)
    
    def safe_energy_calculation(Q, rho_grid, lam_grid, mu_grid):
        # 限制速度的最大值
        v_r = np.clip(Q[0] / (rho_grid + 1e-10), -1e3, 1e3)
        v_z = np.clip(Q[1] / (rho_grid + 1e-10), -1e3, 1e3)
        
        # 计算动能密度
        kinetic_energy = 0.5 * rho_grid * (v_r**2 + v_z**2)
        
        # 限制应力分量的最大值
        stress_components = [np.clip(Q[i], -1e9, 1e9) for i in range(2, 6)]
        
        # 计算应变能密度
        strain_energy = 0.5 * (stress_components[0]**2 + stress_components[1]**2 + 
                              stress_components[2]**2 + 2*stress_components[3]**2) / (lam_grid + 2*mu_grid + 1e-10)
        
        total_energy = kinetic_energy + strain_energy
        
        # 检查并处理异常值
        total_energy = np.where(np.isfinite(total_energy), total_energy, 0)
        total_energy = np.clip(total_energy, 0, 1e12)  # 限制最大能量值
        
        return kinetic_energy, strain_energy, total_energy, v_r, v_z
    
    # 计算初始能量
    kinetic_energy, strain_energy, total_energy, v_r, v_z = safe_energy_calculation(
        Q_init, rho_grid, lam_grid, mu_grid)
    
    # 初始化图像
    im1 = ax1.imshow(v_z, extent=[0, R_max, Z_max, 0], cmap='seismic', aspect='auto', 
                     vmin=-0.1, vmax=0.1)
    cbar1 = fig.colorbar(im1, ax=ax1, shrink=0.8)
    cbar1.set_label('Vertical Velocity (m/s)')
    ax1.set_title('Vertical Velocity Field')
    ax1.set_xlabel('Radial Distance (m)')
    ax1.set_ylabel('Depth (m)')
    
    im2 = ax2.imshow(Q_init[4]/1e6, extent=[0, R_max, Z_max, 0], cmap='viridis', aspect='auto')
    cbar2 = fig.colorbar(im2, ax=ax2, shrink=0.8)
    cbar2.set_label('Stress σ_zz (MPa)')
    ax2.set_title('Vertical Stress Field')
    ax2.set_xlabel('Radial Distance (m)')
    ax2.set_ylabel('Depth (m)')
    
    im3 = ax3.imshow(np.log10(total_energy + 1e-10), extent=[0, R_max, Z_max, 0], 
                     cmap='plasma', aspect='auto')
    cbar3 = fig.colorbar(im3, ax=ax3, shrink=0.8)
    cbar3.set_label('log₁₀(Energy Density) (J/m³)')
    ax3.set_title('Total Energy Density')
    ax3.set_xlabel('Radial Distance (m)')
    ax3.set_ylabel('Depth (m)')
    
    # 标记材料界面
    for ax in (ax1, ax2, ax3):
        ax.axhline(y=H1, color='white', linestyle='--', alpha=0.7, linewidth=1)
        ax.axhline(y=H2, color='white', linestyle='--', alpha=0.7, linewidth=1)
    
    # 定义监测点
    near_field_r = max(1, int(len(r_centers) * 0.1))  # 确保索引有效
    far_field_r = min(len(r_centers)-1, int(len(r_centers) * 0.7))
    shallow_z = max(1, int(len(z_centers) * 0.2))
    deep_z = min(len(z_centers)-1, int(len(z_centers) * 0.8))
    
    # 初始化监测数据存储
    times = []
    near_field_data = {'v_z': [], 'stress': [], 'energy': []}
    far_field_data = {'v_z': [], 'stress': [], 'energy': []}
    shallow_data = {'v_z': [], 'stress': [], 'energy': []}
    deep_data = {'v_z': [], 'stress': [], 'energy': []}
    
    # 初始化监测图
    line_nf_vz, = ax4.plot([], [], 'b-', label='v_z (near)', linewidth=2)
    line_nf_stress, = ax4.plot([], [], 'r-', label='σ_zz/10⁶ (near)', linewidth=2)
    line_ff_vz, = ax4.plot([], [], 'b--', label='v_z (far)', linewidth=2)
    line_ff_stress, = ax4.plot([], [], 'r--', label='σ_zz/10⁶ (far)', linewidth=2)
    ax4.set_title('Near-field vs Far-field Monitoring')
    ax4.set_xlabel('Time (s)')
    ax4.set_ylabel('Amplitude')
    ax4.legend(fontsize=8)
    ax4.grid(True, alpha=0.3)
    
    line_sh_energy, = ax5.plot([], [], 'g-', label='Energy (shallow)', linewidth=2)
    line_dp_energy, = ax5.plot([], [], 'g--', label='Energy (deep)', linewidth=2)
    line_sh_vz, = ax5.plot([], [], 'm-', label='v_z (shallow)', linewidth=2)
    line_dp_vz, = ax5.plot([], [], 'm--', label='v_z (deep)', linewidth=2)
    ax5.set_title('Shallow vs Deep Monitoring')
    ax5.set_xlabel('Time (s)')
    ax5.set_ylabel('Amplitude')
    ax5.legend(fontsize=8)
    ax5.grid(True, alpha=0.3)
    
    # 深度剖面监测
    line_depth_vz, = ax6.plot([], [], 'b-', label='v_z profile', linewidth=2)
    line_depth_energy, = ax6.plot([], [], 'orange', label='Energy×10⁻⁶', linewidth=2)
    ax6.set_title('Center Depth Profile')
    ax6.set_xlabel('Depth (m)')
    ax6.set_ylabel('Amplitude')
    ax6.legend(fontsize=8)
    ax6.grid(True, alpha=0.3)
    ax6.axvline(x=H1, color='gray', linestyle=':', alpha=0.5)
    ax6.axvline(x=H2, color='gray', linestyle=':', alpha=0.5)
    
    # 时间文本
    time_text = fig.text(0.5, 0.02, '', ha='center', fontsize=14, weight='bold')
    
    # 更新函数
    def update(frame):
        data = all_data[frame]
        current_time = data['time']
        
        rho, lam, mu, cp = material_properties(data['z_centers'])
        rho_grid = np.outer(rho, np.ones(len(data['r_centers'])))
        lam_grid = np.outer(lam, np.ones(len(data['r_centers'])))
        mu_grid = np.outer(mu, np.ones(len(data['r_centers'])))
        
        Q = data['Q']
        
        # 能量和速度
        kinetic_energy, strain_energy, total_energy, v_r, v_z = safe_energy_calculation(
            Q, rho_grid, lam_grid, mu_grid)
        
        # 更新2D场图像
        im1.set_array(v_z)
        vz_min, vz_max = np.percentile(v_z[np.isfinite(v_z)], [1, 99])
        if vz_max > vz_min:
            im1.set_clim(vmin=vz_min, vmax=vz_max)
        
        stress_field = Q[4]/1e6
        stress_min, stress_max = np.percentile(stress_field[np.isfinite(stress_field)], [1, 99])
        im2.set_array(stress_field)
        if stress_max > stress_min:
            im2.set_clim(vmin=stress_min, vmax=stress_max)
        
        log_energy = np.log10(total_energy + 1e-10)
        energy_min, energy_max = np.percentile(log_energy[np.isfinite(log_energy)], [1, 99])
        im3.set_array(log_energy)
        if energy_max > energy_min:
            im3.set_clim(vmin=energy_min, vmax=energy_max)
        
        # 更新标题
        ax1.set_title(f'Vertical Velocity Field (t={current_time:.4f}s)')
        ax2.set_title(f'Vertical Stress Field (t={current_time:.4f}s)')
        ax3.set_title(f'Total Energy Density (t={current_time:.4f}s)')
        
        # 收集监测数据
        times.append(current_time)
        
        # 安全获取监测点数据
        def safe_get_value(array, i, j, default=0.0):
            try:
                val = array[i, j]
                return val if np.isfinite(val) else default
            except:
                return default
        
        # 近场和远场监测
        near_field_data['v_z'].append(safe_get_value(v_z, shallow_z, near_field_r))
        near_field_data['stress'].append(safe_get_value(Q[4]/1e6, shallow_z, near_field_r))
        near_field_data['energy'].append(safe_get_value(total_energy, shallow_z, near_field_r))
        
        far_field_data['v_z'].append(safe_get_value(v_z, shallow_z, far_field_r))
        far_field_data['stress'].append(safe_get_value(Q[4]/1e6, shallow_z, far_field_r))
        far_field_data['energy'].append(safe_get_value(total_energy, shallow_z, far_field_r))
        
        # 浅部和深部监测
        shallow_data['v_z'].append(safe_get_value(v_z, shallow_z, near_field_r))
        shallow_data['energy'].append(safe_get_value(total_energy, shallow_z, near_field_r))
        
        deep_data['v_z'].append(safe_get_value(v_z, deep_z, near_field_r))
        deep_data['energy'].append(safe_get_value(total_energy, deep_z, near_field_r))
        
        # 更新监测图
        line_nf_vz.set_data(times, near_field_data['v_z'])
        line_nf_stress.set_data(times, near_field_data['stress'])
        line_ff_vz.set_data(times, far_field_data['v_z'])
        line_ff_stress.set_data(times, far_field_data['stress'])
        
        line_sh_energy.set_data(times, shallow_data['energy'])
        line_dp_energy.set_data(times, deep_data['energy'])
        line_sh_vz.set_data(times, shallow_data['v_z'])
        line_dp_vz.set_data(times, deep_data['v_z'])
        
        # 更新深度剖面
        center_idx = 0  # r=0处
        depth_vz = v_z[:, center_idx]
        depth_energy = total_energy[:, center_idx] * 1e-6
        
        line_depth_vz.set_data(data['z_centers'], depth_vz)
        line_depth_energy.set_data(data['z_centers'], depth_energy)
        
        def safe_set_limits(ax, x_data, y_data, margin=0.1):
            try:
                if len(x_data) > 0 and len(y_data) > 0:
                    x_data = np.array(x_data)
                    y_data = np.array(y_data)
                    
                    valid_x = x_data[np.isfinite(x_data)]
                    valid_y = y_data[np.isfinite(y_data)]
                    
                    if len(valid_x) > 0:
                        x_min, x_max = np.min(valid_x), np.max(valid_x)
                        if x_max > x_min:
                            ax.set_xlim(x_min, x_max)
                        else:
                            ax.set_xlim(x_min - 0.1, x_min + 0.1)
                    
                    if len(valid_y) > 0:
                        y_min, y_max = np.min(valid_y), np.max(valid_y)
                        if y_max > y_min:
                            y_range = y_max - y_min
                            ax.set_ylim(y_min - margin * y_range, y_max + margin * y_range)
                        else:
                            ax.set_ylim(y_min - 0.1, y_min + 0.1)
            except Exception as e:
                print(f"Warning: Could not set axis limits: {e}")
        
        if len(times) > 1:
            all_vz = near_field_data['v_z'] + far_field_data['v_z']
            all_stress = near_field_data['stress'] + far_field_data['stress']
            safe_set_limits(ax4, times, all_vz + all_stress)
            
            all_energy = shallow_data['energy'] + deep_data['energy']
            all_vz_depth = shallow_data['v_z'] + deep_data['v_z']
            safe_set_limits(ax5, times, all_energy + all_vz_depth)
        
        safe_set_limits(ax6, data['z_centers'], np.concatenate([depth_vz, depth_energy]))
        
        max_energy = np.max(total_energy[np.isfinite(total_energy)]) if np.any(np.isfinite(total_energy)) else 0
        time_text.set_text(f'Time: {current_time:.4f}s | Frame: {frame+1}/{len(all_data)} | '
                          f'Max Energy: {max_energy:.2e} J/m³')
        
        return (im1, im2, im3, line_nf_vz, line_nf_stress, line_ff_vz, line_ff_stress,
                line_sh_energy, line_dp_energy, line_sh_vz, line_dp_vz, 
                line_depth_vz, line_depth_energy, time_text)
    
    # 创建动画
    ani = animation.FuncAnimation(
        fig, 
        update, 
        frames=len(all_data),
        interval=500,  # 500毫秒
        blit=False,
        repeat=True
    )
    

    ani.save('wave_propagation_enhanced_animation.gif', writer='pillow', fps=2, dpi=100)
    print("Enhanced animation saved as wave_propagation_enhanced_animation.gif")
    
    plt.close(fig)

if __name__ == "__main__":
    final_Q = main_solver()
    
    if rank == 0:
        global_grid = {
            'r_centers': np.linspace(0, R_max, Nr),
            'z_centers': np.linspace(0, Z_max, Nz)
        }
        
        print("Creating enhanced visualizations...")
        visualize_results()
        print("All visualizations completed!")
    
    MPI.Finalize()