# import numpy as np
# from scipy.signal import butter, filtfilt
# import matplotlib.pyplot as plt

# # 生成示例信号（含1Hz抖动 + 10Hz有效信号）
# fs = 30  # 采样频率30Hz
# t = np.arange(0, 10, 1/fs)
# # signal = 0.2 * np.sin(2*np.pi*1*t) + 0.2 * np.sin(2*np.pi*2*t) + 0.2 * np.sin(2*np.pi*4*t) + np.sin(2*np.pi*0.1*t)  # 1Hz抖动 + 0.1Hz信号
# orin = np.sin(2*np.pi*0.1*t)
# signal = 0.2 * np.sin(2*np.pi*1*t) + 0.2 * np.sin(2*np.pi*2*t) + 0.2 * np.sin(2*np.pi*3*t) + 0.2 * np.sin(2*np.pi*4*t) + 0.2 * np.sin(2*np.pi*5*t) + orin
# filtered_signal = []  # 初始化为空列表

# ffps = 6
# ft = 0.33

# for i, value in enumerate(signal):
#     total = 0
#     count = 0
#     for d in range(int(ft * ffps)):
#         b = int(d * (fs / ffps))
#         if i >= b:
#             total += signal[i - b]
#             count += 1
#     if count > 0:
#         filtered_signal.append(total / count)
#     else:
#         filtered_signal.append(0)

# # 将 filtered_signal 转换为 numpy 数组
# filtered_signal = np.array(filtered_signal)

# # 绘图对比
# plt.figure()
# plt.plot(t, orin, 'o-', label='orin', markersize=1, markerfacecolor='r', markeredgecolor='r', color='g')
# plt.plot(t, signal, 'o-', label='signal', markersize=1, markerfacecolor='b', markeredgecolor='b', color='y')
# plt.plot(t, filtered_signal, 'o-', label='filtered', markersize=1, markerfacecolor='r', markeredgecolor='r', color='b')
# plt.legend()
# plt.show()


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from collections import deque

# 全局参数初始化
fs = 30  # 采样频率30Hz
t = np.arange(0, 10, 1/fs)  # 时间序列（固定不变）

# 定义移动平均滤波器
def moving_average(signal, window_size):
    return np.convolve(signal, np.ones(window_size)/window_size, mode='same')


class MovingAverageFilter:
    def __init__(self, window_size):
        self.window_size = window_size
        self.buffer = deque(maxlen=window_size)
    
    def update(self, new_value):
        """接收新数据并返回当前移动平均值"""
        self.buffer.append(new_value)
        return sum(self.buffer) / len(self.buffer)

# 更新图像的函数
def update_plot(*args):
    # 获取当前参数
    window_size = int(window_size_slider.get())
    base_freq = base_freq_slider.get()
    
    # 生成动态信号
    orin = 2*np.sin(2*np.pi*0.1*t)  # 原始信号保持0.1Hz
    signal = (
        0.1 * np.sin(2*np.pi*base_freq*t) + 
        0.1 * np.sin(2*np.pi*(base_freq+1)*t) + 
        0.1 * np.sin(2*np.pi*(base_freq+2)*t) + 
        0.1 * np.sin(2*np.pi*(base_freq+3)*t) + 
        0.1 * np.sin(2*np.pi*(base_freq+4)*t) + 
        orin
    )
    

    filtered_signal = []
    filter = MovingAverageFilter(window_size)
    for data in signal:
        value = filter.update(data)
        filtered_signal.append(value)
    filtered_signal = np.array(filtered_signal)


    # 更新绘图
    ax.clear()
    ax.plot(t, orin, 'o-', label='Original (0.1Hz)', markersize=1, markerfacecolor='r', markeredgecolor='r', color='g')
    ax.plot(t, signal, 'o-', label=f'Signal (Base {base_freq:.1f}Hz)', markersize=1, markerfacecolor='b', markeredgecolor='b', color='y')
    ax.plot(t, filtered_signal, 'o-', label=f'Filtered (Window {window_size})', markersize=1, markerfacecolor='r', markeredgecolor='r', color='b')
    ax.legend()
    canvas.draw()

# 创建主窗口
root = tk.Tk()
root.title("实时信号滤波分析仪")

# 创建matplotlib图形
fig, ax = plt.subplots(figsize=(10, 5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# 控制面板
control_frame = ttk.Frame(root)
control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

# 窗口大小控制
ttk.Label(control_frame, text="滤波窗口大小:").grid(row=0, column=0, sticky="w")
window_size_slider = ttk.Scale(
    control_frame, 
    from_=1, 
    to=100, 
    orient=tk.HORIZONTAL,
    command=update_plot
)
window_size_slider.set(10)
window_size_slider.grid(row=0, column=1, sticky="ew")
window_size_label = ttk.Label(control_frame, text="10")
window_size_label.grid(row=0, column=2, padx=5)

# 信号基频控制
ttk.Label(control_frame, text="信号基频 (Hz):").grid(row=1, column=0, sticky="w")
base_freq_slider = ttk.Scale(
    control_frame,
    from_=0.5,
    to=5.0,
    orient=tk.HORIZONTAL,
    command=update_plot
)
base_freq_slider.set(1.0)
base_freq_slider.grid(row=1, column=1, sticky="ew")
base_freq_label = ttk.Label(control_frame, text="1.0")
base_freq_label.grid(row=1, column=2, padx=5)

# 动态更新标签值
def update_slider_labels(event):
    window_size_label.config(text=f"{int(window_size_slider.get())}")
    base_freq_label.config(text=f"{base_freq_slider.get():.1f}")

window_size_slider.bind("<Motion>", update_slider_labels)
base_freq_slider.bind("<Motion>", update_slider_labels)

# 初始化图像
update_plot()

# 运行主循环
root.mainloop()