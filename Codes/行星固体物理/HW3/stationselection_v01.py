import numpy as np
import matplotlib.pyplot as plt

from obspy.clients.fdsn import Client
from obspy import UTCDateTime
from obspy.geodetics import locations2degrees

import cartopy.crs as ccrs
import cartopy.feature as cfeature

# ===============================
# 1. 震源参数（汶川地震）
# ===============================
evla = 31.0
evlo = 103.4
evdp = 19  # km
origin_time = UTCDateTime("2008-05-12T06:28:00")

# ===============================
# 2. 获取台站（30–90°）
# ===============================
client = Client("IRIS")

inventory = client.get_stations(
    latitude=evla,
    longitude=evlo,
    minradius=30,
    maxradius=90,
    starttime=origin_time,
    endtime=origin_time + 3600,
    channel="BH?",
    level="station"
)

print("Total stations found:", len(inventory.get_contents()["stations"]))

# ===============================
# 3. 提取台站信息
# ===============================
stations = []

for net in inventory:
    for sta in net:
        dist = locations2degrees(evla, evlo, sta.latitude, sta.longitude)
        stations.append({
            "network": net.code,
            "station": sta.code,
            "lat": sta.latitude,
            "lon": sta.longitude,
            "dist": dist
        })

# ===============================
# 4. 按震中距排序
# ===============================
stations = sorted(stations, key=lambda x: x["dist"])

# ===============================
# 5. 自动“均匀选台站”（核心算法）
# ===============================
def select_uniform_stations(stations, n=25):
    distances = np.array([s["dist"] for s in stations])
    target = np.linspace(30, 90, n)

    selected = []
    used = set()

    for t in target:
        idx = np.argmin(np.abs(distances - t))
        while idx in used:
            idx += 1
            if idx >= len(stations):
                break
        if idx < len(stations):
            selected.append(stations[idx])
            used.add(idx)

    return selected

selected_stations = select_uniform_stations(stations, n=25)

print("\nSelected stations:")
for s in selected_stations:
    print(s["network"], s["station"], f"{s['dist']:.1f}°")

# ===============================
# 6. 画地图
# ===============================
fig = plt.figure(figsize=(12, 6))
ax = plt.axes(projection=ccrs.PlateCarree())

ax.set_global()
ax.coastlines()
ax.add_feature(cfeature.BORDERS, linewidth=0.5)
ax.add_feature(cfeature.LAND, alpha=0.3)
ax.add_feature(cfeature.OCEAN, alpha=0.3)

# --- 所有台站（灰色）
lats_all = [s["lat"] for s in stations]
lons_all = [s["lon"] for s in stations]
ax.scatter(lons_all, lats_all, s=10, color='gray', label="All stations")

# --- 选中的台站（三角形）
lats_sel = [s["lat"] for s in selected_stations]
lons_sel = [s["lon"] for s in selected_stations]
ax.scatter(lons_sel, lats_sel, marker='^', s=80, color='blue', label="Selected")

# --- 震源（红色五角星）
ax.scatter(evlo, evla, marker='*', s=200, color='red', label="Event")

# --- 标注台站名（可选）
for s in selected_stations:
    ax.text(s["lon"]+2, s["lat"]+2, s["station"], fontsize=8)

ax.legend()
ax.set_title("Station Distribution (30°–90°) - Wenchuan Earthquake")

plt.show()