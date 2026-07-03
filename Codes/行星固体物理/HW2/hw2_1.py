import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def fault_stress(theta):
    theta_rad = np.radians(theta)
    
    # Calculate the normal and shear stress on the fault plane
    tau_n = -40-20*np.sin(theta_rad)*np.cos(theta_rad)-20*np.cos(theta_rad)**2
    tau_s = 20*np.sin(theta_rad)*np.cos(theta_rad)+10*(np.sin(theta_rad)**2-np.cos(theta_rad)**2)
    
    return tau_n, tau_s

atheta = np.arange(0, 360, 5)
tau_n, tau_s = fault_stress(atheta)


# ===============================
# 可视化 1：剪应力
# ===============================

plt.figure()

plt.plot(atheta, tau_s, marker="o", label="Shear stress")

plt.xlabel("Fault strike (deg)")
plt.ylabel("Shear stress (kPa)")
plt.xticks(np.arange(0, 360, 30))
plt.legend()
plt.grid()

plt.savefig("1_shear_stress.png")


plt.figure()

plt.plot(atheta, tau_n, marker="o", label="Normal stress")

plt.xlabel("Fault strike (deg)")
plt.ylabel("Normal stress (kPa)")
plt.title("Normal stress vs fault orientation")
plt.xticks(np.arange(0, 360, 30))
plt.legend()
plt.grid()

plt.savefig("1_normal_stress.png")