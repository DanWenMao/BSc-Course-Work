"""
cai_dynamics.py — CAI 颗粒轨道积分 (2.5D 含角动量)

在柱坐标 (ϖ, z) 下求解颗粒运动方程，包含方位向角动量 L = ϖ·v_φ:

状态矢量 y = [ϖ, z, v_ϖ, v_z, L]

  dϖ/dt  = v_ϖ
  dz/dt  = v_z
  dv_ϖ/dt = -GM/r³ · ϖ + L²/ϖ³ + (v_{w,ϖ} - v_ϖ)/t_stop
  dv_z/dt = -GM/r³ · z   + (v_{w,z} - v_z)/t_stop
  dL/dt   = ϖ · (v_{w,φ} - v_φ)/t_stop

其中:
  r = √(ϖ²+z²)
  v_φ = L/ϖ
  v_{w,φ} = Ω_X · ϖ  (等转动定理: 风沿磁力线以恒定 Ω_X 共转)
  v_{w,ϖ}, v_{w,z} 由风场插值得到

引力 + 离心力共同决定径向运动，方位向拖曳驱动角动量交换。
"""

import numpy as np
from scipy.integrate import solve_ivp
from constants import G, M_star


class WindInterpolator:
    """风场插值器：由 (r, θ) 网格上的 (v_r, v_θ) 提供任意点的风速。"""

    def __init__(self, r_grid, theta_grid, v_r, v_theta):
        from scipy.interpolate import RegularGridInterpolator

        self._r_1d = r_grid[:, 0]
        self._theta_1d = theta_grid[0, :]
        self._interp_vr = RegularGridInterpolator(
            (self._r_1d, self._theta_1d), v_r,
            bounds_error=False, fill_value=0.0
        )
        self._interp_vtheta = RegularGridInterpolator(
            (self._r_1d, self._theta_1d), v_theta,
            bounds_error=False, fill_value=0.0
        )

    def __call__(self, r, theta):
        """返回 (v_r, v_θ) 在 (r, theta) 处的值。"""
        pt = np.array([[r, theta]])
        vr = float(self._interp_vr(pt)[0])
        vt = float(self._interp_vtheta(pt)[0])
        return vr, vt


class ParticleSimulation:
    """单颗粒轨道积分 (2.5D)。"""

    def __init__(self, a_cm, Omega_X, rho_g_func, wind_interp, t_stop_func):
        """
        参数
        ----
        a_cm : float
            颗粒半径 (cm)
        Omega_X : float
            风共转角速度 (rad/s)
        rho_g_func : callable(r, theta) -> float
        wind_interp : WindInterpolator
        t_stop_func : callable(a, rho_g) -> float
        """
        self.a = a_cm
        self.Omega_X = Omega_X
        self.rho_g_func = rho_g_func
        self.wind = wind_interp
        self.t_stop_func = t_stop_func

    def _wind_full(self, r, theta, varpi):
        """
        获取风的全速度矢量 (v_ϖ, v_z, v_φ) 在 (r, θ) 处。

        v_φ = Ω_X · ϖ (等转动)
        """
        vr, vt = self.wind(r, theta)
        sin_th = np.sin(theta)
        cos_th = np.cos(theta)
        v_varpi = vr * sin_th + vt * cos_th
        v_z = vr * cos_th - vt * sin_th
        v_phi = self.Omega_X * varpi
        return v_varpi, v_z, v_phi

    def _ode_rhs(self, t, y):
        """
        ODE: y = [ϖ, z, v_ϖ, v_z, L]
        """
        varpi, z, v_varpi, v_z, L = y
        r = np.sqrt(varpi ** 2 + z ** 2)
        r_safe = max(r, 1e10)
        varpi_safe = max(varpi, 1e10)

        theta = np.arctan2(varpi, z)
        v_phi = L / varpi_safe

        # 引力
        grav_factor = -G * M_star / r_safe ** 3
        a_grav_varpi = grav_factor * varpi
        a_grav_z = grav_factor * z

        # 离心加速度 (径向, 在柱坐标中)
        a_cent_varpi = L ** 2 / varpi_safe ** 3

        # 风速
        vw_varpi, vw_z, vw_phi = self._wind_full(r_safe, theta, varpi)

        # 拖曳
        rho_g = self.rho_g_func(r_safe, theta)
        rho_g_safe = max(rho_g, 1e-25)
        t_stop = self.t_stop_func(self.a, rho_g_safe)

        a_drag_varpi = (vw_varpi - v_varpi) / t_stop
        a_drag_z = (vw_z - v_z) / t_stop

        # 角动量变化率: dL/dt = ϖ · a_drag_φ
        dL_dt = varpi * (vw_phi - v_phi) / t_stop

        return [
            v_varpi,
            v_z,
            a_grav_varpi + a_cent_varpi + a_drag_varpi,
            a_grav_z + a_drag_z,
            dL_dt,
        ]

    def integrate(self, y0, t_span, t_eval=None, **kwargs):
        """
        积分颗粒轨道。

        参数
        ----
        y0 : array (5,)
            [ϖ, z, v_ϖ, v_z, L]
        t_span : tuple
        t_eval : array, 可选

        返回
        ----
        sol : OdeSolution
        """
        kwargs.setdefault("rtol", 1e-6)
        kwargs.setdefault("atol", 1e-8)
        kwargs.setdefault("method", "LSODA")  # 自动处理刚性/非刚性
        kwargs.setdefault("max_step", t_span[1] / 500)  # 限制步长防止紧密耦合颗粒的数值爆炸
        
        # Early termination events
        from constants import R_star, AU
        r_escape = 10.0 * AU  # 逃逸判据：10 AU
        
        def hit_star(t, y):
            varpi, z, _, _, _ = y
            r = np.sqrt(varpi**2 + z**2)
            return r - R_star
        hit_star.terminal = True
        hit_star.direction = -1  # 仅在穿过R_star向内时触发
        
        def escaped(t, y):
            varpi, z, _, _, _ = y
            r = np.sqrt(varpi**2 + z**2)
            return r - r_escape
        escaped.terminal = True
        escaped.direction = 1  # 仅在穿过r_escape向外时触发
        
        kwargs.setdefault("events", [hit_star, escaped])
        
        return solve_ivp(self._ode_rhs, t_span, y0, t_eval=t_eval, **kwargs)


def run_particles(
    particle_radii,
    Omega_X,
    y0_array,
    t_span,
    rho_g_func,
    wind_interp,
    t_stop_func,
    **kwargs,
):
    """
    运行多个颗粒的轨道积分。

    返回
    ----
    trajectories : list of dict
        每个包含 'a', 't', 'varpi', 'z', 'r', 'v_varpi', 'v_z', 'v_phi', 'L'
    """
    trajectories = []
    for i, a_cm in enumerate(particle_radii):
        sim = ParticleSimulation(
            a_cm, Omega_X, rho_g_func, wind_interp, t_stop_func
        )
        sol = sim.integrate(y0_array[i], t_span, **kwargs)

        varpi = sol.y[0, :]
        z = sol.y[1, :]
        r = np.sqrt(varpi ** 2 + z ** 2)
        L = sol.y[4, :]
        varpi_safe = np.maximum(varpi, 1e10)
        v_phi = L / varpi_safe

        trajectories.append(
            {
                "a": a_cm,
                "t": sol.t,
                "varpi": varpi,
                "z": z,
                "r": r,
                "v_varpi": sol.y[2, :],
                "v_z": sol.y[3, :],
                "v_phi": v_phi,
                "L": L,
            }
        )
    return trajectories
