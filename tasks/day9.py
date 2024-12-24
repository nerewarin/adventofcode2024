from adventofcode2024.utils.test_and_run import test, run
from typing import List, Tuple
import logging
import os

# Configure logging based on environment variable
log_level = os.getenv('level', 'INFO')
logging.basicConfig(level=log_level)

def parse_disk_map(input_data: str | list) -> List[int]:
    if isinstance(input_data, list):
        input_data = input_data[0]
    return [int(x) for x in input_data.strip()]

def get_initial_state(disk_map: List[int]) -> List[Tuple[int, int, int]]:
    """Convert disk map to list of (file_id, start_pos, length) tuples."""
    blocks = []
    file_id = 0
    current_pos = 0
    
    for i, length in enumerate(disk_map):
        if i % 2 == 0:  # File block
            blocks.append((file_id, current_pos, length))
            file_id += 1
        current_pos += length
    return blocks

def move_blocks_left(blocks: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    """Move blocks from right to left, filling gaps."""
    # Create a list to track occupied positions
    total_length = sum(1 for _, _, length in blocks for _ in range(length)) * 2
    occupied = [False] * total_length
    result = []
    
    # Mark initially occupied positions
    for file_id, start, length in blocks:
        for pos in range(start, start + length):
            occupied[pos] = True
    
    # Process blocks from right to left
    for i in range(len(blocks) - 1, -1, -1):
        file_id, orig_start, length = blocks[i]
        logging.debug(f"\nMoving block {file_id} (length {length})")
        
        # Unmark original positions
        for pos in range(orig_start, orig_start + length):
            occupied[pos] = False
        
        # Find gaps and fill them
        remaining_length = length
        current_pos = 0
        
        while remaining_length > 0:
            # Find next free position
            while current_pos < total_length and occupied[current_pos]:
                current_pos += 1
            
            # Find length of this gap
            gap_end = current_pos
            while gap_end < total_length and not occupied[gap_end]:
                gap_end += 1
            
            # Fill gap
            fill_length = min(gap_end - current_pos, remaining_length)
            result.append((file_id, current_pos, fill_length))
            
            # Mark positions as occupied
            for pos in range(current_pos, current_pos + fill_length):
                occupied[pos] = True
                
            logging.debug(f"Filled gap at {current_pos} with {fill_length} blocks")
            
            remaining_length -= fill_length
            current_pos = gap_end
    
    return sorted(result, key=lambda x: x[1])

def calculate_checksum(positions: List[Tuple[int, int, int]]) -> int:
    """Calculate checksum based on final positions."""
    return sum(pos * file_id for file_id, start_pos, length in positions 
              for pos in range(start_pos, start_pos + length))

def visualize_state(blocks: List[Tuple[int, int, int]], total_length: int) -> str:
    """Helper function to visualize the disk state."""
    disk = ['.' for _ in range(total_length)]
    for file_id, start_pos, length in blocks:
        for i in range(length):
            disk[start_pos + i] = str(file_id)
    return ''.join(disk)

def solve_part1(input_data: str | list) -> int:
    disk_map = parse_disk_map(input_data)
    initial_state = get_initial_state(disk_map)
    
    logging.debug(f"Initial: {visualize_state(initial_state, sum(disk_map))}")
    final_state = move_blocks_left(initial_state)
    logging.debug(f"Final: {visualize_state(final_state, sum(disk_map))}")
    
    return calculate_checksum(final_state)

test(solve_part1, expected=1928)
run(solve_part1)
# 6307275788409