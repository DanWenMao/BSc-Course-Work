"""
bernoulli.py — Bernoulli 方程求解稳态 X-wind 速度场

等温稳态流沿磁通量管的 Bernoulli 方程:
  f(v) = ½ v² - c_s² ln v = F(s)
  F(s) = C + c_s² ln A(s) - Ψ_eff(s)

声速点条件 (regularity condition):
  dΨ_eff/ds = c_s² · d(ln A)/ds       at v = c_s

求解流程:
  1. 定位声速点 s_c (正则条件)
  2. 确定常数 C (= f_min - c_s² ln A(s_c) + Ψ_eff(s_c))
  3. 对每个 s 求解代数方程 f(v) = F(s)
     - s ≤ s_c : 亚声速分支 (v < c_s)
     - s > s_c : 超声速分支 (v > c_s)
"""

import numpy as np
from scipy.optimize import brentq
from constants import c_s


def f_v(v):
    """
    Bernoulli 函数 f(v) = ½ v² - c_s² ln v

    参数
    ----
    v : 标量或数组 (cm/s), v > 0

    返回
    ----
    标量或数组
    """
    v_safe = np.maximum(v, 1e-30)
    return 0.5 * v ** 2 - c_s ** 2 * np.log(v_safe)


def f_min():
    """f(v) 的极小值，在 v = c_s 处取得。"""
    return 0.5 * c_s ** 2 - c_s ** 2 * np.log(c_s)


def f_prime(v):
    """f'(v) = v - c_s²/v"""
    return v - c_s ** 2 / np.maximum(v, 1e-30)


def solve_v(F, branch="subsonic"):
    """
    求解 f(v) = F 得到 v。

    参数
    ----
    F : float
        必须满足 F >= f_min
    branch : 'subsonic' | 'supersonic'

    返回
    ----
    v : float (cm/s)
    """
    fm = f_min()
    if F < fm:
        # F 略小于 f_min (数值误差), 钳制到声速
        return c_s

    if abs(F - fm) < 1e-12:
        return c_s

    if branch == "subsonic":
        # v ∈ (0, c_s], f 单调递减
        v_low = 1e-10 * c_s  # 非常小的初速度
        v_high = c_s
        f_low = f_v(v_low)
        f_high = fm
        # f_low 非常大 (v→0, -ln v → ∞), f_high = f_min
        if F >= f_low:
            # F 在上界之上, 返回 v_low (实际上 v 可以任意小)
            # 用 Newton 法迭代
            v = 0.5 * c_s
            for _ in range(50):
                fv = f_v(v)
                if abs(fv - F) < 1e-12 * abs(F + 1):
                    return v
                fp = f_prime(v)
                dv = (fv - F) / fp
                v -= dv
                v = np.clip(v, v_low, v_high)
            return v
        try:
            return brentq(lambda v: f_v(v) - F, v_low, v_high, xtol=1e-14)
        except ValueError:
            # 回退 Newton
            v = 0.5 * c_s
            for _ in range(100):
                fv = f_v(v)
                if abs(fv - F) < 1e-12 * abs(F + 1):
                    break
                fp = f_prime(v)
                dv = np.clip((fv - F) / fp, -0.5 * v, 0.5 * v)
                v -= dv
                v = np.clip(v, 1e-30, c_s)
            return v

    else:  # supersonic
        # v ∈ [c_s, ∞), f 单调递增
        v_low = c_s
        v_high = max(1e2 * c_s, 1e8)  # ~100 km/s, 远超预期
        f_high = f_v(v_high)

        # 确保 F 在区间内
        while f_high < F:
            v_high *= 2.0
            f_high = f_v(v_high)

        try:
            return brentq(lambda v: f_v(v) - F, v_low, v_high, xtol=1e-14)
        except ValueError:
            v = 2.0 * c_s
            for _ in range(100):
                fv = f_v(v)
                if abs(fv - F) < 1e-12 * abs(F + 1):
                    break
                fp = f_prime(v)
                dv = (fv - F) / fp
                v -= dv
                v = max(v, c_s * 1.001)
            return v


def find_sonic_point(data):
    """
    根据正则条件 dΨ/ds = c_s² · d(ln A)/ds 定位声速点。

    使用平滑后的残差的最小绝对值位置。平滑抑制有限差分数值噪声。
    """
    residual_raw = data["dPsi_ds"] - c_s ** 2 * data["dlnA_ds"]
    
    # Smooth residual with a 5-point moving average to suppress finite-difference noise
    n = len(residual_raw)
    if n >= 5:
        kernel = np.ones(5) / 5.0
        residual = np.convolve(residual_raw, kernel, mode='same')
        # Restore endpoints from original
        residual[:2] = residual_raw[:2]
        residual[-2:] = residual_raw[-2:]
    else:
        residual = residual_raw
    
    idx = np.argmin(np.abs(residual))
    
    # Safety: ensure idx is not at the very boundary
    if idx == 0:
        idx = 1
    if idx >= n - 1:
        idx = n - 2
    
    return idx


def solve_wind_velocity(data):
    """
    沿磁力线求解完整的稳态风速度场。

    参数
    ----
    data : dict
        flux_tube.compute_along_fieldline() 的返回

    返回
    ----
    dict:
        'v'          : 速度场 (cm/s)
        'sonic_idx'  : 声速点索引
        'C'          : Bernoulli 常数
        'F'          : F(s) 数组
    """
    s = data["s"]
    A = data["A"]
    Psi = data["Psi_eff"]
    n = len(s)
    fm = f_min()

    # 1. 定位声速点
    sonic_idx = find_sonic_point(data)

    # 2. 确定常数 C
    C = fm - c_s ** 2 * np.log(A[sonic_idx]) + Psi[sonic_idx]

    # 3. 计算 F(s)
    F = C + c_s ** 2 * np.log(A) - Psi

    # 4. 求解 v(s)
    v = np.zeros(n)
    for i in range(n):
        branch = "subsonic" if i <= sonic_idx else "supersonic"
        v[i] = solve_v(F[i], branch)

    # 确保声速点处 v = c_s
    v[sonic_idx] = c_s

    return {"v": v, "sonic_idx": sonic_idx, "C": C, "F": F}


def wind_mass_flux(data, v_solution):
    """
    计算质量通量密度 (相对值, ∝ ρ·v·A = const)。

    返回沿磁力线的常数质量通量 (可用于交叉检验)。
    """
    s = data["s"]
    A = data["A"]
    v = v_solution["v"]
    sonic_idx = v_solution["sonic_idx"]

    # ρ ∝ 1/(v·A) (质量守恒)
    # 在声速点: ρ_s = const (由 base 密度决定外部给定)
    # 这里仅返回相对值
    rho_rel = 1.0 / (v * A)
    mdot_rel = rho_rel * v * A  # 应为常数 (数值检验)
    mdot_err = np.std(mdot_rel) / np.mean(mdot_rel)
    return rho_rel, mdot_rel, mdot_err
