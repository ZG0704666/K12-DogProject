"""
Mechanical Dog Simulation - Initial Implementation (WITH PERFORMANCE ISSUES)
This code demonstrates common performance bottlenecks in robotics simulations.
"""

import time
import math


class MechanicalDog:
    """A simulated mechanical dog with various movement capabilities."""
    
    def __init__(self, name):
        self.name = name
        self.position = [0.0, 0.0, 0.0]  # x, y, z coordinates
        self.velocity = [0.0, 0.0, 0.0]
        self.leg_positions = [[0.0, 0.0, 0.0] for _ in range(4)]  # 4 legs
        self.sensor_data = []
        self.movement_history = []
        
    def update_position(self, delta_time):
        """Update dog position based on velocity - INEFFICIENT VERSION"""
        # ISSUE 1: Creating new list every iteration instead of modifying in-place
        new_position = []
        for i in range(len(self.position)):
            new_position.append(self.position[i] + self.velocity[i] * delta_time)
        self.position = new_position
        
        # ISSUE 2: Storing entire position history without limit
        self.movement_history.append(self.position[:])
        
    def calculate_leg_kinematics(self, leg_index, target_position):
        """Calculate inverse kinematics for leg movement - INEFFICIENT VERSION"""
        # ISSUE 3: Repeated expensive trigonometric calculations
        angles = []
        for i in range(100):  # Unnecessary iterations
            angle = math.sin(i * 0.01) * math.cos(i * 0.01)
            angles.append(angle)
        
        # ISSUE 4: Inefficient distance calculation with string concatenation
        distance_str = ""
        for i in range(3):
            distance_str += str(target_position[i] - self.leg_positions[leg_index][i])
            distance_str += ","
        
        # ISSUE 5: Converting back from string (pointless conversion)
        distances = [float(x) for x in distance_str.rstrip(',').split(',')]
        distance = math.sqrt(sum([d**2 for d in distances]))
        
        return distance
    
    def scan_environment(self, num_samples):
        """Simulate environmental scanning - INEFFICIENT VERSION"""
        # ISSUE 6: Quadratic time complexity - nested loops
        sensor_readings = []
        for i in range(num_samples):
            for j in range(num_samples):
                # ISSUE 7: Using expensive operations in tight loop
                reading = math.pow(i, 2) + math.pow(j, 2)
                sensor_readings.append(reading)
        
        # ISSUE 8: Repeatedly extending list instead of pre-allocation
        self.sensor_data.extend(sensor_readings)
        
        return sensor_readings
    
    def find_obstacles(self, sensor_data):
        """Identify obstacles from sensor data - INEFFICIENT VERSION"""
        # ISSUE 9: Using list for membership testing (O(n) lookup)
        obstacles = []
        threshold = 1000
        
        for reading in sensor_data:
            if reading > threshold:
                # ISSUE 10: Checking if already in list (O(n) operation)
                if reading not in obstacles:
                    obstacles.append(reading)
        
        return obstacles
    
    def plan_path(self, start, goal, obstacles):
        """Plan a path avoiding obstacles - INEFFICIENT VERSION"""
        # ISSUE 11: Creating many temporary lists
        path = []
        current = list(start)
        
        # ISSUE 12: Inefficient iteration without early termination
        for step in range(1000):
            # Copy current position inefficiently
            next_pos = []
            for coord in current:
                next_pos.append(coord)
            
            # ISSUE 13: Redundant distance calculations
            dist_to_goal = math.sqrt(
                (goal[0] - next_pos[0])**2 +
                (goal[1] - next_pos[1])**2 +
                (goal[2] - next_pos[2])**2
            )
            
            if dist_to_goal < 0.1:
                break
            
            # Move towards goal
            for i in range(3):
                next_pos[i] += (goal[i] - next_pos[i]) * 0.01
            
            path.append(next_pos)
            current = next_pos
        
        return path
    
    def calculate_energy_consumption(self, path):
        """Calculate energy needed for a path - INEFFICIENT VERSION"""
        # ISSUE 14: String concatenation in loop
        energy_log = ""
        total_energy = 0
        
        for i in range(len(path) - 1):
            # ISSUE 15: Redundant calculations
            current = path[i]
            next_pos = path[i + 1]
            
            distance = 0
            for j in range(3):
                distance += (next_pos[j] - current[j]) ** 2
            distance = math.sqrt(distance)
            
            energy = distance * 10  # Simple energy model
            total_energy += energy
            
            # ISSUE 16: Inefficient string building
            energy_log += f"Step {i}: {energy} units\n"
        
        return total_energy, energy_log


def simulate_dog_movement(num_steps=100):
    """Run a simulation of the mechanical dog - INEFFICIENT VERSION"""
    dog = MechanicalDog("Spot")
    
    # Set initial velocity
    dog.velocity = [1.0, 0.5, 0.0]
    
    # ISSUE 17: Not using efficient timing
    start_time = time.time()
    
    for step in range(num_steps):
        # Update position
        dog.update_position(0.1)
        
        # ISSUE 18: Calling expensive operations every iteration
        sensor_data = dog.scan_environment(20)
        obstacles = dog.find_obstacles(sensor_data)
        
        # Calculate leg positions
        for leg in range(4):
            target = [step * 0.1, step * 0.1, 0]
            dog.calculate_leg_kinematics(leg, target)
    
    end_time = time.time()
    
    print(f"Simulation completed in {end_time - start_time:.4f} seconds")
    print(f"Final position: {dog.position}")
    print(f"Movement history size: {len(dog.movement_history)} entries")
    print(f"Sensor data size: {len(dog.sensor_data)} readings")
    
    return dog


if __name__ == "__main__":
    print("Running inefficient mechanical dog simulation...")
    print("=" * 60)
    
    # Run simulation
    dog = simulate_dog_movement(100)
    
    # Plan a path
    print("\nPlanning path...")
    start = [0, 0, 0]
    goal = [10, 10, 0]
    obstacles = dog.find_obstacles(dog.sensor_data)
    path = dog.plan_path(start, goal, obstacles)
    
    # Calculate energy
    energy, log = dog.calculate_energy_consumption(path)
    print(f"Path length: {len(path)} steps")
    print(f"Total energy: {energy:.2f} units")
    
    print("=" * 60)
    print("Simulation complete!")
