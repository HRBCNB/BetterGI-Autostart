import numpy as np
import matplotlib.pyplot as plt

# 1. 定义分段函数
def resistance_factor_func(x):
    condlist = [x <= 0, (x > 0) & (x <= 0.75), x > 0.75]
    funclist = [
        lambda x: 1 - x / 2,        # 抗性 <= 0
        lambda x: 1 - x,            # 0 < 抗性 <= 0.75
        lambda x: 1 / (4 * x + 1)   # 抗性 > 0.75
    ]
    return np.piecewise(x, condlist, funclist)

# 2. 生成数据
# 设定范围从 -0.5 (-50%) 到 2.0 (200%)
x = np.linspace(-0.5, 2.0, 1000)
y = resistance_factor_func(x)

# 3. 绘图
plt.figure(figsize=(10, 6), dpi=100)
plt.plot(x, y, label='Resistance Factor', color='#1f77b4', linewidth=2.5)

# 4. 标注转折点
critical_x = [0, 0.75]
critical_y = [1, 0.25]
plt.scatter(critical_x, critical_y, color='red', zorder=5)

# 5. 添加辅助线和文字
plt.axhline(0, color='black', linewidth=0.8)
plt.axvline(0, color='gray', linestyle='--', alpha=0.6)
plt.axvline(0.75, color='red', linestyle='--', alpha=0.4)



# 6. 图表修饰
plt.title('Resistance Factor Curve', fontsize=14)
plt.xlabel('Resistance (x)', fontsize=12)
plt.ylabel('Damage Multiplier (y)', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()
plt.ylim(0, 1.5)

# 显示图像
plt.show()