import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager


def plot_receiver_flux_map(csv_file, receiver_base_z, receiver_height):
    """
    读取CUDA仿真生成的接收器能流密度数据并绘制热力图。

    Args:
        csv_file (str): 包含能流密度数据的CSV文件名。
        receiver_base_z (float): 接收器底部的高度 (m)。
        receiver_height (float): 接收器的高度 (m)。
    """
    # --- 1. 设置绘图环境 (支持中文) ---
    # 指定一个支持中文的字体，例如 'SimHei' (黑体) 或 'Microsoft YaHei' (微软雅黑)
    # 如果系统没有这些字体，请替换为可用的中文字体路径
    try:
        plt.rcParams['font.sans-serif'] = ['SimHei']
    except:
        print("警告：未找到'SimHei'字体，中文可能显示为方块。请安装或指定其他中文字体。")
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    plt.style.use('default')  # 使用默认样式

    # --- 2. 加载和处理数据 ---
    print(f"正在读取数据文件: {csv_file}...")
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"错误：找不到文件 '{csv_file}'。请确保CUDA程序已成功运行并生成该文件。")
        return

    # 将数据透视为二维网格
    # index对应Y轴, columns对应X轴
    flux_data = df.pivot(index='Z_Index', columns='Theta_Index', values='Flux_Density(W/m^2)')

    # 转换为Numpy数组，并处理可能存在的NaN值
    flux_grid = flux_data.to_numpy()
    flux_grid = np.nan_to_num(flux_grid, nan=0.0)

    # 获取网格维度
    grid_h, grid_w = flux_grid.shape
    print(f"数据加载成功，网格维度: {grid_w}(角度) x {grid_h}(高度)")

    # --- 3. 绘图 ---
    fig, ax = plt.subplots(figsize=(12, 8), facecolor='#d6e8ff')  # 设置画布尺寸和背景色
    ax.set_facecolor('#d6e8ff')  # 设置绘图区背景色

    # 使用imshow绘制热力图
    # extent参数定义了图像的坐标范围: [x_min, x_max, y_min, y_max]
    # x轴: 方位角从 -180 (南) -> -90 (西) -> 0 (北) -> 90 (东) -> 180 (南)
    # y轴: 接收器物理高度
    # origin='lower' 表示 (0,0) 索引在左下角，这与我们的Z_Index=0在底部相匹配
    im = ax.imshow(
        flux_grid,
        cmap='jet',  # 使用'jet'色彩映射，与示例图类似
        extent=[-180, 180, receiver_base_z, receiver_base_z + receiver_height],
        interpolation='bicubic',  # 使用双三次插值使图像更平滑
        aspect='auto'
    )

    # --- 4. 设置坐标轴、标题和颜色条 ---
    ax.set_title("接收器能量密度分布光斑图 (3月21日 12:00 - 全场)", fontsize=16, pad=20)
    ax.set_xlabel("方位角（度）- 正南为-180°/180°，正北为 0°", fontsize=12)
    ax.set_ylabel("接收器高度（m）", fontsize=12)

    # 设置Y轴刻度
    ax.set_yticks(np.arange(int(receiver_base_z), int(receiver_base_z + receiver_height) + 1, 1.0))
    # 设置X轴刻度
    ax.set_xticks(np.arange(-180, 181, 30))

    # 添加颜色条
    cbar = fig.colorbar(im, ax=ax, pad=0.02)
    cbar.set_label("能量密度 (W/m²)", fontsize=12)

    # 添加网格线
    ax.grid(True, linestyle='--', color='white', alpha=0.5)

    # --- 5. 显示和保存图像 ---
    plt.tight_layout()
    output_filename = "receiver_flux_map.png"
    plt.savefig(output_filename, dpi=300, facecolor=fig.get_facecolor())
    print(f"绘图完成，已保存为 '{output_filename}'")
    plt.show()


if __name__ == '__main__':
    # --- 配置参数 (必须与 main.cu 中的 SimConfig 保持一致!) ---
    # 从您的main.cu文件中获取这些值
    RECEIVER_BASE_Z = 76.0
    RECEIVER_HEIGHT = 8.0
    CSV_FILENAME = "receiver_flux_map.csv"

    plot_receiver_flux_map(CSV_FILENAME, RECEIVER_BASE_Z, RECEIVER_HEIGHT)