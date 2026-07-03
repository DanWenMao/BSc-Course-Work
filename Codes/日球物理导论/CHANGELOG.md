# Changelog — v4 (from v3)

## 2026-06-16: Dipole field lines from star surface → X-point

**Problem**: `plot_dipole_background()` drew pure dipole field lines everywhere in gray,
inconsistent with the X-wind model's two-zone field geometry.

**Iteration 1**: Truncated dipole at R_X — lines looked like "dipole fragments" hanging
mid-air, not clearly connecting star to magnetospheric boundary.

**Iteration 2**: Added X-wind open field lines in gray as background. But dipole lines
still terminated on the R_X dashed arc (at various heights), not on the disk.

**Iteration 3 (final)**: 
- Dipole lines now generated with R_eq ∈ [1.2 R_star, R_X]
  (previously 0.3 R_star → 3.0 AU, all >> R_X)
- Each line terminates naturally at the disk midplane (z=0) at its R_eq ≤ R_X
- Outermost line terminates exactly at X-point (R_X, 0)
- Star-side truncated at R_star for clean star surface attachment

**Visual result**: 
  Inside R_X: 12 closed dipole lines fanning from star surface → disk midplane
  At R_X: outermost closed line terminates at X-point (disk truncation)
  Outside R_X: 20 gray X-wind open field lines + 6 colored wind-solution lines

## Files modified
- `dipole_field.py` — `truncate_dipole_line(r, theta, r_outer, r_inner=None)` 
- `visualization.py` — new `plot_background_field()`: closed dipole + open bg lines
- `main.py` — dipole lines generated with R_eq ∈ [R_star, R_X]; bg_flines (20 lines)
- `render_animation.py` — generates bg_flines from pickle R_X
