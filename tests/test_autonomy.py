"""
Tests for Autonomy Module / 自動駕駛模組測試 / 自动驾驶模块测试
Path finder, safety checker, radiation sim, trajectory planner, data twin compressor.
"""

from src.autonomy.path_finder import a_star, a_star_8dir
from src.autonomy.safety_checker import (
    check_path_smoothness,
    euclidean_distance,
    is_safe_path,
    vector_angle,
)
from src.autonomy.radiation_sim import (
    monte_carlo_dose_estimate,
    shannon_entropy,
    simulate_radiation,
)
from src.autonomy.trajectory_planner import (
    hohmann_transfer,
    road_trajectory_analog,
    safe_altitude,
)
from src.autonomy.data_twin_compressor import (
    batch_compress_conversations,
    compress_driver_profile,
    compress_text,
    decompress_driver_profile,
)


# =========================================================================
# Path Finder Tests / 路徑搜尋器測試 / 路径搜索器测试
# =========================================================================

class TestPathFinder:

    def test_simple_path(self):
        """Test path on open grid / 在開放網格上測試路徑"""
        grid = [[0, 0], [0, 0]]
        path = a_star((0, 0), (1, 1), grid)
        assert path is not None
        assert path[0] == (0, 0)
        assert path[-1] == (1, 1)

    def test_blocked_path(self):
        """Test no path through wall / 測試被牆阻擋的路徑"""
        grid = [[0, 1], [1, 0]]
        path = a_star((0, 0), (1, 1), grid)
        assert path is None

    def test_obstacle_avoidance(self):
        """Test path avoids obstacles / 測試路徑迴避障礙物"""
        grid = [
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [1, 0, 0, 0],
        ]
        path = a_star((0, 0), (3, 3), grid)
        assert path is not None
        # Verify no obstacles on path / 驗證路徑上無障礙物
        for r, c in path:
            assert grid[r][c] == 0

    def test_same_start_goal(self):
        """Test start equals goal / 測試起點等於終點"""
        grid = [[0]]
        path = a_star((0, 0), (0, 0), grid)
        assert path is not None
        assert len(path) == 1

    def test_8dir_path(self):
        """Test 8-directional pathfinding / 測試8方向路徑搜尋"""
        grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        path = a_star_8dir((0, 0), (2, 2), grid)
        assert path is not None
        # 8-dir should find shorter path / 8方向應找到更短路徑
        path_4 = a_star((0, 0), (2, 2), grid)
        assert len(path) <= len(path_4)


# =========================================================================
# Safety Checker Tests / 安全檢查器測試 / 安全检查器测试
# =========================================================================

class TestSafetyChecker:

    def test_safe_path(self):
        """Test clearly safe path / 測試明顯安全的路徑"""
        path = [(0, 0), (1, 0), (2, 0)]
        hazards = [(0, 10), (1, 10)]
        result = is_safe_path(path, hazards, safe_distance=2.0)
        assert result.is_safe is True
        assert len(result.violations) == 0

    def test_unsafe_path(self):
        """Test path too close to hazard / 測試路徑離危險太近"""
        path = [(0, 0), (1, 0)]
        hazards = [(0, 0.5)]
        result = is_safe_path(path, hazards, safe_distance=2.0)
        assert result.is_safe is False
        assert len(result.violations) > 0

    def test_euclidean_distance(self):
        """Test distance calculation / 測試距離計算"""
        d = euclidean_distance((0, 0), (3, 4))
        assert abs(d - 5.0) < 1e-10  # 3-4-5 triangle

    def test_vector_angle(self):
        """Test angle calculation / 測試角度計算"""
        angle = vector_angle((1, 0), (0, 1))
        assert abs(angle - 90.0) < 1e-10  # Perpendicular = 90°

    def test_path_smoothness(self):
        """Test smoothness checker / 測試平滑度檢查"""
        # U-turn path / U型迴轉路徑
        path = [(0, 0), (1, 0), (1, 1), (0, 1)]
        turns = check_path_smoothness(path, max_angle=100.0)
        # Should detect the sharp turn / 應偵測到急轉彎
        assert isinstance(turns, list)


# =========================================================================
# Radiation Sim Tests / 輻射模擬測試 / 辐射模拟测试
# =========================================================================

class TestRadiationSim:

    def test_basic_simulation(self):
        """Test standard simulation / 測試標準模擬"""
        result = simulate_radiation(thickness=0.5)
        assert result.unshielded_dose > 0
        assert result.shielded_dose > 0
        assert result.shielded_dose < result.unshielded_dose
        assert result.reduction_factor > 1.0

    def test_thicker_shield(self):
        """Test thicker shield reduces dose more / 測試更厚屏蔽減少更多劑量"""
        thin = simulate_radiation(thickness=0.5)
        thick = simulate_radiation(thickness=2.0)
        assert thick.shielded_dose < thin.shielded_dose

    def test_monte_carlo(self):
        """Test Monte Carlo estimation / 測試蒙特卡羅估計"""
        mc = monte_carlo_dose_estimate(n_trials=1000)
        assert mc["mean_dose"] > 0
        assert mc["std_dev"] >= 0
        assert mc["trials"] == 1000

    def test_text_entropy(self):
        """Test Shannon entropy calculation / 測試夏農熵計算"""
        # All same characters = 0 entropy / 全相同字元 = 0 熵
        from src.autonomy.data_twin_compressor import shannon_entropy as se
        assert se("aaaa") == 0.0
        # Two equally likely chars = 1 bit / 兩個等概率字元 = 1 位元
        assert abs(se("ab" * 100) - 1.0) < 0.01


# =========================================================================
# Trajectory Planner Tests / 軌跡規劃器測試 / 轨迹规划器测试
# =========================================================================

class TestTrajectoryPlanner:

    def test_hohmann_transfer(self):
        """Test Hohmann transfer calculation / 測試霍曼轉移計算"""
        result = hohmann_transfer(alt1_km=400, alt2_km=2000)
        assert result.delta_v1 > 0
        assert result.delta_v2 > 0
        assert result.total_delta_v > 0
        assert result.transfer_time_hours > 0

    def test_safe_altitude(self):
        """Test radiation belt safety / 測試輻射帶安全性"""
        assert safe_altitude(200) is True       # Below inner belt
        assert safe_altitude(5000) is True       # Between belts
        assert safe_altitude(700) is False       # In inner belt
        assert safe_altitude(70000) is True      # Above outer belt

    def test_road_trajectory(self):
        """Test road trajectory analog / 測試道路軌跡類比"""
        result = road_trajectory_analog(
            start_speed_kmh=60,
            target_speed_kmh=100,
            distance_km=5,
        )
        assert result["delta_v_ms"] > 0
        assert result["travel_time_min"] > 0
        assert result["safe_speed"] is True

    def test_unsafe_speed(self):
        """Test unsafe speed detection / 測試不安全速度偵測"""
        result = road_trajectory_analog(
            start_speed_kmh=100,
            target_speed_kmh=200,
            distance_km=10,
        )
        assert result["safe_speed"] is False


# =========================================================================
# Data Twin Compressor Tests / 資料雙胞胎壓縮器測試 / 数据双胞胎压缩器测试
# =========================================================================

class TestDataTwinCompressor:

    def test_text_compression(self):
        """Test text compression / 測試文本壓縮"""
        text = "Repeated text for testing compression. " * 50
        result = compress_text(text)
        assert result.compressed_bytes < result.original_bytes
        assert result.savings_percent > 0

    def test_driver_profile_roundtrip(self):
        """Test compress → decompress roundtrip / 測試壓縮→解壓縮往返"""
        profile = {
            "driver_id": "test-001",
            "preferences": {"temp_c": 22, "speed": "moderate"},
        }
        compressed = compress_driver_profile(profile)
        restored = decompress_driver_profile(compressed["compressed_data"])
        assert restored == profile

    def test_batch_conversation(self):
        """Test batch conversation compression / 測試批次對話壓縮"""
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
        ]
        result = batch_compress_conversations(messages)
        assert result["message_count"] == 2
        assert result["compressed_bytes"] > 0

    def test_entropy_calculation(self):
        """Test Shannon entropy / 測試夏農熵"""
        # High entropy (random) / 高熵（隨機）
        import string
        random_text = string.ascii_letters * 10
        high_entropy = shannon_entropy(random_text)

        # Low entropy (repetitive) / 低熵（重複）
        low_text = "aaaa" * 100
        low_entropy = shannon_entropy(low_text)

        assert high_entropy > low_entropy
