"""
Radiation Simulation for Space-Linked Autonomy
輻射模擬用於太空連結自駕 / 辐射模拟用于太空连接自驾
=======================================================
Simulates radiation dose for satellite-aided autonomous driving
(e.g., Tesla vehicles using Starlink for navigation & communication).

模擬衛星輔助自動駕駛的輻射劑量（例如使用星鏈進行導航和通訊的 Tesla 車輛）。
模拟卫星辅助自动驾驶的辐射剂量（例如使用星链进行导航和通信的 Tesla 车辆）。

Mathematical Foundation / 數學基礎 / 数学基础:
- Exponential attenuation: I = I₀ · e^(-μ·x·ρ)
  指數衰減 / 指数衰减
  where μ = attenuation coefficient, x = thickness, ρ = density
- Integration for total dose: D = ∫ Φ(E) · (1/E) dE
  總劑量積分 / 总剂量积分
- Monte Carlo simulation for uncertainty estimation
  蒙特卡羅模擬用於不確定性估計 / 蒙特卡洛模拟用于不确定性估计

Author: Donnie Chen (donniechen92@gmail.com)
"""

import math
import random
from dataclasses import dataclass
from typing import Any


@dataclass
class RadiationResult:
    """Radiation simulation result / 輻射模擬結果 / 辐射模拟结果"""
    unshielded_dose: float      # Unshielded dose / 無屏蔽劑量 / 无屏蔽剂量
    shielded_dose: float        # Shielded dose / 有屏蔽劑量 / 有屏蔽剂量
    reduction_factor: float     # Dose reduction ratio / 劑量減少比率 / 剂量减少比率
    shielding_efficiency: float # Shielding efficiency % / 屏蔽效率 %


def flux_spectrum(
    energy: float,
    flux_constant: float = 1e4,
) -> float:
    """
    Simple power-law flux spectrum: Φ(E) = C / E
    簡單冪律通量光譜 / 简单幂律通量光谱

    Args:
        energy: Particle energy (MeV) / 粒子能量
        flux_constant: Flux constant (particles/cm²/s) / 通量常數

    Returns:
        Flux at given energy / 給定能量的通量
    """
    if energy <= 0:
        return 0.0
    return flux_constant / energy


def dose_rate(energy: float, flux_constant: float = 1e4) -> float:
    """
    Unshielded dose rate at given energy.
    給定能量的無屏蔽劑量率。
    给定能量的无屏蔽剂量率。

    D'(E) = Φ(E) × (1/E) = C / E²
    """
    if energy <= 0:
        return 0.0
    return flux_constant / (energy * energy)


def shielded_dose_rate(
    energy: float,
    thickness: float = 0.5,
    attenuation_coeff: float = 0.1,
    density: float = 2.7,
    flux_constant: float = 1e4,
) -> float:
    """
    Shielded dose rate with exponential attenuation.
    帶指數衰減的有屏蔽劑量率。
    带指数衰减的有屏蔽剂量率。

    D'_shielded(E) = D'(E) × e^(-μ × x × ρ)

    Args:
        energy: Particle energy (MeV) / 粒子能量
        thickness: Shield thickness (cm) / 屏蔽厚度
        attenuation_coeff: Linear attenuation coefficient / 線性衰減係數
        density: Shield material density (g/cm³), default=2.7 (aluminum)
                 屏蔽材料密度，預設=2.7（鋁）
        flux_constant: Flux constant / 通量常數
    """
    unshielded = dose_rate(energy, flux_constant)
    attenuation = math.exp(-attenuation_coeff * thickness * density)
    return unshielded * attenuation


def numerical_integrate(
    func: Any,
    e_min: float,
    e_max: float,
    n_steps: int = 1000,
) -> float:
    """
    Simple trapezoidal numerical integration.
    簡單梯形數值積分。
    简单梯形数值积分。

    ∫[a,b] f(x)dx ≈ Σ (f(xᵢ) + f(xᵢ₊₁)) × Δx / 2
    """
    dx = (e_max - e_min) / n_steps
    total = 0.0
    for i in range(n_steps):
        e1 = e_min + i * dx
        e2 = e1 + dx
        total += (func(e1) + func(e2)) * dx / 2.0
    return total


def simulate_radiation(
    thickness: float = 0.5,
    attenuation_coeff: float = 0.1,
    density: float = 2.7,
    e_min: float = 1.0,
    e_max: float = 1000.0,
    flux_constant: float = 1e4,
    n_steps: int = 1000,
) -> RadiationResult:
    """
    Full radiation simulation.
    完整輻射模擬。
    完整辐射模拟。

    Args:
        thickness: Shield thickness (cm) / 屏蔽厚度
        attenuation_coeff: Attenuation coefficient / 衰減係數
        density: Material density (g/cm³) / 材料密度
        e_min: Minimum energy (MeV) / 最小能量
        e_max: Maximum energy (MeV) / 最大能量
        flux_constant: Flux normalization / 通量歸一化
        n_steps: Integration steps / 積分步數

    Returns:
        RadiationResult with dose comparisons / 包含劑量比較的結果
    """
    # Unshielded total dose / 無屏蔽總劑量
    unshielded = numerical_integrate(
        lambda e: dose_rate(e, flux_constant), e_min, e_max, n_steps
    )

    # Shielded total dose / 有屏蔽總劑量
    shielded = numerical_integrate(
        lambda e: shielded_dose_rate(e, thickness, attenuation_coeff, density, flux_constant),
        e_min,
        e_max,
        n_steps,
    )

    reduction = unshielded / shielded if shielded > 0 else float("inf")
    efficiency = (1 - shielded / unshielded) * 100 if unshielded > 0 else 0

    return RadiationResult(
        unshielded_dose=round(unshielded, 4),
        shielded_dose=round(shielded, 4),
        reduction_factor=round(reduction, 4),
        shielding_efficiency=round(efficiency, 2),
    )


def monte_carlo_dose_estimate(
    n_trials: int = 10000,
    thickness: float = 0.5,
    attenuation_coeff: float = 0.1,
    density: float = 2.7,
    e_min: float = 1.0,
    e_max: float = 1000.0,
) -> dict[str, float]:
    """
    Monte Carlo dose estimation with uncertainty.
    蒙特卡羅劑量估計（含不確定性）。
    蒙特卡洛剂量估计（含不确定性）。

    Randomly samples energies and averages dose.
    隨機採樣能量並平均劑量。
    """
    doses: list[float] = []

    for _ in range(n_trials):
        energy = random.uniform(e_min, e_max)
        dose = shielded_dose_rate(energy, thickness, attenuation_coeff, density)
        doses.append(dose)

    mean_dose = sum(doses) / len(doses)
    variance = sum((d - mean_dose) ** 2 for d in doses) / len(doses)
    std_dev = math.sqrt(variance)

    return {
        "mean_dose": round(mean_dose, 6),
        "std_dev": round(std_dev, 6),
        "min_dose": round(min(doses), 6),
        "max_dose": round(max(doses), 6),
        "trials": n_trials,
    }


# --- Demo / 示範 / 示范 ---
if __name__ == "__main__":
    # Standard simulation / 標準模擬
    result = simulate_radiation(thickness=0.5, attenuation_coeff=0.1, density=2.7)
    print(f"Unshielded dose / 無屏蔽劑量: {result.unshielded_dose:.2f}")
    print(f"Shielded dose / 有屏蔽劑量: {result.shielded_dose:.2f}")
    print(f"Reduction factor / 減少因子: {result.reduction_factor:.2f}x")
    print(f"Shielding efficiency / 屏蔽效率: {result.shielding_efficiency:.1f}%")

    # Monte Carlo estimation / 蒙特卡羅估計
    print("\nMonte Carlo estimation / 蒙特卡羅估計:")
    mc = monte_carlo_dose_estimate(n_trials=10000)
    print(f"  Mean dose / 平均劑量: {mc['mean_dose']}")
    print(f"  Std dev / 標準差: {mc['std_dev']}")
    print(f"  Trials / 試驗數: {mc['trials']}")
