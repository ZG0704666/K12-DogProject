"""
Unit tests for mechanical dog simulations
Tests verify that optimizations maintain correctness.
"""

import math
import sys
from dog_simulation_slow import MechanicalDog
from dog_simulation_optimized import MechanicalDogOptimized


def test_position_update_correctness():
    """Verify position updates produce same results"""
    print("Testing position update correctness...")
    
    dog_slow = MechanicalDog("Test")
    dog_opt = MechanicalDogOptimized("Test")
    
    # Set same initial conditions
    dog_slow.velocity = [1.0, 2.0, 0.5]
    dog_opt.velocity = [1.0, 2.0, 0.5]
    
    # Update positions
    delta_time = 0.1
    for _ in range(10):
        dog_slow.update_position(delta_time)
        dog_opt.update_position(delta_time)
    
    # Check positions match
    for i in range(3):
        assert abs(dog_slow.position[i] - dog_opt.position[i]) < 1e-6, \
            f"Position mismatch at index {i}"
    
    print("✓ Position updates are correct")


def test_leg_kinematics_correctness():
    """Verify leg kinematics calculations are equivalent"""
    print("Testing leg kinematics correctness...")
    
    dog_slow = MechanicalDog("Test")
    dog_opt = MechanicalDogOptimized("Test")
    
    target = [1.0, 2.0, 3.0]
    
    dist_slow = dog_slow.calculate_leg_kinematics(0, target)
    dist_opt = dog_opt.calculate_leg_kinematics(0, target)
    
    assert abs(dist_slow - dist_opt) < 1e-6, \
        f"Distance calculation mismatch: {dist_slow} vs {dist_opt}"
    
    print("✓ Leg kinematics calculations are correct")


def test_environment_scanning_correctness():
    """Verify environment scanning produces same data"""
    print("Testing environment scanning correctness...")
    
    dog_slow = MechanicalDog("Test")
    dog_opt = MechanicalDogOptimized("Test")
    
    samples = 10
    data_slow = dog_slow.scan_environment(samples)
    data_opt = dog_opt.scan_environment(samples)
    
    assert len(data_slow) == len(data_opt), \
        "Sensor data length mismatch"
    
    for i in range(len(data_slow)):
        assert abs(data_slow[i] - data_opt[i]) < 1e-6, \
            f"Sensor data mismatch at index {i}"
    
    print("✓ Environment scanning is correct")


def test_obstacle_detection_correctness():
    """Verify obstacle detection finds same obstacles"""
    print("Testing obstacle detection correctness...")
    
    dog_slow = MechanicalDog("Test")
    dog_opt = MechanicalDogOptimized("Test")
    
    # Create test sensor data
    sensor_data = [500, 1200, 800, 1500, 900, 2000]
    
    obstacles_slow = dog_slow.find_obstacles(sensor_data)
    obstacles_opt = dog_opt.find_obstacles(sensor_data)
    
    # Convert to sets for comparison
    obstacles_slow_set = set(obstacles_slow)
    
    assert obstacles_slow_set == obstacles_opt, \
        f"Obstacle sets don't match: {obstacles_slow_set} vs {obstacles_opt}"
    
    print("✓ Obstacle detection is correct")


def test_path_planning_correctness():
    """Verify path planning produces valid paths"""
    print("Testing path planning correctness...")
    
    dog_slow = MechanicalDog("Test")
    dog_opt = MechanicalDogOptimized("Test")
    
    start = [0.0, 0.0, 0.0]
    goal = [5.0, 5.0, 0.0]
    obstacles = set()
    
    path_slow = dog_slow.plan_path(start, goal, obstacles)
    path_opt = dog_opt.plan_path(start, goal, obstacles)
    
    # Both should reach goal (within tolerance)
    def distance_to_goal(path, goal):
        if not path:
            return float('inf')
        last = path[-1]
        dx = goal[0] - last[0]
        dy = goal[1] - last[1]
        dz = goal[2] - last[2]
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    dist_slow = distance_to_goal(path_slow, goal)
    dist_opt = distance_to_goal(path_opt, goal)
    
    assert dist_slow < 0.5, f"Slow path didn't reach goal: distance {dist_slow}"
    assert dist_opt < 0.5, f"Optimized path didn't reach goal: distance {dist_opt}"
    
    # Path lengths should be similar (within 10%)
    ratio = len(path_slow) / len(path_opt) if len(path_opt) > 0 else 1.0
    assert 0.9 <= ratio <= 1.1, \
        f"Path lengths too different: {len(path_slow)} vs {len(path_opt)}"
    
    print("✓ Path planning is correct")


def test_energy_calculation_correctness():
    """Verify energy calculations are consistent"""
    print("Testing energy calculation correctness...")
    
    dog_slow = MechanicalDog("Test")
    dog_opt = MechanicalDogOptimized("Test")
    
    # Create a simple test path
    path = [
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [2.0, 0.0, 0.0],
        [3.0, 0.0, 0.0]
    ]
    
    energy_slow, _ = dog_slow.calculate_energy_consumption(path)
    energy_opt, _ = dog_opt.calculate_energy_consumption(path)
    
    assert abs(energy_slow - energy_opt) < 1e-3, \
        f"Energy calculation mismatch: {energy_slow} vs {energy_opt}"
    
    # Energy should be 30.0 (3 steps of 1.0 distance * 10 energy per distance)
    expected = 30.0
    assert abs(energy_slow - expected) < 1e-3, \
        f"Energy calculation wrong: {energy_slow} vs expected {expected}"
    
    print("✓ Energy calculations are correct")


def test_memory_bounds():
    """Verify optimized version bounds memory usage"""
    print("Testing memory bounds...")
    
    dog_opt = MechanicalDogOptimized("Test", max_history=100)
    dog_opt.velocity = [1.0, 1.0, 0.0]
    
    # Update position many times
    for _ in range(1000):
        dog_opt.update_position(0.1)
    
    # History should be bounded
    assert len(dog_opt.movement_history) <= 100, \
        f"History not bounded: {len(dog_opt.movement_history)} entries"
    
    print("✓ Memory bounds working correctly")


def run_all_tests():
    """Run all correctness tests"""
    print("=" * 70)
    print("RUNNING CORRECTNESS TESTS")
    print("=" * 70)
    print("\nVerifying that optimizations maintain correctness...\n")
    
    tests = [
        test_position_update_correctness,
        test_leg_kinematics_correctness,
        test_environment_scanning_correctness,
        test_obstacle_detection_correctness,
        test_path_planning_correctness,
        test_energy_calculation_correctness,
        test_memory_bounds,
    ]
    
    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ TEST FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ TEST ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    if failed == 0:
        print("ALL TESTS PASSED! ✓")
        print("Optimizations maintain correctness.")
    else:
        print(f"TESTS FAILED: {failed}/{len(tests)}")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
