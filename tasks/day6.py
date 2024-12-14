import sys
from pathlib import Path
# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from utils.test_and_run import test, run

DIRECTIONS = {
    '^': (-1, 0),  # up
    '>': (0, 1),   # right
    'v': (1, 0),   # down
    '<': (0, -1),  # left
}

TURN_RIGHT = {
    '^': '>',
    '>': 'v',
    'v': '<',
    '<': '^'
}

def find_start(grid):
    """Find starting position and direction of the guard"""
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell in DIRECTIONS:
                return i, j, cell
    raise ValueError("No starting position found")

def is_valid_position(pos, grid):
    """Check if position is within grid bounds"""
    return (0 <= pos[0] < len(grid) and 
            0 <= pos[1] < len(grid[0]))

def simulate_guard_path(data):
    # Convert input to grid
    grid = [list(line) for line in data]
    
    # Find start position
    row, col, direction = find_start(grid)
    visited = {(row, col)}
    
    while True:
        # Check position in front
        dr, dc = DIRECTIONS[direction]
        next_row, next_col = row + dr, col + dc
        
        # If position is invalid or has obstacle, turn right
        if (not is_valid_position((next_row, next_col), grid) or 
            grid[next_row][next_col] == '#'):
            direction = TURN_RIGHT[direction]
            continue
            
        # Move forward
        row, col = next_row, next_col
        visited.add((row, col))
        
        # Check if guard has left the map
        if not is_valid_position((row + dr, col + dc), grid):
            break
    
    return len(visited)

def part1(data):
    return simulate_guard_path(data)

if __name__ == "__main__":
    test(part1, 41)
    run(part1)
