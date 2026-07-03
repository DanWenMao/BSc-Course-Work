"""
visualization.py — 可视化

半平面 (ϖ≥0, z≥0) 展示:
  1. 背景磁场 — 内部截断偶极 + 外部 X-wind 开放磁力线 (灰色, 与模型一致)
  2. X-point 位置 (红色虚线)
  3. 开放磁场线与稳态 X-wind (亚/超声速分色, 声速点标记)
  4. CAI 颗粒轨迹 (颜色区分粒径, 形状区分内外 R_X)

输出: PNG 静态图 / MP4 动画
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from matplotlib.lines import Line2D
from constants import R_star, AU

# 颜色方案 (科学论文风格)
COLOR_1UM = "#DAA520"      # gold — 1 μm
COLOR_100UM = "#FF6B35"    # orange — 100 μm
COLOR_1CM = "#4A90D9"      # blue — 1 cm
COLOR_SUN = "#F5A623"
COLOR_DIPOLE = "#B0B0B0"
COLOR_SUBSONIC = "#2E86AB"
COLOR_SUPERSONIC = "#A23B72"
COLOR_SONIC = "#2ECC71"
COLOR_XPOINT = "#E74C3C"
COLOR_DISK = "#999999"


def _size_color(a_cm):
    """根据粒径返回颜色。"""
    if a_cm < 5e-4:
        return COLOR_1UM
    elif a_cm < 0.05:
        return COLOR_100UM
    else:
        return COLOR_1CM


def _size_label(a_cm):
    """根据粒径返回标签。"""
    if a_cm < 5e-4:
        return "1 μm"
    elif a_cm < 0.05:
        return "100 μm"
    else:
        return "1 cm"


def setup_figure(r_max_AU=0.20):
    """
    设置半平面 (ϖ≥0) 图窗。

    参数
    ----
    r_max_AU : float
        图的最大半径 (AU)

    返回
    ----
    fig, ax
    """
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 11,
        "axes.labelsize": 12,
        "axes.titlesize": 13,
        "legend.fontsize": 9,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
    })

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect("equal")
    r_max = r_max_AU * AU
    ax.set_xlim(0, r_max)
    ax.set_ylim(0, r_max)
    ax.set_xlabel(r"$\varpi$ (AU)")
    ax.set_ylabel(r"$z$ (AU)")

    # 刻度用 AU
    ax.xaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f"{x / AU:.2f}")
    )
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda y, _: f"{y / AU:.2f}")
    )

    # 画恒星 (半圆)
    star = Circle((0, 0), R_star, color=COLOR_SUN, ec="darkorange",
                  lw=0.8, zorder=10)
    ax.add_patch(star)
    ax.text(R_star * 1.2, -R_star * 0.3, "Star", ha="left",
            fontsize=9, color=COLOR_SUN, style="italic")

    # 盘面线 (z=0)
    ax.axhline(0, color=COLOR_DISK, ls="--", lw=0.6, alpha=0.6)
    # ϖ 轴标签
    ax.text(r_max * 0.5, -r_max * 0.06, "Disk midplane",
            ha="center", fontsize=8, color=COLOR_DISK, style="italic")

    return fig, ax


def plot_background_field(ax, dipole_lines, R_X, bg_open_lines=None):
    """绘制与模型物理一致的背景磁场。

    内部 (r < R_X): 偶极闭合磁力线 (灰色, 截断于磁层边界)
    外部 (r > R_X): X-wind 开放磁力线 (灰色, 参数形式 r=r₀[sin²θ+α(π/2-θ)+cot²θ])

    参数
    ----
    ax : matplotlib Axes
    dipole_lines : list of (r, theta) 元组
        偶极磁力线 (会在 R_X 处截断)
    R_X : float
        磁层截断半径 (cm)
    bg_open_lines : list of dict, 可选
        背景开放磁力线, 每项含 {'r': array, 'theta': array}
        若无则只显示内部偶极场
    """
    from dipole_field import truncate_dipole_line

    # --- 内部偶极场 (截断于 [R_star, R_X]: 星面→磁层边界) ---
    for r, theta in dipole_lines:
        r_plot, theta_plot = truncate_dipole_line(r, theta, R_X, R_star)
        if len(r_plot) == 0:
            continue
        varpi = r_plot * np.sin(theta_plot)
        z = r_plot * np.cos(theta_plot)
        ax.plot(varpi, z, color=COLOR_DIPOLE, lw=0.3, alpha=0.35)

    # --- 外部开放磁力线 (X-wind 几何) ---
    if bg_open_lines is not None:
        for fl in bg_open_lines:
            varpi = fl["r"] * np.sin(fl["theta"])
            z = fl["r"] * np.cos(fl["theta"])
            ax.plot(varpi, z, color=COLOR_DIPOLE, lw=0.3, alpha=0.35)


# Backward compatibility
def plot_dipole_background(ax, dipole_lines, R_X=None):
    """已弃用: 请使用 plot_background_field() 以匹配模型磁场几何。"""
    plot_background_field(ax, dipole_lines, R_X)


def plot_xpoint(ax, R_X):
    """绘制 X-point 位置与 R_X 圆。"""
    # R_X 圆弧
    theta_ring = np.linspace(0, np.pi / 2, 50)
    ax.plot(R_X * np.sin(theta_ring), R_X * np.cos(theta_ring),
            color=COLOR_XPOINT, ls="--", lw=0.8, alpha=0.6)
    # X-point 标记
    ax.plot(R_X, 0, "x", color=COLOR_XPOINT, markersize=8, mew=1.5,
            zorder=20)
    ax.text(R_X * 0.95, R_X * 0.12, r"$R_X$", ha="right",
            fontsize=9, color=COLOR_XPOINT)


def plot_open_field_lines(ax, field_lines, wind_solutions):
    """
    绘制开放磁力线 (仅上半平面)。
    亚声速段蓝色, 超声速段紫红, 声速点绿色。
    """
    for fl, ws in zip(field_lines, wind_solutions):
        r = fl["r"]
        theta = fl["theta"]
        v = ws["v"]
        sonic_idx = ws["sonic_idx"]
        varpi = r * np.sin(theta)
        z = r * np.cos(theta)

        # 亚声速段
        ax.plot(varpi[: sonic_idx + 1], z[: sonic_idx + 1],
                color=COLOR_SUBSONIC, lw=1.8, alpha=0.85)
        # 超声速段
        ax.plot(varpi[sonic_idx:], z[sonic_idx:],
                color=COLOR_SUPERSONIC, lw=1.8, alpha=0.85)
        # 声速点
        ax.plot(varpi[sonic_idx], z[sonic_idx], "o",
                color=COLOR_SONIC, ms=5, zorder=15, markeredgecolor="white",
                markeredgewidth=0.5)

    # 图例
    legend_elements = [
        Line2D([0], [0], color=COLOR_SUBSONIC, lw=2,
               label="Subsonic ($v < c_s$)"),
        Line2D([0], [0], color=COLOR_SUPERSONIC, lw=2,
               label="Supersonic ($v > c_s$)"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=COLOR_SONIC,
               markersize=7, label="Sonic point"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", frameon=True,
              fontsize=8, ncol=1)


class CAIAnimator:
    """CAI 颗粒轨迹动画 (半平面, 论文风格)。"""

    def __init__(self, fig, ax, trajectories, dt_frame=0.02):
        """
        参数
        ----
        fig, ax : matplotlib 对象
        trajectories : list of dict
        dt_frame : float
            每帧时间间隔 (yr)
        """
        self.fig = fig
        self.ax = ax
        self.dt_frame_yr = dt_frame
        self.dt_frame = dt_frame * 365.25 * 86400

        self.traj = trajectories
        self.n_particles = len(trajectories)
        self.t_max = max(t["t"][-1] for t in trajectories)

        # 按粒径着色
        a_values = [t["a"] for t in trajectories]
        self.colors = [_size_color(a) for a in a_values]

        # 每个粒子独立 plot 标记 (稳健 blit, 支持不同形状)
        self.markers = []
        for i, t in enumerate(trajectories):
            marker = "v" if t.get("inside", False) else "o"
            (m,) = ax.plot([], [], marker=marker, ms=8, color=self.colors[i],
                          zorder=30)
            self.markers.append(m)

        # 轨迹尾迹
        self.trail_lines = []
        for i in range(self.n_particles):
            (line,) = ax.plot([], [], lw=0.7, alpha=0.4,
                             color=self.colors[i])
            self.trail_lines.append(line)

        # 时间文本
        self.time_text = ax.text(
            0.02, 0.98, "", transform=ax.transAxes, fontsize=11,
            va="top", fontfamily="monospace"
        )

    def _get_state_at_time(self, traj, t):
        """在时间 t 获取轨迹状态。"""
        idx = np.searchsorted(traj["t"], t)
        if idx >= len(traj["t"]):
            return None
        if idx == 0:
            return (traj["varpi"][0], traj["z"][0])
        return (traj["varpi"][idx], traj["z"][idx])

    def init_anim(self):
        for m in self.markers:
            m.set_data([], [])
        for line in self.trail_lines:
            line.set_data([], [])
        self.time_text.set_text("")
        return [*self.markers, self.time_text, *self.trail_lines]

    def update(self, frame):
        t = frame * self.dt_frame
        t_yr = t / (365.25 * 86400)

        for i, traj in enumerate(self.traj):
            result = self._get_state_at_time(traj, t)
            if result is None:
                varpi, z = traj["varpi"][-1], traj["z"][-1]
                self.markers[i].set_data([varpi], [z])
                self.markers[i].set_color("#cccccc")
            else:
                varpi, z = result
                self.markers[i].set_data([varpi], [z])
                self.markers[i].set_color(self.colors[i])

        # 轨迹尾迹
        trail_len = 50
        for i, traj in enumerate(self.traj):
            idx = np.searchsorted(traj["t"], t)
            start = max(0, idx - trail_len)
            self.trail_lines[i].set_data(
                traj["varpi"][start: idx + 1],
                traj["z"][start: idx + 1]
            )

        self.time_text.set_text(f"t = {t_yr:.2f} yr")

        return [*self.markers, self.time_text, *self.trail_lines]

    def animate(self, filename="xwind_cai.mp4", fps=15):
        n_frames = int(self.t_max / self.dt_frame) + 1
        anim = FuncAnimation(
            self.fig,
            self.update,
            frames=min(n_frames, 400),
            init_func=self.init_anim,
            blit=True,
            interval=1000 / fps,
        )
        anim.save(filename, fps=fps, dpi=150, writer="ffmpeg")
        plt.close(self.fig)
        print(f"  Animation saved to {filename}")
        return anim
