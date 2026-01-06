## `plot_heatmap.py` (针对 `heliostat_1000_shading_map.csv`)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl


def plot_heatmap(csv_file_path, heliostat_id):
    """
    从CSV文件加载数据并绘制高清热力图。
    """
    # 1. 使用 Pandas 加载数据
    print(f"Loading data from {csv_file_path}...")
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {csv_file_path}")
        print("Please make sure the CSV file is in the same directory as the script.")
        return  # 如果文件不存在则退出

    # 2. 将数据转换为 2D Numpy 数组（矩阵）
    # 检查数据是否完整
    if 'X_Index' not in df.columns or 'Y_Index' not in df.columns or 'Shading_Efficiency' not in df.columns:
        print("Error: CSV file must contain 'X_Index', 'Y_Index', and 'Shading_Efficiency' columns.")
        return

    # 使用 pivot 方法将长格式数据转换为宽格式（矩阵）
    try:
        heatmap_data = df.pivot(index='Y_Index', columns='X_Index', values='Shading_Efficiency').values
    except Exception as e:
        print(f"Error processing data into a matrix. Is the data for a full grid? Error: {e}")
        return

    # 获取矩阵维度
    side_length_y, side_length_x = heatmap_data.shape

    # =======================================================================
    # 优化后的高清绘图方式
    # =======================================================================
    # a) 设置画布和DPI
    fig, ax = plt.subplots(figsize=(10, 8))

    # b) 使用 imshow 绘图, 关键参数:
    #    interpolation='none': 禁止颜色插值，让每个像素块都棱角分明
    #    origin='lower':      让 (0,0) 点位于左下角，符合常规坐标系
    #    cmap='viridis':      一个视觉效果很好的色谱
    im = ax.imshow(heatmap_data, interpolation='none', origin='lower', cmap='viridis', vmin=0, vmax=1)

    # c) 设置标题和标签
    ax.set_title(f"Shading Efficiency Map for Heliostat {heliostat_id} (High Resolution)", fontsize=16)
    ax.set_xlabel("Microfacet X Index", fontsize=12)
    ax.set_ylabel("Microfacet Y Index", fontsize=12)

    # d) 创建一个颜色条
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label('Shading Efficiency', rotation=270, labelpad=15, fontsize=12)

    # e) 调整刻度，避免过于密集
    #    如果微面元数量很多，可以每隔10个或20个显示一个刻度
    tick_interval = max(1, side_length_x // 12)  # 自动计算刻度间隔，最多显示12个标签
    ax.set_xticks(np.arange(0, side_length_x, tick_interval))
    ax.set_yticks(np.arange(0, side_length_y, tick_interval))

    # f) 保存为高分辨率图像文件
    #    dpi=300 是印刷级别的清晰度，非常适合查看细节
    output_filename = f"heliostat_{heliostat_id}_map_sharp.png"
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')

    print(f"Success! Saved sharp, high-resolution map to {output_filename}")
    plt.show()  # 在屏幕上显示图像


# --- 主程序入口 ---
# --- 主程序入口 ---
if __name__ == '__main__':
    # --- 修改这里 ---
    HELIOSAT_ID = 1000  # 定义变量，全大写
    # ----------------

    CSV_PATH = f"heliostat_{HELIOSAT_ID}_shading_map.csv"

    # 确保调用函数时使用的变量名与定义时完全一致（包括大小写）
    plot_heatmap(CSV_PATH, HELIOSAT_ID)