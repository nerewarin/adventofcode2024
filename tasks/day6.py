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

def can_get_stuck(grid, start_row, start_col, direction):
    """Check if the guard can get stuck in a loop with an obstruction placed."""
    visited = set()
    row, col = start_row, start_col
    
    while True:
        if (row, col) in visited:
            return True  # Guard is stuck in a loop
        visited.add((row, col))
        
        dr, dc = DIRECTIONS[direction]
        next_row, next_col = row + dr, col + dc
        
        # If position is invalid or has an obstacle, turn right
        if (not is_valid_position((next_row, next_col), grid) or 
            grid[next_row][next_col] == '#'):
            direction = TURN_RIGHT[direction]
            continue
        
        # Move forward
        row, col = next_row, next_col
        
        # Check if guard has left the map
        if not is_valid_position((row + dr, col + dc), grid):
            break
    
    return False  # Guard did not get stuck

def part2(data):
    grid = [list(line) for line in data]
    row, col, direction = find_start(grid)
    possible_positions = 0
    
    # Check all adjacent positions for potential obstructions
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if abs(dr) + abs(dc) == 1:  # Only check orthogonal positions
                new_row, new_col = row + dr, col + dc
                if is_valid_position((new_row, new_col), grid) and (new_row, new_col) != (row, col):
                    # Temporarily place an obstruction
                    original_cell = grid[new_row][new_col]
                    grid[new_row][new_col] = 'O'  # Place obstruction
                    if can_get_stuck(grid, row, col, direction):
                        possible_positions += 1
                    grid[new_row][new_col] = original_cell  # Restore original cell
    
    return possible_positions

# Update the main block to include part2
if __name__ == "__main__":
    test(part1, 41)
    run(part1)
    run(part2)