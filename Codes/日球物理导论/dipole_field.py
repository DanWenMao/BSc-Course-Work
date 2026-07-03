"""
dipole_field.py — 恒星偶极磁场

坐标系：球坐标 (r, θ)，偶极轴沿 θ=0 (z 轴)。盘面在 θ=π/2 (赤道面)。

偶极磁场分量:
  B_r(r,θ) = 2 B_* (R_*/r)³ cos θ
  B_θ(r,θ) =   B_* (R_*/r)³ sin θ

偶极磁力线方程:
  r(θ) = R_eq sin² θ      (R_eq = 磁力线在赤道面的截距)

"""

import numpy as np
from constants import B_star, R_star


def B_field(r, theta):
    """
    返回偶极磁场在 (r, θ) 处的 (B_r, B_θ, |B|)。

    参数
    ----
    r, theta : 标量或等长数组
        球坐标 (cm, rad)

    返回
    ----
    B_r, B_theta, B_mag : 标量或数组 (G)
    """
    factor = B_star * (R_star / r) ** 3
    B_r = 2.0 * factor * np.cos(theta)
    B_theta = factor * np.sin(theta)
    B_mag = np.sqrt(B_r ** 2 + B_theta ** 2)
    return B_r, B_theta, B_mag


def field_line_equator_radius(r, theta):
    """
    根据场点 (r, θ) 推算该磁力线在赤道面的截距 R_eq。

    r = R_eq sin²θ  →  R_eq = r / sin²θ
    """
    sin_th = np.sin(theta)
    sin_th = np.where(sin_th < 1e-15, 1e-15, sin_th)  # 避免极点除零
    return r / sin_th ** 2


def trace_field_line(R_eq, n_pts=500):
    """
    追踪一根偶极磁力线：从赤道面 (θ=π/2) 到 θ_min。

    参数
    ----
    R_eq : float
        磁力线赤道面截距 (cm)
    n_pts : int
        沿磁力线的分点数

    返回
    ----
    r, theta : 1-D ndarray (从赤道向外排列)
    s         : 弧长 (cm), s=0 在赤道面
    B_mag     : |B| (G)
    """
    from constants import theta_min

    theta = np.linspace(np.pi / 2, theta_min, n_pts)
    r = R_eq * np.sin(theta) ** 2
    _, _, B_mag = B_field(r, theta)

    # 弧长用梯形积分
    # ds/dθ = √((dr/dθ)² + r²)
    dr_dtheta = 2.0 * R_eq * np.sin(theta) * np.cos(theta)
    ds_dtheta = np.sqrt(dr_dtheta ** 2 + r ** 2)
    s = np.zeros(n_pts)
    # θ 从 π/2 递减，但我们要 s 递增 (从盘面向外)，所以用累计积分
    for i in range(1, n_pts):
        s[i] = s[i - 1] + 0.5 * (ds_dtheta[i] + ds_dtheta[i - 1]) * abs(
            theta[i] - theta[i - 1]
        )

    return r, theta, s, B_mag


def truncate_dipole_line(r, theta, r_outer, r_inner=None):
    """
    将偶极磁力线截断到 [r_inner, r_outer] 区间内。

    r 沿磁力线从赤道 (r=R_eq, 最大) 向极区 (r≈0) 递减。
    截断保留 r_inner <= r <= r_outer 的部分 —
    即从星面 (r=R_star) 到磁层边界 (r=R_X) 的闭合段。

    参数
    ----
    r, theta : 1-D ndarray
        磁力线球坐标 (r 从赤道向极区递减)
    r_outer : float
        外侧截断半径 (cm), 保留 r <= r_outer 的部分 (盘侧)
    r_inner : float, 可选
        内侧截断半径 (cm), 保留 r >= r_inner 的部分 (星侧)
        默认 None = 不截断内侧

    返回
    ----
    r_clipped, theta_clipped : 1-D ndarray
        截断后的坐标数组。若整条线在有效区间外, 返回空数组。
    """
    if len(r) == 0:
        return np.array([]), np.array([])

    # --- 外侧截断 (盘侧): 保留 r <= r_outer ---
    mask_outer = r <= r_outer
    if not np.any(mask_outer):
        return np.array([]), np.array([])

    first_idx = int(np.argmax(mask_outer))  # 第一个 r <= r_outer

    # --- 内侧截断 (星侧): 保留 r >= r_inner ---
    if r_inner is not None:
        mask_inner = r >= r_inner
        if not np.any(mask_inner):
            return np.array([]), np.array([])
        last_idx = len(r) - 1 - int(np.argmax(mask_inner[::-1]))  # 最后一个 r >= r_inner
    else:
        last_idx = len(r) - 1

    if first_idx > last_idx:
        return np.array([]), np.array([])

    # 构建截断数组, 在外侧和内测截断处各插入精确边界点
    pieces_r = []
    pieces_theta = []

    # 外侧边界插值 (如需要)
    if first_idx > 0 and r[first_idx - 1] > r_outer:
        frac = (r_outer - r[first_idx - 1]) / (r[first_idx] - r[first_idx - 1])
        theta_outer = theta[first_idx - 1] + frac * (theta[first_idx] - theta[first_idx - 1])
        pieces_r.append(np.array([r_outer]))
        pieces_theta.append(np.array([theta_outer]))

    pieces_r.append(r[first_idx: last_idx + 1])
    pieces_theta.append(theta[first_idx: last_idx + 1])

    # 内侧边界插值 (如需要)
    if r_inner is not None and last_idx < len(r) - 1 and r[last_idx] > r_inner:
        frac = (r_inner - r[last_idx]) / (r[last_idx + 1] - r[last_idx])
        theta_inner = theta[last_idx] + frac * (theta[last_idx + 1] - theta[last_idx])
        pieces_r.append(np.array([r_inner]))
        pieces_theta.append(np.array([theta_inner]))

    r_clipped = np.concatenate(pieces_r)
    theta_clipped = np.concatenate(pieces_theta)

    return r_clipped, theta_clipped


def dipole_field_lines(n_lines=12, r_max=5.0):
    """
    生成用于背景展示的多条偶极磁力线 (赤道截距均匀分布)。

    参数
    ----
    n_lines : int
        磁力线条数
    r_max : float
        最外层磁力线的赤道截距 (AU)

    返回
    ----
    lines : list of (r, theta) 元组
        每条磁力线的 (r, theta) 坐标数组
    """
    from constants import AU

    R_eq_values = np.linspace(0.3 * R_star, r_max * AU, n_lines)
    lines = []
    for Req in R_eq_values:
        r, theta, _, _ = trace_field_line(Req, n_pts=300)
        lines.append((r, theta))
    return lines
