#!/usr/bin/env python3
"""
main.py — X-Wind Model: CAI Transport Simulation

完整流程:
  1. 计算 X-point 位置
  2. 生成偶极背景磁场
  3. 生成开放磁力线
  4. 沿磁力线计算磁通量管截面和有效势
  5. Bernoulli 方程求解稳态风速度
  6. 构建二维风场
  7. CAI 颗粒轨道积分
  8. 可视化与动画输出

用法:
  python main.py                 # 运行完整模拟 + 动画
  python main.py --no-anim       # 仅计算 + 静态图
"""

import sys
import numpy as np

# ============================================================================
# 导入所有模块
# ============================================================================
from constants import (
    G,
    M_star,
    R_star,
    B_star,
    M_dot,
    AU,
    yr,
    c_s,
    T_wind,
    rho_CAI,
    a_CAI_min,
    a_CAI_max,
    n_CAI,
    n_theta,
    theta_min,
    n_field_lines,
    n_field_lines_dipole,
    t_end,
    dt_output,
    rtol,
    atol,
    mu_mol,
    mH,
    kB,
    Omega_star,
)

from dipole_field import dipole_field_lines

from xpoint import truncation_radius, set_stellar_rotation, corotation_radius

from open_field_lines import open_field_lines

from flux_tube import compute_along_fieldline

from bernoulli import solve_wind_velocity, f_min, c_s as bernoulli_cs

from wind_field import build_wind_field

from drag import (
    stopping_time,
    thermal_velocity,
    compute_gas_density,
)

from cai_dynamics import WindInterpolator, run_particles

from visualization import (
    setup_figure,
    plot_background_field,
    plot_xpoint,
    plot_open_field_lines,
    CAIAnimator,
)


# ============================================================================
# 主流程
# ============================================================================
def main(animate=True):
    print("=" * 60)
    print("  X-Wind Model: CAI Transport Simulation")
    print("=" * 60)

    # ------------------------------------------------------------------
    # Step 1: X-point
    # ------------------------------------------------------------------
    print("\n[1/8] Computing X-point parameters ...")
    R_X = truncation_radius()
    Omega_X = set_stellar_rotation(R_X)
    R_co = corotation_radius(Omega_X)
    print(f"  B_*        = {B_star:.0f} G")
    print(f"  Ṁ         = {M_dot:.1e} M⊙/yr")
    print(f"  μ          = {B_star * R_star**3:.2e} G·cm³")
    print(f"  R_X        = {R_X/AU:.4f} AU = {R_X/R_star:.1f} R_star")
    print(f"  R_co       = {R_co/AU:.4f} AU")
    print(f"  Ω_X        = {Omega_X:.3e} rad/s (P = {2*np.pi/Omega_X/86400:.2f} d)")
    print(f"  c_s        = {c_s/1e5:.2f} km/s")

    # ------------------------------------------------------------------
    # Step 2: Dipole background
    # ------------------------------------------------------------------
    print("\n[2/8] Generating dipole field lines (star → disk inside R_X) ...")
    n_dip = n_field_lines_dipole
    # 偶极线赤道截距从星面到 X-point: 闭合场区域
    from dipole_field import trace_field_line
    R_eq_dipole = np.linspace(1.2 * R_star, R_X, n_dip)
    dipole_lines = []
    for Req in R_eq_dipole:
        r, theta, _, _ = trace_field_line(Req, n_pts=300)
        dipole_lines.append((r, theta))
    print(f"  {len(dipole_lines)} dipole lines (R_eq: "
          f"{R_eq_dipole[0]/R_star:.1f}–{R_eq_dipole[-1]/R_star:.1f} R_star, "
          f"outermost terminates at X-point)")

    # ------------------------------------------------------------------
    # Step 3: Open field lines
    # ------------------------------------------------------------------
    print("\n[3/8] Generating open field lines ...")
    n_fl = n_field_lines
    alpha = 1.0  # 张开参数（≥1 保证磁力线单调向外展开）
    flines = open_field_lines(R_X, n_lines=n_fl, alpha=alpha)
    print(f"  {len(flines)} open field lines (α = {alpha})")

    # 背景开放磁力线: 更密集的足点, 仅几何 (无风解)
    bg_flines = open_field_lines(R_X, n_lines=20, alpha=alpha)
    print(f"  {len(bg_flines)} background open field lines for visualization")

    # ------------------------------------------------------------------
    # Step 4: Flux tube & effective potential
    # ------------------------------------------------------------------
    print("\n[4/8] Computing flux tube geometry and effective potential ...")
    flux_data = []
    for fl in flines:
        fd = compute_along_fieldline(fl["r"], fl["theta"], fl["s"], Omega_X)
        flux_data.append(fd)
    print(f"  Computed for {len(flux_data)} field lines")

    # ------------------------------------------------------------------
    # Step 5: Bernoulli wind solution
    # ------------------------------------------------------------------
    print("\n[5/8] Solving Bernoulli equation for wind velocity ...")
    wind_solutions = []
    for i, fd in enumerate(flux_data):
        ws = solve_wind_velocity(fd)
        wind_solutions.append(ws)
        sonic_s = fd["s"][ws["sonic_idx"]]
        v_max = ws["v"][-1]
        print(
            f"  Line {i+1}: sonic at s={sonic_s/AU:.4f} AU, "
            f"v_max = {v_max/1e5:.2f} km/s "
            f"(M_max = {v_max/c_s:.2f})"
        )

    # ------------------------------------------------------------------
    # Step 6: 2-D wind field
    # ------------------------------------------------------------------
    print("\n[6/8] Building 2-D wind field on grid ...")
    nr = 200
    nth = 100
    r_1d = np.logspace(np.log10(0.5 * R_X), np.log10(0.5 * AU), nr)
    theta_1d = np.linspace(theta_min, np.pi / 2, nth)
    r_grid, theta_grid = np.meshgrid(r_1d, theta_1d, indexing="ij")

    v_r, v_theta, v_mag = build_wind_field(flines, wind_solutions, r_grid, theta_grid, R_X)
    print(f"  Grid: {nr}×{nth}, v_max = {v_mag.max()/1e5:.2f} km/s")

    # Build wind interpolator
    wind_interp = WindInterpolator(r_grid, theta_grid, v_r, v_theta)

    # ------------------------------------------------------------------
    # Step 7: CAI particle integration
    # ------------------------------------------------------------------
    print("\n[7/8] Integrating CAI particle trajectories ...")

    # Gas density
    from dipole_field import B_field
    _, _, B_grid = B_field(r_grid, theta_grid)
    v_mag_safe = np.where(v_mag < 1e2, 1e2, v_mag)
    rho_grid = B_grid / v_mag_safe
    rho_base = 2e-10  # g/cm³
    i_xp = np.argmin(np.abs(r_grid[:, 0] - R_X))
    norm_factor = rho_base / rho_grid[i_xp, -1]
    rho_grid *= norm_factor

    from scipy.interpolate import RegularGridInterpolator
    rho_interp = RegularGridInterpolator(
        (r_1d, theta_1d), rho_grid,
        bounds_error=False, fill_value=rho_base * 1e-6
    )

    def gas_density(r, theta):
        rho_coronal = 2e-16  # g/cm³, Shu (2001) §2.2
        if r < R_X:
            return rho_coronal
        pt = np.array([[r, theta]])
        return float(rho_interp(pt)[0])

    # ====================================================================
    # CAI initial conditions — 覆盖 R_X 内外, 表征初始状态的影响
    # ====================================================================
    # r 采样: R_X 内侧 (重联环) 和外侧 (风区) — quick 和 full 一致
    r_values_RX = np.array([0.85, 0.95, 1.05, 1.20])
    r_values = r_values_RX * R_X

    # θ 采样: 盘面上方
    theta_angles_deg = np.array([75, 85])
    theta_angles_rad = np.deg2rad(theta_angles_deg)

    # 粒径 — quick 和 full 一致
    a_values = np.array([1e-4, 1e-2, 1.0])  # 1μm, 100μm, 1cm

    # 角动量模式: K = 开普勒, C = 共转 (C 已注释——X-wind 岩石初始为开普勒)
    L_modes = ["K"]  # "C" commented out — rocks have Keplerian L from reconnection ring

    print(f"  Gas density at X-point: {rho_base:.1e} g/cm³")
    print(f"  r/R_X: {r_values_RX.tolist()}")
    print(f"  θ angles: {theta_angles_deg.tolist()} deg")
    print(f"  Particle radii: {a_values[0]*1e4:.2f} μm – {a_values[-1]:.2f} cm")
    print(f"  L modes: K=Keplerian, C=Corotation")

    t_span = (0, t_end)
    t_eval = np.arange(0, t_span[1], dt_output)
    print(f"  Integration time: {t_span[1]/yr:.1f} yr")

    # 为每个 (r, θ, a, L_mode) 组合生成初始条件
    y0_list = []
    particle_meta = []  # (r_idx, th_rad, a, L_mode)

    for i_r, r0 in enumerate(r_values):
        for th in theta_angles_rad:
            varpi0 = r0 * np.sin(th)
            z0 = r0 * np.cos(th)

            # 开普勒角动量: L_K = ϖ × v_K(ϖ)
            # v_K(ϖ) = √(GM/ϖ) for equatorial circular orbit
            L_keplerian = varpi0 * np.sqrt(G * M_star / varpi0)

            # 共转角动量: L_co = Ω_X × ϖ²
            L_corotation = Omega_X * varpi0 ** 2

            # 小的向上速度扰动 (帮助粒子离开盘面)
            vK_local = np.sqrt(G * M_star / r0)
            v_varpi0 = 0.0
            v_z0 = 0.005 * vK_local

            for L_mode in L_modes:
                L0 = L_keplerian if L_mode == "K" else L_corotation
                y0_base = [varpi0, z0, v_varpi0, v_z0, L0]
                for a in a_values:
                    y0_list.append(y0_base.copy())
                    particle_meta.append((i_r, th, a, L_mode))

    y0_array = np.array(y0_list)
    n_particles_total = len(y0_array)
    print(f"  Total particles: {n_particles_total}")

    # 展平粒径数组
    particle_radii_flat = np.tile(
        np.repeat(a_values, len(L_modes)),
        len(r_values) * len(theta_angles_rad)
    )

    trajectories = run_particles(
        particle_radii_flat,
        Omega_X,
        y0_array,
        t_span,
        gas_density,
        wind_interp,
        lambda a, rhog: stopping_time(a, rhog),
        t_eval=t_eval,
    )
    print(f"  {len(trajectories)} trajectories computed")

    # Add metadata to trajectories
    for i, (i_r, th, a, L_mode) in enumerate(particle_meta):
        trajectories[i]["r0_RX"] = r_values_RX[i_r]
        trajectories[i]["L_mode"] = L_mode
        trajectories[i]["inside"] = r_values_RX[i_r] < 1.0

    # Print summary — 按 r 和 L_mode 分组
    from drag import stokes_number

    for i_r, r_RX in enumerate(r_values_RX):
        region = "INSIDE" if r_RX < 1.0 else "OUTSIDE"
        marker = "▼" if r_RX < 1.0 else "●"
        print(f"\n  r = {r_RX:.2f} R_X ({region}):")
        for L_mode in L_modes:
            print(f"    L = {L_mode}:")
            # 找出该 (r, L_mode) 的粒子索引
            for i_th, th_deg in enumerate(theta_angles_deg):
                th_rad = theta_angles_rad[i_th]
                idx_in_meta = [
                    j for j, (ir, tth, aa, lm) in enumerate(particle_meta)
                    if ir == i_r and abs(tth - th_rad) < 1e-10 and lm == L_mode
                ]
                if idx_in_meta:
                    print(f"      θ = {th_deg}°:")
                    for j in idx_in_meta:
                        traj = trajectories[j]
                        r0_au = traj["r"][0] / AU
                        rf_au = traj["r"][-1] / AU
                        thf = np.rad2deg(np.arccos(
                            np.clip(traj["z"][-1] / max(traj["r"][-1], 1e10), -1, 1)))
                        St0 = stokes_number(traj["a"],
                            gas_density(traj["r"][0], th_rad), Omega_X)
                        a_label = (f"{traj['a']*1e4:.2f}μm" if traj['a'] < 0.01
                                   else (f"{traj['a']*10:.2f}mm" if traj['a'] < 0.1
                                         else f"{traj['a']:.2f}cm"))
                        status = ""
                        if rf_au > 0.5:
                            status = "→ EJECTED"
                        elif rf_au < r0_au * 0.5:
                            status = "→ INFALL"
                        else:
                            dr = rf_au - r0_au
                            status = f"→ Δr={dr*AU/R_X:+.3f} RX"
                        print(
                            f"        {marker} a={a_label:>7s}: St₀={St0:.1e}, "
                            f"r: {r0_au:.4f}→{rf_au:.4f} AU, "
                            f"θf={thf:.1f}° {status}"
                        )

    # ------------------------------------------------------------------
    # Save simulation data for offline re-rendering
    # ------------------------------------------------------------------
    import pickle
    sim_data = {
        "R_X": R_X,
        "R_star": R_star,
        "Omega_X": Omega_X,
        "c_s": c_s,
        "dipole_lines": [(r.copy(), theta.copy()) for r, theta in dipole_lines],
        "flines": [{k: v.copy() if hasattr(v, "copy") else v for k, v in fl.items()}
                    for fl in flines],
        "wind_solutions": [{k: v.copy() if hasattr(v, "copy") else v for k, v in ws.items()}
                           for ws in wind_solutions],
        "trajectories": trajectories,
        "r_values_RX": r_values_RX,
        "theta_angles_deg": theta_angles_deg,
        "a_values": a_values,
        "L_modes": L_modes,
    }
    with open("sim_data.pkl", "wb") as f:
        pickle.dump(sim_data, f, protocol=pickle.HIGHEST_PROTOCOL)
    print("  Simulation data saved to sim_data.pkl")

    # ------------------------------------------------------------------
    # Step 8: Visualization
    # ------------------------------------------------------------------
    print("\n[8/8] Generating visualizations ...")

    # Static plot — 仅背景, 不加粒子轨迹 (避免与动画重叠)
    fig, ax = setup_figure(r_max_AU=0.2)
    plot_background_field(ax, dipole_lines, R_X, bg_open_lines=bg_flines)
    plot_xpoint(ax, R_X)
    plot_open_field_lines(ax, flines, wind_solutions)

    # Legend (粒子)
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#DAA520',
               markersize=8, label='1 μm'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#FF6B35',
               markersize=8, label='100 μm'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#4A90D9',
               markersize=8, label='1 cm'),
        Line2D([0], [0], marker='v', color='w', markerfacecolor='gray',
               markersize=8, label='Inside R_X'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='gray',
               markersize=8, label='Outside R_X'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', frameon=True,
              fontsize=8, ncol=1)

    fig.savefig("xwind_static.png", dpi=150, bbox_inches="tight")
    print("  Static plot saved to xwind_static.png")

    if animate:
        print("  Generating animation ...")
        animator = CAIAnimator(fig, ax, trajectories, dt_frame=dt_output/yr)
        animator.animate("xwind_cai.mp4", fps=20)
    else:
        print("  Skipping animation (--no-anim)")

    print("\n" + "=" * 60)
    print("  Simulation complete.")
    print("=" * 60)


if __name__ == "__main__":
    do_anim = "--no-anim" not in sys.argv
    main(animate=do_anim)
