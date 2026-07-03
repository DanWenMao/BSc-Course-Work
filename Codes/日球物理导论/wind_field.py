"""
wind_field.py — 二维风场构建

将多条开放磁力线上的 1-D 风解插值到 2-D 球坐标网格 (r, θ)，
得到 v_r(r,θ), v_θ(r,θ)。

风矢量沿磁场线方向:  v̂ 沿磁力线切线方向
速度模 |v| 由 Bernoulli 解给出。

插值策略: 对每条磁力线在 (r,θ) 空间做 Delaunay 三角剖分后线性插值。
凸包外的点通过最近邻回退处理。
"""

import numpy as np
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator
from constants import theta_min


def build_wind_field(field_lines, wind_solutions, r_grid, theta_grid, R_X=None):
    """
    构建 2-D 风场。

    参数
    ----
    field_lines : list of dict
        open_field_lines.open_field_lines() 的输出
    wind_solutions : list of dict
        每条磁力线对应的 bernoulli.solve_wind_velocity() 输出
    r_grid : 2-D ndarray
        网格 r 坐标 (cm)
    theta_grid : 2-D ndarray
        网格 θ 坐标 (rad)
    R_X : float, 可选
        X-point 半径。若提供, r < R_X 区域风速强制为 0

    返回
    ----
    v_r, v_theta, v_mag : 2-D ndarray (cm/s)
    """
    # 收集所有磁力线上的点, 裁剪到网格范围内
    all_r = []
    all_theta = []
    all_v = []

    r_max = r_grid.max()
    theta_max = theta_grid.max()
    theta_min_grid = theta_grid.min()

    for fl, ws in zip(field_lines, wind_solutions):
        r = fl["r"]
        theta = fl["theta"]
        v = ws["v"]
        in_bounds = (r <= r_max) & (theta >= theta_min_grid) & (theta <= theta_max)
        all_r.append(r[in_bounds])
        all_theta.append(theta[in_bounds])
        all_v.append(v[in_bounds])

    all_r = np.concatenate(all_r)
    all_theta = np.concatenate(all_theta)
    all_v = np.concatenate(all_v)

    # 构建插值器 (速度模)
    # 保留 v=0 的基态点, 使 Delaunay 凸包延伸到盘面
    points = np.column_stack([all_r, all_theta])
    mask = np.isfinite(all_r) & np.isfinite(all_theta) & np.isfinite(all_v) & (all_v >= 0)
    points = points[mask]
    all_v_clean = all_v[mask]

    interp_v = LinearNDInterpolator(points, all_v_clean, fill_value=float('nan'))
    interp_v_near = NearestNDInterpolator(points, all_v_clean)

    r_flat = r_grid.ravel()
    theta_flat = theta_grid.ravel()
    v_flat = interp_v(r_flat, theta_flat)
    nan_mask = ~np.isfinite(v_flat)
    if np.any(nan_mask):
        v_flat[nan_mask] = interp_v_near(r_flat[nan_mask], theta_flat[nan_mask])

    v_mag = v_flat.reshape(r_grid.shape)

    # 风速方向: 从磁力线数据点计算局部切线方向, 插值到网格
    all_dir_r = []
    all_dir_theta = []
    for fl in field_lines:
        r_fl = fl["r"]
        th_fl = fl["theta"]
        in_bounds = (r_fl <= r_max) & (th_fl >= theta_min_grid) & (th_fl <= theta_max)
        r_fl = r_fl[in_bounds]
        th_fl = th_fl[in_bounds]
        n = len(r_fl)
        dir_r_fl = np.zeros(n)
        dir_th_fl = np.zeros(n)
        for i in range(1, n - 1):
            dr = r_fl[i + 1] - r_fl[i - 1]
            dth = th_fl[i + 1] - th_fl[i - 1]
            d_orth = np.array([dr, r_fl[i] * dth])
            norm = np.sqrt(d_orth[0]**2 + d_orth[1]**2)
            if norm > 0:
                dir_r_fl[i] = d_orth[0] / norm
                dir_th_fl[i] = d_orth[1] / norm
        if n >= 2:
            dr0 = r_fl[1] - r_fl[0]
            dth0 = th_fl[1] - th_fl[0]
            d_orth0 = np.array([dr0, r_fl[0] * dth0])
            n0 = np.sqrt(d_orth0[0]**2 + d_orth0[1]**2)
            if n0 > 0:
                dir_r_fl[0] = d_orth0[0] / n0
                dir_th_fl[0] = d_orth0[1] / n0
            drN = r_fl[-1] - r_fl[-2]
            dthN = th_fl[-1] - th_fl[-2]
            d_orthN = np.array([drN, r_fl[-1] * dthN])
            nN = np.sqrt(d_orthN[0]**2 + d_orthN[1]**2)
            if nN > 0:
                dir_r_fl[-1] = d_orthN[0] / nN
                dir_th_fl[-1] = d_orthN[1] / nN
        all_dir_r.append(dir_r_fl[1:-1] if n > 2 else dir_r_fl)
        all_dir_theta.append(dir_th_fl[1:-1] if n > 2 else dir_th_fl)

    all_dir_r = np.concatenate(all_dir_r)
    all_dir_theta = np.concatenate(all_dir_theta)

    dir_points_list = []
    for fl in field_lines:
        r_fl = fl["r"]
        th_fl = fl["theta"]
        in_bounds = (r_fl <= r_max) & (th_fl >= theta_min_grid) & (th_fl <= theta_max)
        r_fl = r_fl[in_bounds]
        th_fl = th_fl[in_bounds]
        n = len(r_fl)
        if n > 2:
            dir_points_list.append(np.column_stack([r_fl[1:-1], th_fl[1:-1]]))
        else:
            dir_points_list.append(np.column_stack([r_fl, th_fl]))

    points_dir_raw = np.concatenate(dir_points_list)
    dir_r_raw = all_dir_r
    dir_th_raw = all_dir_theta
    dirmask = (np.isfinite(points_dir_raw[:, 0]) & np.isfinite(points_dir_raw[:, 1]) &
               np.isfinite(dir_r_raw) & np.isfinite(dir_th_raw))
    points_dir = points_dir_raw[dirmask]
    dir_r_clean = dir_r_raw[dirmask]
    dir_th_clean = dir_th_raw[dirmask]

    interp_dir_r = LinearNDInterpolator(points_dir, dir_r_clean, fill_value=float('nan'))
    interp_dir_th = LinearNDInterpolator(points_dir, dir_th_clean, fill_value=float('nan'))
    interp_dir_r_near = NearestNDInterpolator(points_dir, dir_r_clean)
    interp_dir_th_near = NearestNDInterpolator(points_dir, dir_th_clean)

    dir_r_flat = interp_dir_r(r_flat, theta_flat)
    dir_th_flat = interp_dir_th(r_flat, theta_flat)
    nan_dirmask = ~np.isfinite(dir_r_flat) | ~np.isfinite(dir_th_flat)
    if np.any(nan_dirmask):
        dir_r_flat[nan_dirmask] = interp_dir_r_near(r_flat[nan_dirmask], theta_flat[nan_dirmask])
        dir_th_flat[nan_dirmask] = interp_dir_th_near(r_flat[nan_dirmask], theta_flat[nan_dirmask])

    dir_mag_flat = np.sqrt(dir_r_flat**2 + dir_th_flat**2)
    dir_mag_safe = np.maximum(dir_mag_flat, 1e-30)
    dir_r_grid = (dir_r_flat / dir_mag_safe).reshape(r_grid.shape)
    dir_th_grid = (dir_th_flat / dir_mag_safe).reshape(r_grid.shape)

    dir_r_grid = np.maximum(dir_r_grid, 0.0)
    dir_norm = np.sqrt(dir_r_grid**2 + dir_th_grid**2)
    dir_norm_safe = np.maximum(dir_norm, 1e-30)
    dir_r_grid /= dir_norm_safe
    dir_th_grid /= dir_norm_safe

    v_r = v_mag * dir_r_grid
    v_theta = v_mag * dir_th_grid

    # R_X 内侧归零: 漏斗流/重联环区无 X-wind 子午面外流
    if R_X is not None:
        inside = r_grid < R_X
        v_r[inside] = 0.0
        v_theta[inside] = 0.0
        v_mag[inside] = 0.0

    return v_r, v_theta, v_mag
