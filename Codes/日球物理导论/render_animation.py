#!/usr/bin/env python3
"""
render_animation.py — 从 sim_data.pkl 离线渲染动画

无需重新运行模拟即可调整可视化参数：
  - 显示范围 (r_max_AU)
  - 帧率 (fps)
  - 动画时长
  - 输出文件名

用法:
  python3 render_animation.py                          # 默认参数
  python3 render_animation.py --r-max 0.5 --fps 20     # 放大到 0.5 AU
  python3 render_animation.py --r-max 0.15 --dt 0.005  # 聚焦 CAI 区域
"""

import sys
import pickle
import numpy as np
from constants import AU, R_star

from visualization import (
    setup_figure,
    plot_background_field,
    plot_xpoint,
    plot_open_field_lines,
    CAIAnimator,
)
from open_field_lines import open_field_lines


def load_data(filename="sim_data.pkl"):
    """加载模拟数据。"""
    with open(filename, "rb") as f:
        return pickle.load(f)


def main():
    # 解析命令行参数
    r_max_AU = 0.2
    fps = 15
    dt_frame_yr = 0.01
    filename = "xwind_cai.mp4"

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--r-max" and i + 1 < len(args):
            r_max_AU = float(args[i + 1])
            i += 2
        elif args[i] == "--fps" and i + 1 < len(args):
            fps = int(args[i + 1])
            i += 2
        elif args[i] == "--dt" and i + 1 < len(args):
            dt_frame_yr = float(args[i + 1])
            i += 2
        elif args[i] == "--output" and i + 1 < len(args):
            filename = args[i + 1]
            i += 2
        else:
            i += 1

    print(f"Loading sim_data.pkl ...")
    data = load_data()
    print(f"  R_X        = {data['R_X']/AU:.4f} AU")
    print(f"  c_s        = {data['c_s']/1e5:.2f} km/s")
    print(f"  Particles  = {len(data['trajectories'])}")
    for traj in data["trajectories"]:
        print(
            f"    a={traj['a']*10:.2f} mm: "
            f"r₀={traj['r'][0]/AU:.4f} → r_f={traj['r'][-1]/AU:.4f} AU"
        )
    print(f"\nRendering animation:")
    print(f"  Display range = ±{r_max_AU:.2f} AU")
    print(f"  Frame dt      = {dt_frame_yr:.2f} yr")
    print(f"  FPS           = {fps}")
    print(f"  Output        = {filename}")

    # 构建静态背景
    fig, ax = setup_figure(r_max_AU=r_max_AU)

    # 生成背景开放磁力线 (仅几何, 无风解)
    bg_flines = open_field_lines(data["R_X"], n_lines=20, alpha=1.0)

    plot_background_field(ax, data["dipole_lines"], data["R_X"],
                          bg_open_lines=bg_flines)
    plot_xpoint(ax, data["R_X"])
    plot_open_field_lines(ax, data["flines"], data["wind_solutions"])

    # 动画
    animator = CAIAnimator(fig, ax, data["trajectories"], dt_frame=dt_frame_yr)
    anim = animator.animate(filename=filename, fps=fps)
    print(f"\nDone. Animation saved to {filename}")


if __name__ == "__main__":
    main()
