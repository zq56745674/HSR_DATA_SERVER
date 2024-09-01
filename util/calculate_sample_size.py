import math
from scipy.stats import norm

def calculate_sample_size(confidence_level, margin_of_error, proportion=0.5):
    # confidence_level: 置信水平
    # margin_of_error: 误差范围
    # proportion: 样本中的比例（默认为0.5，即样本中的正负样本数量相等）

    # Z值对应的置信水平
    z_values = {
        0.90: 1.645,
        0.95: 1.96,
        0.99: 2.576
    }
    
    z = z_values[confidence_level]
    p = proportion
    e = margin_of_error
    
    n = (z**2 * p * (1 - p)) / e**2
    return math.ceil(n)

def finite_population_correction(n, N):
    print(f"总体量: {N}")
    return math.ceil(n / (1 + (n - 1) / N))

# 示例：95%的置信水平，±5%的误差范围
sample_size = calculate_sample_size(0.95, 0.05, 0.03)
print(f"所需的样本量: {sample_size}")

# 2.1亿数据，95%的置信水平，±5%的误差范围
total_population = 78400000
sample_size = calculate_sample_size(0.95, 0.05, 0.03)
adjusted_sample_size = finite_population_correction(sample_size, total_population)
print(f"2.1亿数据所需的样本量（有限总体修正后）: {adjusted_sample_size}")


def calculate_margin_of_error(n, N, p=0.5):
    # 计算未调整的误差范围
    E = 1.96 * math.sqrt((p * (1 - p)) / n)
    # 计算有限总体修正后的误差范围
    E_adj = E * math.sqrt((N - n) / (N - 1))
    return E_adj

def calculate_confidence_level(n, E, p=0.5):
    # 计算置信水平对应的Z值
    Z = E / math.sqrt((p * (1 - p)) / n)
    # 通过标准正态分布表查找置信水平
    confidence_level = norm.cdf(Z) - norm.cdf(-Z)
    return confidence_level

# 总体规模
N = 106000000
# 样本量
n = 1800
# 样本比例
p = 0.035

# 计算误差范围
E = calculate_margin_of_error(n, N, p)
print(f"误差范围: {E:.4f}")

# 计算置信水平
confidence_level = calculate_confidence_level(n, E, p)
print(f"置信水平: {confidence_level:.4f}")

# 计算置信区间
lower_bound = p - E
upper_bound = p + E
print(f"置信区间: ({lower_bound:.4f}, {upper_bound:.4f})")

# 计算误差值
error_value = E / p
print(f"误差值: {error_value:.4f}")