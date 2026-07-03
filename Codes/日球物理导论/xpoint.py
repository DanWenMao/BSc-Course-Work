"""
xpoint.py — X-point 参数计算

磁层截断半径 R_X:
  R_X = k (μ⁴ / (G M_* Ṁ²))^(1/7)

其中 μ = B_* R_*³ 为恒星磁矩。

共转半径:
  R_co = (G M_* / Ω_*²)^(1/3)

"""

import numpy as np
from constants import G, M_star, R_star, B_star, M_dot, yr, k_X, Omega_star


def magnetic_moment():
    """返回恒星磁矩 μ = B_* R_*³ (G·cm³)"""
    return B_star * R_star ** 3


def truncation_radius(mu=None, k=None):
    """
    计算磁层截断半径 R_X (cm)。

    参数
    ----
    mu : float, 可选
        恒星磁矩 (G·cm³), 默认由 magnetic_moment() 计算
    k  : float, 可选
        无量纲常数, 默认 k_X

    返回
    ----
    R_X : float (cm)
    """
    if mu is None:
        mu = magnetic_moment()
    if k is None:
        k = k_X

    M_dot_cgs = M_dot * M_star / yr  # g/s  (M_dot 以 M⊙/yr 给出)

    numerator = mu ** 4
    denominator = G * M_star * M_dot_cgs ** 2
    R_X = k * (numerator / denominator) ** (1.0 / 7.0)
    return R_X


def corotation_radius(Omega):
    """共转半径 R_co = (G M_* / Ω²)^(1/3) (cm)"""
    return (G * M_star / Omega ** 2) ** (1.0 / 3.0)


def set_stellar_rotation(R_X):
    """
    设定恒星自转角速度，使共转半径恰好等于 R_X。

    Ω_* = √(G M_* / R_X³)
    """
    Omega = np.sqrt(G * M_star / R_X ** 3)
    global Omega_star
    Omega_star = Omega
    return Omega
