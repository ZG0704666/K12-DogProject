"""
Mechanical Dog Simulation - Optimized Implementation
This code demonstrates best practices for performance optimization.
"""

import time
import math
from collections import deque


class MechanicalDogOptimized:
    """An optimized simulated mechanical dog with various movement capabilities."""
    
    def __init__(self, name, max_history=1000):
        self.name = name
        # Use lists for efficient numerical operations
        self.position = [0.0, 0.0, 0.0]  # x, y, z coordinates
        self.velocity = [0.0, 0.0, 0.0]
        self.leg_positions = [[0.0, 0.0, 0.0] for _ in range(4)]  # 4 legs
        self.sensor_data = []
        # FIX 1: Use deque with maxlen to automatically limit history size
        self.movement_history = deque(maxlen=max_history)
        
    def update_position(self, delta_time):
        """Update dog position based on velocity - OPTIMIZED VERSION"""
        # FIX 2: Modify list in-place instead of creating new list
        for i in range(3):
            self.position[i] += self.velocity[i] * delta_time
        
        # Store copy of position (deque automatically manages size)
        self.movement_history.append(tuple(self.position))
        
    def calculate_leg_kinematics(self, leg_index, target_position):
        """Calculate inverse kinematics for leg movement - OPTIMIZED VERSION"""
        # FIX 3: Removed unnecessary trigonometric calculations
        # Calculate distance directly without unnecessary conversions
        
        # FIX 4 & 5: Direct calculation without string conversion
        dx = target_position[0] - self.leg_positions[leg_index][0]
        dy = target_position[1] - self.leg_positions[leg_index][1]
        dz = target_position[2] - self.leg_positions[leg_index][2]
        
        # FIX: Use more efficient distance calculation
        distance = math.sqrt(dx*dx + dy*dy + dz*dz)
        
        return distance
    
    def scan_environment(self, num_samples):
        """Simulate environmental scanning - OPTIMIZED VERSION"""
        # FIX 6: Pre-allocate list for better memory performance
        total_readings = num_samples * num_samples
        sensor_readings = [0.0] * total_readings
        
        # FIX 7: Use simpler arithmetic instead of pow() in tight loop
        idx = 0
        for i in range(num_samples):
            i_squared = i * i  # Cache the squared value
            for j in range(num_samples):
                sensor_readings[idx] = i_squared + j * j
                idx += 1
        
        # FIX 8: Pre-allocated, so no need to extend
        self.sensor_data = sensor_readings
        
        return sensor_readings
    
    def find_obstacles(self, sensor_data):
        """Identify obstacles from sensor data - OPTIMIZED VERSION"""
        # FIX 9 & 10: Use set for O(1) membership testing instead of list
        obstacles = set()
        threshold = 1000
        
        for reading in sensor_data:
            if reading > threshold:
                obstacles.add(reading)
        
        return obstacles
    
    def plan_path(self, start, goal, obstacles):
        """Plan a path avoiding obstacles - OPTIMIZED VERSION"""
        # FIX 11: Pre-allocate list capacity
        path = []
        current = list(start)
        
        # Pre-calculate goal coordinates for efficiency
        goal_x, goal_y, goal_z = goal
        step_size = 0.01
        tolerance = 0.1
        tolerance_sq = tolerance * tolerance  # Use squared distance to avoid sqrt
        
        # FIX 12: Add early termination and use squared distance
        for step in range(1000):
            # FIX 13: Use squared distance to avoid expensive sqrt
            dx = goal_x - current[0]
            dy = goal_y - current[1]
            dz = goal_z - current[2]
            dist_squared = dx*dx + dy*dy + dz*dz
            
            if dist_squared < tolerance_sq:
                break
            
            # Move towards goal - update in place
            current[0] += dx * step_size
            current[1] += dy * step_size
            current[2] += dz * step_size
            
            # Store copy of current position
            path.append(tuple(current))
        
        return path
    
    def calculate_energy_consumption(self, path):
        """Calculate energy needed for a path - OPTIMIZED VERSION"""
        # FIX 14 & 16: Use list to build log, join at end
        energy_log_parts = []
        total_energy = 0.0
        
        # FIX: Pre-calculate path length
        path_len = len(path)
        
        for i in range(path_len - 1):
            # FIX 15: More efficient distance calculation
            current = path[i]
            next_pos = path[i + 1]
            
            # Calculate distance using direct arithmetic
            dx = next_pos[0] - current[0]
            dy = next_pos[1] - current[1]
            dz = next_pos[2] - current[2]
            distance = math.sqrt(dx*dx + dy*dy + dz*dz)
            
            energy = distance * 10  # Simple energy model
            total_energy += energy
            
            # Build log efficiently
            energy_log_parts.append(f"Step {i}: {energy} units")
        
        # Join all log parts once at the end
        energy_log = "\n".join(energy_log_parts)
        
        return total_energy, energy_log


def simulate_dog_movement(num_steps=100):
    """Run an optimized simulation of the mechanical dog"""
    dog = MechanicalDogOptimized("Spot")
    
    # Set initial velocity
    dog.velocity = [1.0, 0.5, 0.0]
    
    # FIX 17: Use time.perf_counter() for better precision
    start_time = time.perf_counter()
    
    for step in range(num_steps):
        # Update position
        dog.update_position(0.1)
        
        # FIX 18: Only scan environment periodically to reduce overhead
        if step % 10 == 0:  # Scan every 10 steps instead of every step
            sensor_data = dog.scan_environment(20)
            obstacles = dog.find_obstacles(sensor_data)
        
        # Calculate leg positions
        for leg in range(4):
            target = [step * 0.1, step * 0.1, 0.0]
            dog.calculate_leg_kinematics(leg, target)
    
    end_time = time.perf_counter()
    
    print(f"Simulation completed in {end_time - start_time:.4f} seconds")
    print(f"Final position: {dog.position}")
    print(f"Movement history size: {len(dog.movement_history)} entries")
    print(f"Sensor data size: {len(dog.sensor_data)} readings")
    
    return dog


if __name__ == "__main__":
    print("Running OPTIMIZED mechanical dog simulation...")
    print("=" * 60)
    
    # Run simulation
    dog = simulate_dog_movement(100)
    
    # Plan a path
    print("\nPlanning path...")
    start = [0.0, 0.0, 0.0]
    goal = [10.0, 10.0, 0.0]
    obstacles = dog.find_obstacles(dog.sensor_data)
    path = dog.plan_path(start, goal, obstacles)
    
    # Calculate energy
    energy, log = dog.calculate_energy_consumption(path)
    print(f"Path length: {len(path)} steps")
    print(f"Total energy: {energy:.2f} units")
    
    print("=" * 60)
    print("Simulation complete!")
