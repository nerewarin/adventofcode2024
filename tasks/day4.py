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
    
    # Check all possible directions: horizontal, vertical, and diagonal
    directions = [
        (1,0),   # right
        (0,1),   # down 
        (1,1),   # diagonal down-right
        (-1,1),  # diagonal down-left
        (-1,0),  # left
        (0,-1),  # up
        (-1,-1), # diagonal up-left
        (1,-1)   # diagonal up-right
    ]
    
    # For each starting position
    for y in range(height):
        for x in range(width):
            # For each direction
            for dx, dy in directions:
                # Check if "XMAS" can be formed from this position and direction
                valid = True
                word = "XMAS"
                for i in range(len(word)):
                    new_x = x + i*dx
                    new_y = y + i*dy
                    if not in_bounds(new_x, new_y) or grid[new_y][new_x] != word[i]:
                        valid = False
                        break
                if valid:
                    count += 1
    
    return count

def solve_part1(input_data: str) -> int:
    # Split input into lines and remove any trailing whitespace
    grid = [line.strip() for line in input_data.splitlines() if line.strip()]
    return find_xmas_occurrences(grid)

def solve_part2(input_data: str) -> int:
    # Part 2 not implemented yet
    return 0

if __name__ == "__main__":
    # Get the absolute path to the input file
    current_dir = os.path.dirname(os.path.dirname(__file__))
    input_file = os.path.join(current_dir, 'inputs', '4', 'run')
    
    # Read the input file
    with open(input_file, 'r') as f:
        input_data = f.read()
    
    print(f"Part 1: {solve_part1(input_data)}")
    print(f"Part 2: {solve_part2(input_data)}")
