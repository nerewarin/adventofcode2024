import re
import os
from typing import List

def find_xmas_occurrences(grid: List[str]) -> int:
    height = len(grid)
    width = len(grid[0])
    count = 0
    
    # Helper function to check if coordinates are within grid bounds
    def in_bounds(x: int, y: int) -> bool:
        return 0 <= x < width and 0 <= y < height
    
    # Check all possible directions for "XMAS"
    directions = [(0,1), (1,0), (1,1), (-1,1), (0,-1), (-1,0), (-1,-1), (1,-1)]
    target = "XMAS"
    
    for y in range(height):
        for x in range(width):
            if grid[y][x] != 'X':
                continue
                
            # Try each direction
            for dx, dy in directions:
                valid = True
                for i in range(len(target)):
                    new_x = x + i*dx
                    new_y = y + i*dy
                    if not in_bounds(new_x, new_y) or grid[new_y][new_x] != target[i]:
                        valid = False
                        break
                if valid:
                    count += 1
    
    return count

def find_xmas_x_pattern(grid: List[str]) -> int:
    height = len(grid)
    width = len(grid[0])
    count = 0
    
    def in_bounds(x: int, y: int) -> bool:
        return 0 <= x < width and 0 <= y < height
        
    def check_arm(x: int, y: int, dx: int, dy: int) -> bool:
        # Check for "MAS" pattern
        x1, y1 = x + dx, y + dy
        x2, y2 = x1 + dx, y1 + dy
        if (in_bounds(x1, y1) and in_bounds(x2, y2) and 
            grid[y1][x1] == 'M' and grid[y2][x2] == 'S'):
            return True
            
        # Check for "SAM" pattern
        if (in_bounds(x1, y1) and in_bounds(x2, y2) and 
            grid[y1][x1] == 'S' and grid[y2][x2] == 'M'):
            return True
            
        return False
    
    # For each center position that could be the middle of an X
    for y in range(height):
        for x in range(width):
            if grid[y][x] != 'A':  # Center must be 'A'
                continue
                
            # Only check one basic X configuration and its variations
            dx1, dy1 = 1, -1  # up-right
            dx2, dy2 = -1, 1  # down-left
            
            # Check all four combinations:
            # 1. Both arms outward
            if check_arm(x, y, dx1, dy1) and check_arm(x, y, dx2, dy2):
                count += 1
                
            # 2. Both arms inward
            if check_arm(x, y, -dx1, -dy1) and check_arm(x, y, -dx2, -dy2):
                count += 1
                
            # 3. First arm outward, second arm inward
            if check_arm(x, y, dx1, dy1) and check_arm(x, y, -dx2, -dy2):
                count += 1
                
            # 4. First arm inward, second arm outward
            if check_arm(x, y, -dx1, -dy1) and check_arm(x, y, dx2, dy2):
                count += 1
                
            # Check the other diagonal configuration
            dx1, dy1 = -1, -1  # up-left
            dx2, dy2 = 1, 1    # down-right
            
            # Check all four combinations for the other diagonal
            # 1. Both arms outward
            if check_arm(x, y, dx1, dy1) and check_arm(x, y, dx2, dy2):
                count += 1
                
            # 2. Both arms inward
            if check_arm(x, y, -dx1, -dy1) and check_arm(x, y, -dx2, -dy2):
                count += 1
                
            # 3. First arm outward, second arm inward
            if check_arm(x, y, dx1, dy1) and check_arm(x, y, -dx2, -dy2):
                count += 1
                
            # 4. First arm inward, second arm outward
            if check_arm(x, y, -dx1, -dy1) and check_arm(x, y, dx2, dy2):
                count += 1
    
    return count // 2  # Divide by 2 because we're counting each pattern twice

def solve_part1(input_data: str) -> int:
    grid = [line.strip() for line in input_data.splitlines() if line.strip()]
    return find_xmas_occurrences(grid)

def solve_part2(input_data: str) -> int:
    grid = [line.strip() for line in input_data.splitlines() if line.strip()]
    return find_xmas_x_pattern(grid)

if __name__ == "__main__":
    # Get the absolute path to the input file
    current_dir = os.path.dirname(os.path.dirname(__file__))
    input_file = os.path.join(current_dir, 'inputs', '4', 'run')
    
    # Read the input file
    with open(input_file, 'r') as f:
        input_data = f.read()
    
    print(f"Part 1: {solve_part1(input_data)}")
    print(f"Part 2: {solve_part2(input_data)}")
    # Print some debug info
    print("\nDebug info:")
    print(f"Input data length: {len(input_data)}")
    print("First few lines of grid:")
    grid = [line.strip() for line in input_data.splitlines() if line.strip()]
    for i, line in enumerate(grid[:5]):
        print(f"Line {i}: {line}")
    print(f"Grid dimensions: {len(grid)} rows x {len(grid[0])} columns")

