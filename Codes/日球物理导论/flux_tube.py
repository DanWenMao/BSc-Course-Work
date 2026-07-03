"""
flux_tube.py — 磁通量管截面面积与有效势

沿开放磁力线计算:
  - A(s) ∝ 1/B(s)     (磁通量守恒: B·A = const)
  - Ψ_eff(s) = -GM/r(s) - ½ Ω_X² ϖ²(s)   (共转系有效势)
  - 数值导数: dΨ_eff/ds, d(ln A)/ds      (用于声速点定位)

"""

import numpy as np
from constants import G, M_star
from dipole_field import B_field


def flux_tube_area(r, theta):
    """
    磁通量管截面面积 (归一化, A ∝ 1/B)。

    返回相对面积 A_rel = 1/|B| (任意归一化, 在后续 Bernoulli 求解中
    归一化常数被吸收进常数 C)。
    """
    _, _, B_mag = B_field(r, theta)
    return 1.0 / B_mag


def effective_potential(r, theta, Omega_X):
    """
    共转参考系中的有效势 (单位质量)。

    Ψ_eff = -GM/r - ½ Ω_X² ϖ²

    参数
    ----
    r, theta : 标量或数组
    Omega_X : float
        Keplar 角速度 at X-point

    返回
    ----
    Psi_eff : 标量或数组 (erg/g ≡ cm²/s²)
    """
    varpi = r * np.sin(theta)  # 柱半径
    return -G * M_star / r - 0.5 * Omega_X ** 2 * varpi ** 2


def compute_along_fieldline(r, theta, s, Omega_X):
    """
    沿磁力线计算全部几何/物理量。

    参数
    ----
    r, theta, s : 1-D ndarray
        磁力线坐标与弧长
    Omega_X : float
        共转角速度

    返回
    ----
    dict:
        's'        : 弧长
        'A'        : 磁通量管截面面积 (相对值)
        'Psi_eff'  : 有效势
        'dPsi_ds'  : dΨ_eff/ds (数值微分)
        'dlnA_ds'  : d(ln A)/ds (数值微分)
        'varpi'    : 柱半径
    """
    A = flux_tube_area(r, theta)
    Psi = effective_potential(r, theta, Omega_X)
    varpi = r * np.sin(theta)

    # 数值微分 (中心差分, 边界用单侧)
    dPsi_ds = np.zeros_like(s)
    dlnA_ds = np.zeros_like(s)

    lnA = np.log(A)

    n = len(s)
    ds = np.diff(s)
    # 内部点: 中心差分
    for i in range(1, n - 1):
        ds_fwd = s[i + 1] - s[i]
        ds_bwd = s[i] - s[i - 1]
        tot = ds_fwd + ds_bwd
        dPsi_ds[i] = (Psi[i + 1] - Psi[i - 1]) / tot
        dlnA_ds[i] = (lnA[i + 1] - lnA[i - 1]) / tot

    # 边界: 单侧差分
    if n >= 2:
        dPsi_ds[0] = (Psi[1] - Psi[0]) / (s[1] - s[0])
        dPsi_ds[-1] = (Psi[-1] - Psi[-2]) / (s[-1] - s[-2])
        dlnA_ds[0] = (lnA[1] - lnA[0]) / (s[1] - s[0])
        dlnA_ds[-1] = (lnA[-1] - lnA[-2]) / (s[-1] - s[-2])

    return {
        "s": s,
        "A": A,
        "Psi_eff": Psi,
        "dPsi_ds": dPsi_ds,
        "dlnA_ds": dlnA_ds,
        "varpi": varpi,
    }
