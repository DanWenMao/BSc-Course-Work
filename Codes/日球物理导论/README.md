# X-Wind Model: CAI Transport Driven by Early Solar Magnetocentrifugal Wind

## 项目简介

本项目数值模拟早期太阳系中 CAI（Calcium-Aluminum-rich Inclusions，钙铝质包体）
在 X-wind 机制作用下的输运过程，对应 Shu et al. (2001, ApJ 548, 1029) 描述的
**阶段 5**——protoCAI 被 X-wind 卷走并输运至外太阳系。

X-wind 理论认为，年轻太阳的强偶极磁场截断原行星盘于 R_X（磁层截断半径），
在 R_X 外侧形成磁离心风（magnetocentrifugal wind），将形成于高温内区的
CAIs 向外输运至数 AU 之外。

---

## 物理模型

### 模型假设

- 年轻太阳具有强偶极磁场（表面 B_* = 3000 G，半径 R_* = 2 R_sun）
- 原行星盘被恒星磁场截断于 R_X，满足 R_X ≈ R_co（共转半径）
- 在 R_X 处存在 X-point，分隔内侧闭合偶极场与外侧 X-wind 开放场
- R_X 外侧开放磁力线锚定于盘面 r_0 ∈ [1.05 R_X, 2.5 R_X]，以 Omega_X 共转
- 气体沿开放磁力线在离心力 + 热压梯度下形成跨声速 X-wind
- 等温物态方程：T = 3000 K，c_s ≈ 3.1 km/s
- CAI 作为无磁化固体颗粒，仅受引力 + Epstein 拖曳力驱动

### 物理链条

```
恒星偶极磁场 → 截断原行星盘于 R_X → X-point
    ↓
R_X 内部：闭合偶极场（星面 → 盘面，r ≤ R_X）
R_X 外部：开放磁力线 r(theta) = r0[sin^2 theta + alpha(pi/2-theta) + cot^2 theta]
    ↓
磁通量管面积 A(s) ∝ 1/B(s) → 共转系有效势 Psi_eff(s)
    ↓
动量方程 → Bernoulli 积分 → 求解跨声速风速度 → 2D 风场插值
    ↓
CAI 颗粒轨道积分（2.5D 柱坐标，含方位角动量）
    ↓
可视化：背景磁场 + 风场 + CAI 轨迹
```

---

## 物理过程详述

### 1. 恒星偶极磁场

球坐标 (r, theta)，偶极轴沿 theta=0（z 轴），盘面在 theta=pi/2：

```
B_r = 2 B_* (R_*/r)^3 cos(theta)
B_theta = B_* (R_*/r)^3 sin(theta)
```

磁力线方程：r(theta) = R_eq sin^2(theta)，R_eq 为赤道面截距。

### 2. X-point（磁层截断半径）

磁压与吸积流 ram pressure 平衡确定截断半径：

```
R_X = k (mu^4 / (G M_* Mdot^2))^(1/7)
```

其中 mu = B_* R_*^3 为磁矩，k = 0.35 为无量纲常数，
Mdot = 2e-9 M_sun/yr 为盘吸积率。

取恒星自转满足共转条件 R_X ≈ R_co：

```
Omega_X = sqrt(G M_* / R_X^3)
R_co = (G M_* / Omega_X^2)^(1/3)
```

**计算值**（默认参数）：R_X ≈ 0.069 AU = 7.5 R_*，Omega_X ≈ 1.7e-5 rad/s（P ≈ 4.2 d）。

### 3. 开放磁力线（X-wind 场几何）

R_X 外侧盘面磁力线向外弯曲并开放至无穷远。采用解析参数化
（Shu et al. 1994, ApJ 429, 781）：

```
r(theta) = r_0 * [sin^2(theta) + alpha*(pi/2 - theta) + cot^2(theta)]
```

- r_0：磁力线足点在赤道面半径（r_0 > R_X）
- alpha ≥ 1：张开参数，保证 dr/dtheta < 0 单调
- 线性项 alpha*(pi/2-theta)：提供盘面附近向外曲率，dr/dtheta|_{theta=pi/2} = -alpha * r_0
- cot^2(theta) 项：确保 theta→0 时 r→∞

开放磁力线特征：
- 风解磁力线：6 条，r_0 ∈ [1.05 R_X, 2.5 R_X]（用于 Bernoulli 风解）
- 背景磁力线：20 条，同上范围（仅几何，用于可视化）
- 足点处气体超开普勒：Omega_X > Omega_K(r_0) → 离心力向外驱动

### 4. 磁通量管与有效势

沿每条开放磁力线计算：
- **磁通量管截面面积**：A(s) ∝ 1/B(s)（磁通量守恒）
- **共转系有效势**：Psi_eff(s) = -GM_*/r(s) - (1/2) Omega_X^2 varpi^2(s)
- **数值导数**：dPsi_eff/ds，d(ln A)/ds（中心差分，用于声速点定位）

### 5. Bernoulli 方程求解稳态风

X-point 外侧的风速度场通过求解等温稳态 Bernoulli 方程得到。
以下给出从动量方程到 Bernoulli 积分的完整推导。

#### 5.1 控制方程

沿磁力线坐标 s（弧长），稳态动量方程为：

```
v dv/ds = -(1/rho) dP/ds - dPsi_eff/ds
```

其中 Psi_eff 为共转系有效势 (§4)。等温物态 P = rho c_s^2 给出：

```
(1/rho) dP/ds = c_s^2 d(ln rho)/ds
```

磁通量管内质量守恒：rho v A = const，取对数微分：

```
d(ln rho)/ds + d(ln v)/ds + d(ln A)/ds = 0
=>  d(ln rho)/ds = -d(ln v)/ds - d(ln A)/ds
```

#### 5.2 推导 Bernoulli 积分

将状态方程和连续性方程代入动量方程：

```
v dv/ds = -c_s^2 [-d(ln v)/ds - d(ln A)/ds] - dPsi_eff/ds
        =  c_s^2 d(ln v)/ds + c_s^2 d(ln A)/ds - dPsi_eff/ds
```

乘以 ds：

```
v dv = c_s^2 d(ln v) + c_s^2 d(ln A) - dPsi_eff
```

逐项积分（c_s 为常数，等温假设）：

```
∫ v dv = c_s^2 ∫ d(ln v) + c_s^2 ∫ d(ln A) - ∫ dPsi_eff
```

得到 **Bernoulli 积分**：

```
(1/2) v^2 - c_s^2 ln v = C + c_s^2 ln A(s) - Psi_eff(s) ≡ F(s)
```

左端为 **Bernoulli 函数** f(v) = (1/2)v^2 - c_s^2 ln v（仅依赖速度），
右端 F(s) 由几何量 A(s) 与势 Psi_eff(s) 沿磁力线完全确定。

#### 5.3 磁场如何控制风——声速点条件

Bernoulli 函数 f(v) = (1/2)v^2 - c_s^2 ln v 的导数 f'(v) = v - c_s^2/v,
在 v = c_s 处为零, f_min = (1/2)c_s^2 - c_s^2 ln c_s。

由于 F(s) 必须 ≥ f_min, 声速点 s_c 满足 F(s_c) = f_min, 等价于:

```
dF/ds|_{s_c} = 0  =>  c_s^2 d(ln A)/ds = dPsi_eff/ds
```

关键一步：由磁通量守恒 A(s) ∝ 1/B(s), 有 d(ln A)/ds = -d(ln B)/ds,
代入正则条件:

```
-c_s^2 d(ln B)/ds = dPsi_eff/ds
```

**这是磁场控制 X-wind 的核心方程。** 左侧为磁通量管几何发散项——
纯由磁场空间分布 B(s) 决定；右侧为有效势梯度——含引力与离心力。
声速点恰好位于磁场几何发散与有效势梯度平衡之处。

磁场的控制通过两个通道进入风动力学:

| 通道 | 物理量 | 进入方式 |
|------|--------|----------|
| 几何约束 (nozzle) | A(s) = 1/B(s) | Bernoulli 积分中 c_s^2 ln A(s) 项; 声速条件中 d(ln A)/ds |
| 离心驱动 | Omega_X | 有效势 Psi_eff 中 -½ Omega_X² varpi²; Omega_X 本身由 R_X 确定, R_X 由 B_* 通过磁层截断公式确定 |

换言之, 恒星表面磁场 B_* 决定了 R_X → 决定了 Omega_X (离心驱动强度),
而偶极场 B(r,theta) 的空间分布决定了沿每条开放磁力线的 A(s) (喷嘴形状)。
二者共同在声速点条件中耦合, 决定风在何处突破声速、最终加速到多大马赫数。

#### 5.4 数值求解流程

1. 沿磁力线计算 A(s) ∝ 1/B(s)，Psi_eff(s)
2. 声速点定位：正则条件残差 |dPsi_eff/ds - c_s^2 d(ln A)/ds| 最小值
   （经 5 点移动平均平滑抑制有限差分噪声）
3. 确定积分常数 C = f_min - c_s^2 ln A(s_c) + Psi_eff(s_c)
4. 逐点计算 F(s) = C + c_s^2 ln A(s) - Psi_eff(s)
5. 求解 f(v) = F(s)：
   - s ≤ s_c：亚声速分支，v ∈ (0, c_s]，Brent 求根 + Newton 回退
   - s > s_c：超声速分支，v ∈ [c_s, ∞)，Brent 求根 + 自适应上界

**典型结果**：声速点位于 s ~ 0.01–0.05 AU，终端马赫数 M ~ 2–5。

### 6. 二维风场构建

将多条磁力线上的 1D Bernoulli 解插值到 2D 球坐标网格（200×100）：

- r 网格：对数均匀，0.5 R_X → 0.5 AU
- theta 网格：线性均匀，theta_min (2°) → pi/2

插值策略：
- 速度模 |v|：Delaunay 三角剖分线性插值（凸包外 NearestND 回退）
- 速度方向：由磁力线切线方向插值得到单位方向矢量
- r < R_X 区域风速强制归零（漏斗流/重联环区无子午面外流）

### 7. 气体密度

采用磁通量管内质量守恒估算：

```
rho(r,theta) = B(r,theta) / |v(r,theta)|
```

归一化至 X-point 处基准密度 rho_base = 2e-10 g/cm^3。
r < R_X 区域为冕气体密度 rho_coronal = 2e-16 g/cm^3（Shu 2001 §2.2 Eq.12）。

### 8. Epstein 拖曳

适用于颗粒半径 a << lambda（分子平均自由程）的 free-molecular 流区：

```
a_drag = (v_w - v) / t_stop
t_stop = (rho_s a) / (rho_g v_th)
```

热运动速度：v_th = sqrt(8 k T / (pi mu m_H))，rho_s = 3.0 g/cm^3（CAI 密度）。

Stokes 数：St = t_stop / t_dyn，t_dyn = 2 pi / Omega_X。

- St << 1（小颗粒）：紧耦合于气体，随风运动
- St >> 1（大颗粒）：脱耦，弹道轨道为主

### 9. CAI 颗粒轨道积分（2.5D）

柱坐标 (varpi, z) 下的运动方程，含方位角动量 L = varpi v_phi：

```
d(varpi)/dt = v_varpi
dz/dt       = v_z
dv_varpi/dt = -GM_*/r^3 varpi + L^2/varpi^3 + (v_{w,varpi} - v_varpi)/t_stop
dv_z/dt     = -GM_*/r^3 z     + (v_{w,z} - v_z)/t_stop
dL/dt       = varpi (v_{w,phi} - v_phi)/t_stop

其中 v_{w,phi} = Omega_X varpi（等转动定理：风沿磁力线以恒定 Omega_X 共转）
```

积分器：scipy.integrate.solve_ivp，LSODA 方法（自动刚性/非刚性切换），
rtol=1e-6，atol=1e-8，max_step = t_end/500。
终止事件：撞星（r ≤ R_*）或逃逸（r ≥ 10 AU）。

#### 初始条件

| 物理量 | 设定 |
|--------|------|
| r/R_X | [0.85, 0.95, 1.05, 1.20] |
| theta | [75°, 85°]（盘面上方） |
| 粒径 a | [1 um, 100 um, 1 cm] |
| 角动量模式 | 开普勒 L = varpi v_K |
| v_z 初值 | 0.005 v_K（向上扰动） |

覆盖 R_X 内外，表征重联环（r < R_X）和风区（r > R_X）初始位置的影响。

积分总时长：t_end = 0.2 yr，输出间隔 dt = 0.001 yr（≈ 8.8 h）。

### 10. 可视化

半平面（varpi ≥ 0，z ≥ 0），四层叠加：

1. **内部闭合偶极场**（灰色）：12 条磁力线，从星面 (r=R_*) → 盘面 (r ≤ R_X)。
   最外层终止于 X-point (R_X, 0)。

2. **外部 X-wind 开放场**（灰色背景）：20 条参数形式开放磁力线，
   r_0 ∈ [1.05 R_X, 2.5 R_X]，显示开放场几何。

3. **风场解**（彩色）：6 条，亚声速段蓝色 → 超声速段紫红，声速点绿色标记。

4. **CAI 轨迹**（彩色标记）：金/橙/蓝区分粒径，▼/● 区分 R_X 内外。

输出：PNG 静态图 + MP4 动画（200 帧 @ 20 fps）。

---

## 代码框架

```
xwind_v4/
├── README.md              本文件
├── CHANGELOG.md            版本修改记录
├── constants.py            物理常数与模型参数
├── dipole_field.py         恒星偶极磁场（含截断工具）
├── xpoint.py               X-point 计算（R_X, Omega_X, R_co）
├── open_field_lines.py     开放磁力线（参数形式）
├── flux_tube.py            磁通量管截面与有效势
├── bernoulli.py            Bernoulli 方程求解跨声速风
├── wind_field.py           1D→2D 风场插值
├── drag.py                 Epstein 拖曳（含 Stokes 数）
├── cai_dynamics.py         CAI 轨道积分（2.5D 柱坐标）
├── visualization.py        可视化（背景场 + 风场 + CAI 动画）
├── render_animation.py     离线动画渲染（从 sim_data.pkl）
└── main.py                 主流程
```

## 运行

```bash
python3 main.py              # 完整模拟 + 动画
python3 main.py --no-anim    # 仅计算 + 静态图
python3 render_animation.py  # 从已有 sim_data.pkl 离线渲染
```

## 参考

- Shu et al. (1994), ApJ 429, 781 — X-wind 磁离心风理论
- Shu et al. (1996), Science 271, 1545 — X-wind 与陨石证据
- Shu et al. (2001), ApJ 548, 1029 — CAI 形成六阶段模型
