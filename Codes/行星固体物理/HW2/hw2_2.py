import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def fault_stress(tao11, tao12, tao22, theta):
    '''
    theta: fault strike angle
    '''
    theta_rad = np.radians(theta)
    
    # Calculate the normal and shear stress on the fault plane
    tau_n = tao11 * np.cos(theta_rad)**2 - 2 * tao12 * np.cos(theta_rad) * np.sin(theta_rad) + tao22 * np.sin(theta_rad)**2
    tau_s = (- tao22 + tao11) * np.cos(theta_rad) * np.sin(theta_rad) + tao12 * (np.cos(theta_rad)**2 - np.sin(theta_rad)**2)
    
    return tau_n, tau_s

def CFF(tau_n, tau_s, mu):
    # Calculate the Coulomb Failure Function
    return np.abs(tau_s) + mu * tau_n

atheta = np.arange(0, 171, 10)  # Fault plane angles from 0 to 180 degrees
[t11_e, t12_e, t22_e] = [3.294, -45.6435, 81.351] # Earthquake stress components, kPa
[t11_y, t12_y, t22_y] = [9.1962, 0.33075, 1.19205] # Yearly stress components, kPa
[t11_1000, t12_1000, t22_1000] = [9.1962*1000, 0.33075*1000, 1.19205*1000] # 1000-year stress components, kPa
[t11_1000_e, t12_1000_e, t22_1000_e] = [t11_1000+t11_e, t12_1000+t12_e, t22_1000+t22_e] # 100₀-year + earthquake stress components, kPa

tau_n_e, tau_s_e = fault_stress(t11_e, t12_e, t22_e, atheta)
tau_n_y, tau_s_y = fault_stress(t11_y, t12_y, t22_y, atheta)
tau_n_1000, tau_s_1000 = fault_stress(t11_1000, t12_1000, t22_1000, atheta)
tau_n_1000_e, tau_s_1000_e = fault_stress(t11_1000_e, t12_1000_e, t22_1000_e, atheta)

CFF_e = CFF(tau_n_e, tau_s_e, 0.2)
CFF_y = CFF(tau_n_y, tau_s_y, 0.2)
CFF_1000 = CFF(tau_n_1000, tau_s_1000, 0.2)
CFF_1000_e = CFF(tau_n_1000_e, tau_s_1000_e, 0.2)

delta_t = (CFF_1000_e - CFF_1000) / CFF_y
# ===============================
# (f)(g)(h) 生成数据表
# ===============================

table = pd.DataFrame({

    "Fault Strike (deg)": atheta,

    "Shear stress Landers (kPa)": tau_s_e,
    "Normal stress Landers (kPa)": tau_n_e,

    "Shear stress yearly (kPa)": tau_s_y,
    "Normal stress yearly (kPa)": tau_n_y,

    "CFF_a (kPa/year)": CFF_y,

    "CFF_1000 (kPa)": CFF_1000,
    "CFF_1000+Landers (kPa)": CFF_1000_e,

    "Delta t (yr)": delta_t

})

table.to_csv("fault_CFF_results.csv", index=False)

# ===============================
# (f) 最大剪应力方向
# ===============================

max_shear_EQ_angle = atheta[np.argmax(np.abs(tau_s_e))]
max_shear_year_angle = atheta[np.argmax(np.abs(tau_s_y))]

print("\nMaximum shear stress orientation:")
print("Earthquake:", max_shear_EQ_angle,"deg")
print("Yearly loading:", max_shear_year_angle,"deg")


# ===============================
# 可视化 1：剪应力
# ===============================

plt.figure()

plt.plot(atheta, tau_s_e, marker="o", label="Shear stress (Earthquake)")
plt.plot(atheta, tau_s_y, marker="s", label="Shear stress (Yearly)")

plt.xlabel("Fault strike (deg)")
plt.ylabel("Shear stress (kPa)")
plt.title("Shear stress vs fault orientation")
plt.xticks(np.arange(0, 180, 10))
plt.legend()
plt.grid()

plt.savefig("2_shear_stress.png")


plt.figure()

plt.plot(atheta, tau_n_e, marker="o", label="Normal stress (Earthquake)")
plt.plot(atheta, tau_n_y, marker="s", label="Normal stress (Yearly)")

plt.xlabel("Fault strike (deg)")
plt.ylabel("Normal stress (kPa)")
plt.title("Normal stress vs fault orientation")
plt.xticks(np.arange(0, 180, 10))
plt.legend()
plt.grid()

plt.savefig("2_normal_stress.png")


# ===============================
# 可视化 2：CFF yearly
# ===============================

plt.figure()

plt.plot(atheta, CFF_y, marker="o", label="CFF yearly")
plt.plot(atheta, CFF_e, marker="s", label="CFF Earthquake")

plt.xlabel("Fault strike (deg)")
plt.ylabel("CFF")
plt.title("Coulomb Failure Function")
plt.xticks(np.arange(0, 180, 10))
plt.grid()

plt.savefig("2_CFF.png")


# ===============================
# 可视化 3：地震时间变化
# ===============================

plt.figure()

plt.bar(atheta, delta_t)

plt.xlabel("Fault strike (deg)")
plt.ylabel("Earthquake time change (years)")
plt.title("Advancement / Delay of next earthquake")
plt.xticks(np.arange(0, 180, 10))
plt.axhline(0)

plt.savefig("2_delta_t.png")
# ===============================
# (i) 自动判断
# ===============================

advance = np.sum(delta_t > 0)
delay = np.sum(delta_t < 0)

print("\nNumber of orientations advancing failure:", advance)
print("Number of orientations delaying failure:", delay)