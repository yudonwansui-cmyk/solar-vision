import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# --- 1. 可配置参数 ---
CSV_FILE_PATH = 'receiver_flux_map.csv'

# 从你的C++代码中获取这些值
RECEIVER_HEIGHT_M = 8.0
RECEIVER_BASE_Z_M = 76.0
GRID_WIDTH = 256  # C++中设置的角度方向分辨率
GRID_HEIGHT = 512 # C++中设置的高度方向分辨率

# 可视化参数
FIG_TITLE = '接收器能量密度分布光斑图 (3月21日 12:00 - 全场)'
COLOR_MAP = 'jet'
SMOOTHING_SIGMA = 1.2 # 推荐值 1.0-2.0
VMIN = 0
VMAX = 400

# --- 2. 加载和重塑数据 ---
try:
    print(f"正在加载数据: {CSV_FILE_PATH}...")
    df = pd.read_csv(CSV_FILE_PATH)
    flux_data = df['Flux_Density(W/m^2)'].values.reshape((GRID_HEIGHT, GRID_WIDTH))
    print("数据加载并重塑成功。")
except Exception as e:
    print(f"错误: 无法加载或重塑数据。请检查文件路径和网格尺寸配置。")
    print(f"具体错误: {e}")
    exit()

# --- 3. 数据处理 ---
# 应用高斯平滑
#if SMOOTHING_SIGMA > 0:
    print(f"应用高斯平滑 (sigma={SMOOTHING_SIGMA})...")
    flux_data_processed = gaussian_filter(flux_data, sigma=SMOOTHING_SIGMA)
#else:
flux_data_processed = flux_data

# --- 4. 绘图 ---

print("开始绘图...")
fig, ax = plt.subplots(figsize=(16, 9))

# 使用imshow绘制热力图
# extent 定义了图像四个角的物理坐标 [left, right, bottom, top]
im = ax.imshow(
    flux_data_processed,
    aspect='auto',
    cmap=COLOR_MAP,
    extent=[-180, 180, RECEIVER_BASE_Z_M, RECEIVER_BASE_Z_M + RECEIVER_HEIGHT_M],
    origin='lower',
    interpolation='bicubic',
    vmin=VMIN,
    vmax=VMAX
)

# 设置坐标轴和标题
ax.set_title(FIG_TITLE, fontsize=18, fontproperties="SimHei")
ax.set_xlabel('方位角 (度) - 正北为0° / 正南为±180°', fontsize=14, fontproperties="SimHei")
ax.set_ylabel('接收器高度 (m)', fontsize=14, fontproperties="SimHei")

# 设置坐标轴刻度
ax.set_xticks(np.arange(-180, 181, 30))
ax.grid(True, linestyle='--', linewidth=0.5, color='white', alpha=0.7)

# 添加颜色条
cbar = fig.colorbar(im, ax=ax)
cbar.set_label('能量密度 (W/m2)', fontsize=14, fontproperties="SimHei")

# 设置整体外观
fig.patch.set_facecolor('#E6F0FF')
ax.set_facecolor('#E6F0FF')

plt.tight_layout()
print("绘图完成，正在显示图像...")
plt.show()