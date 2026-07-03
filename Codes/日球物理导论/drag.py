"""
drag.py — Epstein 拖曳模型

Epstein 拖曳适用于颗粒半径 a ≪ 气体分子平均自由程 λ 的 free-molecular 流区。

拖曳加速度:
  a_drag = (v_wind - v_particle) / t_stop

Stopping time (Epstein):
  t_stop = (ρ_s · a) / (ρ_g · v_th)

其中 v_th = √(8 k_B T / (π μ m_H)) 为气体分子热运动速度。

Stokes 数:
  St = t_stop / t_dyn,  t_dyn = 2π/Ω_X

"""

import numpy as np
from constants import kB, mu_mol, mH, rho_CAI, T_wind

# 气体分子热运动速度 (cm/s)
_v_th = np.sqrt(8.0 * kB * T_wind / (np.pi * mu_mol * mH))


def thermal_velocity():
    """返回气体分子平均热运动速度 (cm/s)。"""
    return _v_th


def stopping_time(a, rho_g):
    """
    Epstein stopping time。

    参数
    ----
    a : float or array
        颗粒半径 (cm)
    rho_g : float or array
        局地气体密度 (g/cm³)

    返回
    ----
    t_stop : float or array (s)
    """
    return (rho_CAI * a) / (rho_g * _v_th)


def stokes_number(a, rho_g, Omega_X):
    """
    Stokes 数: St = t_stop / t_dyn

    参数
    ----
    a, rho_g : 同 stopping_time
    Omega_X : float
        轨道角速度 (rad/s)

    返回
    ----
    St : float or array
    """
    t_dyn = 2.0 * np.pi / Omega_X
    return stopping_time(a, rho_g) / t_dyn


def drag_acceleration(v_wind, v_particle, t_stop):
    """
    拖曳加速度矢量。

    参数
    ----
    v_wind : array (2,) or (N,2)
        风速矢量 (cm/s)
    v_particle : array (2,) or (N,2)
        颗粒速度矢量
    t_stop : float
        Stopping time (s)

    返回
    ----
    a_drag : array (2,) or (N,2)
        拖曳加速度 (cm/s²)
    """
    return (np.asarray(v_wind) - np.asarray(v_particle)) / t_stop


def compute_gas_density(r, theta, rho_base, v_solution, A_array):
    """
    根据质量守恒沿磁力线计算气体密度。

    ρ(s) = ρ_base · (v_base · A_base) / (v(s) · A(s))

    参数
    ----
    r, theta : arrays
        磁力线坐标
    rho_base : float
        基态气体密度 (g/cm³), 在 s=0 (盘面) 处
    v_solution : array
        沿磁力线的速度 (cm/s)
    A_array : array
        磁通量管截面面积

    返回
    ----
    rho_g : array
        气体密度沿磁力线 (g/cm³)
    """
    vA_0 = v_solution[0] * A_array[0]
    vA = v_solution * A_array
    vA_safe = np.where(vA < 1e-30, vA_0, vA)
    return rho_base * vA_0 / vA_safe
