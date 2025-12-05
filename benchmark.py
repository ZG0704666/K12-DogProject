"""
Performance Benchmark: Comparing Slow vs Optimized Implementation
This script measures and compares the performance improvements.
"""

import time
import sys
from dog_simulation_slow import MechanicalDog, simulate_dog_movement as simulate_slow
from dog_simulation_optimized import MechanicalDogOptimized, simulate_dog_movement as simulate_optimized


def benchmark_position_updates(iterations=10000):
    """Benchmark position update performance"""
    print("\n" + "=" * 70)
    print("BENCHMARK 1: Position Updates")
    print("=" * 70)
    
    # Slow version
    dog_slow = MechanicalDog("TestDog")
    dog_slow.velocity = [1.0, 0.5, 0.2]
    
    start = time.perf_counter()
    for _ in range(iterations):
        dog_slow.update_position(0.1)
    slow_time = time.perf_counter() - start
    
    # Optimized version
    dog_opt = MechanicalDogOptimized("TestDog")
    dog_opt.velocity = [1.0, 0.5, 0.2]
    
    start = time.perf_counter()
    for _ in range(iterations):
        dog_opt.update_position(0.1)
    opt_time = time.perf_counter() - start
    
    print(f"Slow version:      {slow_time:.4f} seconds")
    print(f"Optimized version: {opt_time:.4f} seconds")
    print(f"Speedup:           {slow_time/opt_time:.2f}x faster")
    print(f"Improvement:       {((slow_time-opt_time)/slow_time*100):.1f}% reduction")


def benchmark_environment_scanning():
    """Benchmark environment scanning performance"""
    print("\n" + "=" * 70)
    print("BENCHMARK 2: Environment Scanning")
    print("=" * 70)
    
    samples = 50
    
    # Slow version
    dog_slow = MechanicalDog("TestDog")
    start = time.perf_counter()
    sensor_data_slow = dog_slow.scan_environment(samples)
    slow_time = time.perf_counter() - start
    
    # Optimized version
    dog_opt = MechanicalDogOptimized("TestDog")
    start = time.perf_counter()
    sensor_data_opt = dog_opt.scan_environment(samples)
    opt_time = time.perf_counter() - start
    
    print(f"Slow version:      {slow_time:.4f} seconds")
    print(f"Optimized version: {opt_time:.4f} seconds")
    print(f"Speedup:           {slow_time/opt_time:.2f}x faster")
    print(f"Improvement:       {((slow_time-opt_time)/slow_time*100):.1f}% reduction")


def benchmark_obstacle_detection():
    """Benchmark obstacle detection performance"""
    print("\n" + "=" * 70)
    print("BENCHMARK 3: Obstacle Detection")
    print("=" * 70)
    
    # Generate test data
    sensor_data = list(range(5000))
    
    # Slow version
    dog_slow = MechanicalDog("TestDog")
    start = time.perf_counter()
    obstacles_slow = dog_slow.find_obstacles(sensor_data)
    slow_time = time.perf_counter() - start
    
    # Optimized version
    dog_opt = MechanicalDogOptimized("TestDog")
    start = time.perf_counter()
    obstacles_opt = dog_opt.find_obstacles(sensor_data)
    opt_time = time.perf_counter() - start
    
    print(f"Slow version:      {slow_time:.4f} seconds")
    print(f"Optimized version: {opt_time:.4f} seconds")
    print(f"Speedup:           {slow_time/opt_time:.2f}x faster")
    print(f"Improvement:       {((slow_time-opt_time)/slow_time*100):.1f}% reduction")


def benchmark_path_planning():
    """Benchmark path planning performance"""
    print("\n" + "=" * 70)
    print("BENCHMARK 4: Path Planning")
    print("=" * 70)
    
    start_pos = [0.0, 0.0, 0.0]
    goal_pos = [10.0, 10.0, 0.0]
    obstacles = set()
    
    # Slow version
    dog_slow = MechanicalDog("TestDog")
    start = time.perf_counter()
    path_slow = dog_slow.plan_path(start_pos, goal_pos, obstacles)
    slow_time = time.perf_counter() - start
    
    # Optimized version
    dog_opt = MechanicalDogOptimized("TestDog")
    start = time.perf_counter()
    path_opt = dog_opt.plan_path(start_pos, goal_pos, obstacles)
    opt_time = time.perf_counter() - start
    
    print(f"Slow version:      {slow_time:.4f} seconds")
    print(f"Optimized version: {opt_time:.4f} seconds")
    print(f"Speedup:           {slow_time/opt_time:.2f}x faster")
    print(f"Improvement:       {((slow_time-opt_time)/slow_time*100):.1f}% reduction")


def benchmark_full_simulation():
    """Benchmark full simulation performance"""
    print("\n" + "=" * 70)
    print("BENCHMARK 5: Full Simulation (100 steps)")
    print("=" * 70)
    
    num_steps = 100
    
    # Slow version
    print("\nRunning slow version...")
    start = time.perf_counter()
    dog_slow = simulate_slow(num_steps)
    slow_time = time.perf_counter() - start
    
    print("\nRunning optimized version...")
    # Optimized version
    start = time.perf_counter()
    dog_opt = simulate_optimized(num_steps)
    opt_time = time.perf_counter() - start
    
    print("\n" + "-" * 70)
    print("COMPARISON:")
    print(f"Slow version:      {slow_time:.4f} seconds")
    print(f"Optimized version: {opt_time:.4f} seconds")
    print(f"Speedup:           {slow_time/opt_time:.2f}x faster")
    print(f"Improvement:       {((slow_time-opt_time)/slow_time*100):.1f}% reduction")


def print_summary():
    """Print summary of optimization techniques"""
    print("\n" + "=" * 70)
    print("OPTIMIZATION TECHNIQUES APPLIED:")
    print("=" * 70)
    print("""
1. IN-PLACE MODIFICATIONS: Modified lists in-place instead of creating new ones
2. MEMORY MANAGEMENT: Used deque with maxlen to limit memory growth
3. REMOVED REDUNDANT OPERATIONS: Eliminated unnecessary calculations
4. AVOIDED STRING OPERATIONS: Used proper data structures instead of strings
5. BETTER DATA STRUCTURES: Used sets instead of lists for membership tests
6. PRE-ALLOCATION: Pre-allocated lists to avoid repeated memory allocations
7. CACHED CALCULATIONS: Stored computed values to avoid recalculation
8. SQUARED DISTANCE: Used squared distance to avoid expensive sqrt operations
9. EFFICIENT STRING BUILDING: Used list join instead of string concatenation
10. REDUCED CALL FREQUENCY: Called expensive operations less frequently
11. BETTER TIMING: Used perf_counter() for more accurate measurements
12. EARLY TERMINATION: Added break conditions to avoid unnecessary iterations

COMPLEXITY IMPROVEMENTS:
- Obstacle detection: O(n²) → O(n) using sets instead of lists
- Path planning: Reduced redundant calculations by ~50%
- Environment scanning: Pre-allocation and cached values
- Memory usage: Bounded history with deque instead of unbounded list
    """)


if __name__ == "__main__":
    print("=" * 70)
    print("MECHANICAL DOG SIMULATION - PERFORMANCE BENCHMARK")
    print("=" * 70)
    print("\nThis benchmark compares the slow vs optimized implementations")
    print("to demonstrate the performance improvements from code optimization.\n")
    
    try:
        # Run individual benchmarks
        benchmark_position_updates(iterations=10000)
        benchmark_environment_scanning()
        benchmark_obstacle_detection()
        benchmark_path_planning()
        
        # Run full simulation benchmark
        benchmark_full_simulation()
        
        # Print summary
        print_summary()
        
        print("\n" + "=" * 70)
        print("BENCHMARK COMPLETE!")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\nBenchmark interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError during benchmark: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
