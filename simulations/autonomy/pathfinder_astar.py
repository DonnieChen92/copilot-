#!/usr/bin/env python3
"""
Path Finder for Auto-Drive (A* Algorithm)

A* grid-based pathfinding for autonomous navigation. Finds the shortest
obstacle-free path from start to goal on a 2D grid where 1 = obstacle
and 0 = traversable.
"""

import heapq
import math


def a_star(start, goal, grid):
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: math.dist(start, goal)}

    while open_set:
        current = heapq.heappop(open_set)[1]
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if (
                0 <= neighbor[0] < rows
                and 0 <= neighbor[1] < cols
                and grid[neighbor[0]][neighbor[1]] == 0
            ):
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + math.dist(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return None


if __name__ == "__main__":
    grid = [
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [1, 0, 0, 0],
    ]

    start = (0, 0)
    goal = (3, 3)
    path = a_star(start, goal, grid)
    print("Safe path:", path)
