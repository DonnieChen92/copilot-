"""
Path Finder for Auto-Drive / 自動駕駛路徑搜尋器 / 自动驾驶路径搜索器
====================================================================
A* algorithm for safe road navigation.
A* 演算法用於安全道路導航。
A* 算法用于安全道路导航。

Mathematical Foundation / 數學基礎 / 数学基础:
- Heuristic: Euclidean distance / 啟發式：歐幾里得距離
  h(n) = sqrt((x₂ - x₁)² + (y₂ - y₁)²)
- Graph theory: shortest path = minimum sum of edge weights
  圖論：最短路徑 = 邊權重的最小總和
  图论：最短路径 = 边权重的最小总和

Integration with Tesla FSD / 與 Tesla FSD 整合:
- Camera/sensor grid → obstacle map / 攝影機/感測器網格 → 障礙物地圖
- A* finds optimal path avoiding obstacles / A* 搜尋迴避障礙物的最佳路徑
- Output feeds into trajectory planner / 輸出供給軌跡規劃器

Author: Donnie Chen (donniechen92@gmail.com)
"""

import heapq
import math
from typing import Optional


def a_star(
    start: tuple[int, int],
    goal: tuple[int, int],
    grid: list[list[int]],
) -> Optional[list[tuple[int, int]]]:
    """
    A* pathfinding algorithm on a 2D grid.
    在 2D 網格上的 A* 路徑搜尋演算法。
    在 2D 网格上的 A* 路径搜索算法。

    Args:
        start: Starting coordinate (row, col) / 起始座標（列, 行）
        goal: Target coordinate (row, col) / 目標座標（列, 行）
        grid: 2D grid where 0 = open, 1 = obstacle
              2D 網格，0 = 開放, 1 = 障礙物

    Returns:
        List of coordinates forming the path, or None if no path exists.
        構成路徑的座標列表，若無路徑則回傳 None。
        构成路径的坐标列表，若无路径则返回 None。

    Mathematical basis / 數學基礎:
        f(n) = g(n) + h(n)
        where g(n) = cost from start to n
              h(n) = Euclidean heuristic estimate to goal
              其中 g(n) = 從起點到 n 的成本
                   h(n) = 到目標的歐幾里得啟發式估計
    """
    rows, cols = len(grid), len(grid[0])

    # Priority queue: (f_score, node) / 優先佇列：(f值, 節點)
    open_set: list[tuple[float, tuple[int, int]]] = []
    heapq.heappush(open_set, (0.0, start))

    # Track path / 追蹤路徑 / 追踪路径
    came_from: dict[tuple[int, int], tuple[int, int]] = {}

    # g_score: cost from start / g值：從起點的成本
    g_score: dict[tuple[int, int], float] = {start: 0.0}

    # f_score: g + heuristic / f值：g + 啟發式
    f_score: dict[tuple[int, int], float] = {start: math.dist(start, goal)}

    # 4-directional movement / 四方向移動 / 四方向移动
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while open_set:
        current = heapq.heappop(open_set)[1]

        # Goal reached / 到達目標 / 到达目标
        if current == goal:
            path: list[tuple[int, int]] = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        # Explore neighbors / 探索鄰居 / 探索邻居
        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)

            # Bounds check / 邊界檢查 / 边界检查
            if not (0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols):
                continue

            # Obstacle check / 障礙物檢查 / 障碍物检查
            if grid[neighbor[0]][neighbor[1]] == 1:
                continue

            tentative_g = g_score[current] + 1.0

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + math.dist(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    # No path found / 未找到路徑 / 未找到路径
    return None


def a_star_8dir(
    start: tuple[int, int],
    goal: tuple[int, int],
    grid: list[list[int]],
) -> Optional[list[tuple[int, int]]]:
    """
    A* with 8-directional movement (includes diagonals).
    8方向移動的 A*（包含對角線）。
    8方向移动的 A*（包含对角线）。

    Diagonal cost = sqrt(2) ≈ 1.414
    對角線成本 = sqrt(2) ≈ 1.414
    """
    rows, cols = len(grid), len(grid[0])
    open_set: list[tuple[float, tuple[int, int]]] = []
    heapq.heappush(open_set, (0.0, start))
    came_from: dict[tuple[int, int], tuple[int, int]] = {}
    g_score: dict[tuple[int, int], float] = {start: 0.0}

    # 8 directions including diagonals / 8方向包含對角線
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),       # Cardinal / 基本方向
        (-1, -1), (-1, 1), (1, -1), (1, 1),      # Diagonal / 對角線
    ]

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            path: list[tuple[int, int]] = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if not (0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols):
                continue
            if grid[neighbor[0]][neighbor[1]] == 1:
                continue

            # Diagonal cost = sqrt(2), cardinal cost = 1
            move_cost = math.sqrt(2) if (dx != 0 and dy != 0) else 1.0
            tentative_g = g_score[current] + move_cost

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + math.dist(neighbor, goal)
                heapq.heappush(open_set, (f, neighbor))

    return None


# --- Demo / 示範 / 示范 ---
if __name__ == "__main__":
    # Example grid / 範例網格 / 示例网格
    # 0 = open road, 1 = obstacle
    # 0 = 開放道路, 1 = 障礙物
    grid = [
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [1, 0, 0, 0],
    ]

    start = (0, 0)
    goal = (3, 3)

    path = a_star(start, goal, grid)
    print(f"Safe path (4-dir) / 安全路徑: {path}")

    path_8 = a_star_8dir(start, goal, grid)
    print(f"Safe path (8-dir) / 安全路徑: {path_8}")
