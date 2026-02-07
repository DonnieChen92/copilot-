"""
Safety Checker for Autonomy / 自動駕駛安全檢查器 / 自动驾驶安全检查器
====================================================================
Distance-based hazard avoidance using vector mathematics.
基於距離的危險迴避，使用向量數學。
基于距离的危险回避，使用向量数学。

Mathematical Foundation / 數學基礎 / 数学基础:
- Euclidean distance: d = sqrt((x₂-x₁)² + (y₂-y₁)²)
  歐幾里得距離 / 欧几里得距离
- Dot product for angle checks: a·b = |a||b|cos(θ)
  點積用於角度檢查 / 点积用于角度检查
- Newton's 1st Law: ΣF = 0 → stable control (balanced forces)
  牛頓第一定律：ΣF = 0 → 穩定控制（平衡力）

Integration with Tesla FSD / 與 Tesla FSD 整合:
- Sensor data → hazard coordinates / 感測器資料 → 危險座標
- Safety checker validates planned path / 安全檢查器驗證規劃路徑
- Returns safe/unsafe with detailed metrics / 回傳安全/不安全與詳細指標

Author: Donnie Chen (donniechen92@gmail.com)
"""

import math
from dataclasses import dataclass
from typing import Any


@dataclass
class SafetyResult:
    """
    Safety check result / 安全檢查結果 / 安全检查结果
    """
    is_safe: bool                          # Overall safety / 整體安全性
    min_distance: float                    # Minimum hazard distance / 最小危險距離
    closest_hazard: tuple[float, ...] | None  # Closest hazard point / 最近危險點
    closest_path_point: tuple[float, ...] | None  # Path point nearest to hazard
    violations: list[dict[str, Any]]       # Safety violations / 安全違規列表
    margin: float                          # Safety margin / 安全餘量


def euclidean_distance(
    p1: tuple[float, ...],
    p2: tuple[float, ...],
) -> float:
    """
    Euclidean distance between two points.
    兩點之間的歐幾里得距離。
    两点之间的欧几里得距离。

    d = sqrt(Σ(p1ᵢ - p2ᵢ)²)
    """
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))


def dot_product(
    v1: tuple[float, ...],
    v2: tuple[float, ...],
) -> float:
    """
    Dot product of two vectors / 兩個向量的點積 / 两个向量的点积

    a · b = Σ(aᵢ × bᵢ)
    """
    return sum(a * b for a, b in zip(v1, v2))


def vector_angle(
    v1: tuple[float, ...],
    v2: tuple[float, ...],
) -> float:
    """
    Angle between two vectors in degrees.
    兩個向量之間的角度（度）。
    两个向量之间的角度（度）。

    θ = arccos((a · b) / (|a| × |b|))
    """
    dot = dot_product(v1, v2)
    mag1 = math.sqrt(sum(x**2 for x in v1))
    mag2 = math.sqrt(sum(x**2 for x in v2))

    if mag1 == 0 or mag2 == 0:
        return 0.0

    cos_theta = max(-1.0, min(1.0, dot / (mag1 * mag2)))
    return math.degrees(math.acos(cos_theta))


def is_safe_path(
    path: list[tuple[float, ...]],
    hazards: list[tuple[float, ...]],
    safe_distance: float = 2.0,
) -> SafetyResult:
    """
    Check if a path maintains safe distance from all hazards.
    檢查路徑是否與所有危險保持安全距離。
    检查路径是否与所有危险保持安全距离。

    Args:
        path: List of path coordinates / 路徑座標列表
        hazards: List of hazard coordinates / 危險座標列表
        safe_distance: Minimum safe distance threshold / 最小安全距離閾值

    Returns:
        SafetyResult with detailed analysis / 包含詳細分析的安全結果
    """
    min_dist = float("inf")
    closest_hazard = None
    closest_path_point = None
    violations: list[dict[str, Any]] = []

    for point in path:
        for hazard in hazards:
            dist = euclidean_distance(point, hazard)

            if dist < min_dist:
                min_dist = dist
                closest_hazard = hazard
                closest_path_point = point

            if dist < safe_distance:
                violations.append({
                    "path_point": point,
                    "hazard": hazard,
                    "distance": round(dist, 4),
                    "deficit": round(safe_distance - dist, 4),
                })

    return SafetyResult(
        is_safe=len(violations) == 0,
        min_distance=round(min_dist, 4),
        closest_hazard=closest_hazard,
        closest_path_point=closest_path_point,
        violations=violations,
        margin=round(min_dist - safe_distance, 4) if min_dist != float("inf") else 0.0,
    )


def check_path_smoothness(
    path: list[tuple[float, ...]],
    max_angle: float = 90.0,
) -> list[dict[str, Any]]:
    """
    Check path for sharp turns (comfort & stability).
    檢查路徑的急轉彎（舒適性與穩定性）。
    检查路径的急转弯（舒适性与稳定性）。

    Newton's 1st Law application: smooth paths maintain balanced forces.
    牛頓第一定律應用：平滑路徑維持平衡力。

    Args:
        path: List of coordinates / 座標列表
        max_angle: Maximum acceptable turn angle / 最大可接受轉向角度

    Returns:
        List of sharp turn violations / 急轉彎違規列表
    """
    sharp_turns: list[dict[str, Any]] = []

    for i in range(1, len(path) - 1):
        # Vector from previous to current / 從前一點到當前點的向量
        v1 = tuple(path[i][j] - path[i - 1][j] for j in range(len(path[i])))
        # Vector from current to next / 從當前點到下一點的向量
        v2 = tuple(path[i + 1][j] - path[i][j] for j in range(len(path[i])))

        angle = vector_angle(v1, v2)

        if angle > max_angle:
            sharp_turns.append({
                "index": i,
                "point": path[i],
                "angle": round(angle, 2),
                "exceeds_by": round(angle - max_angle, 2),
            })

    return sharp_turns


# --- Demo / 示範 / 示范 ---
if __name__ == "__main__":
    # Example: Check path safety / 範例：檢查路徑安全
    path = [(0, 0), (1, 0), (2, 0), (3, 0)]
    hazards = [(1, 1), (2, 2)]

    result = is_safe_path(path, hazards, safe_distance=2.0)
    print(f"Path safe? / 路徑安全？: {result.is_safe}")
    print(f"Min distance / 最小距離: {result.min_distance}")
    print(f"Safety margin / 安全餘量: {result.margin}")
    print(f"Violations / 違規: {len(result.violations)}")

    # Example: Check smoothness / 範例：檢查平滑度
    curvy_path = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 2)]
    turns = check_path_smoothness(curvy_path, max_angle=90.0)
    print(f"\nSharp turns / 急轉彎: {len(turns)}")
    for t in turns:
        print(f"  Point {t['point']}: {t['angle']}°")
