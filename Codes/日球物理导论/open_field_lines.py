"""
open_field_lines.py — X-wind 开放磁力线生成

开放磁力线锚定在盘面 (θ=π/2) 上的 r_0 处。在 X-wind 模型中,
磁力线必须在盘面附近强烈向外弯曲 (离心力驱动), 并在远离盘面处
延伸至无穷远。

磁力线参数化:

    r(θ) = r_0 × [sin²θ + alpha × (π/2 - θ) + cot²θ]

- 线性项 alpha×(π/2-θ): 提供盘面附近的向外曲率
  dr/dθ|_(θ=π/2) = -alpha × r_0 → 强向外
- cot²θ: 确保远处延伸至无穷 (θ→0 时 r→∞)
- 单调性: dr/dθ < 0 对所有 θ∈(0,π/2) 当 alpha ≥ 1

参考: Shu et al. 1994, ApJ 429, 781 — X-wind 开放磁力线在盘面
外侧向外弯曲, 使离盘气体以超开普勒速度旋转。
"""

import numpy as np
from constants import theta_min


def single_field_line(r_0, n_pts=500, alpha=1.0):
    """
    生成一根开放磁力线。

    参数
    ----
    r_0 : float
        磁力线足点在赤道面的半径 (cm)
    n_pts : int
        分点数
    alpha : float
        磁场张开参数 (≥1 保证单调性; 越大磁力线在盘面附近越快向外弯曲)

    返回
    ----
    r, theta : 1-D ndarray
    s         : 弧长 (cm), s=0 在赤道面
    """
    theta = np.linspace(np.pi / 2, theta_min, n_pts)

    # r(θ) = r_0 × [sin²θ + alpha×(π/2-θ) + cot²θ]
    sin_th = np.sin(theta)
    cos_th = np.cos(theta)
    dtheta = np.pi / 2 - theta  # 偏离赤道面的角度, ≥ 0

    cot2 = np.zeros(n_pts)
    mask = sin_th > 1e-30
    cot2[mask] = (cos_th[mask] / sin_th[mask]) ** 2
    cot2[0] = 0.0  # θ=π/2: cot²θ = 0 exactly

    r = r_0 * (sin_th ** 2 + alpha * dtheta + cot2)

    # 弧长: ds/dθ = sqrt((dr/dθ)² + r²)
    # dr/dθ = r_0 × [sin(2θ) - alpha - 2·cotθ/sin²θ]
    #        = r_0 × [sin(2θ) - alpha - 2·cosθ/sin³θ]
    dr_dtheta = np.zeros(n_pts)
    for i in range(n_pts):
        if sin_th[i] > 1e-30:
            dr_dtheta[i] = r_0 * (
                np.sin(2 * theta[i])
                - alpha
                - 2.0 * cos_th[i] / sin_th[i] ** 3
            )
        else:
            dr_dtheta[i] = -alpha * r_0  # θ→0 极限
    # θ=π/2: dr/dθ = r_0 × [0 - alpha - 0] = -alpha × r_0
    dr_dtheta[0] = -alpha * r_0

    ds_dtheta = np.sqrt(dr_dtheta ** 2 + r ** 2)
    s = np.zeros(n_pts)
    for i in range(1, n_pts):
        s[i] = s[i - 1] + 0.5 * (ds_dtheta[i] + ds_dtheta[i - 1]) * (
            theta[i - 1] - theta[i]
        )

    return r, theta, s


def open_field_lines(R_X, n_lines=6, alpha=1.0):
    """
    生成一组开放磁力线，足点半径从 1.05*R_X 到 2.5*R_X 均匀分布。

    参数
    ----
    R_X : float
        X-point 半径 (cm)
    n_lines : int
        磁力线条数
    alpha : float
        磁场张开参数 (≥1 保证单调性; 越大磁力线在盘面附近越快向外弯曲)

    返回
    ----
    lines : list of dict
        每条包含 {'r_0': float, 'r': array, 'theta': array, 's': array}
    """
    # X-wind field lines: footpoints OUTSIDE R_X where Ω_K < Ω_X,
    # so corotation gives super-Keplerian rotation → centrifugal ejection.
    r_0_values = np.linspace(1.05 * R_X, 2.5 * R_X, n_lines)
    lines = []
    for r0 in r_0_values:
        r, theta, s = single_field_line(r0, n_pts=500, alpha=alpha)
        lines.append({"r_0": r0, "r": r, "theta": theta, "s": s})
    return lines


def field_line_geometry(r_0, n_pts=500, alpha=1.0):
    """
    便捷接口：生成单条磁力线的几何信息，与 trace_field_line 兼容。
    """
    r, theta, s = single_field_line(r_0, n_pts, alpha)
    return r, theta, s
