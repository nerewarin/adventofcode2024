from adventofcode2024.utils.test_and_run import test, run
from typing import List, Tuple
import logging
import os

# Configure logging based on environment variable
log_level = os.getenv('level', 'INFO')
logging.basicConfig(level=log_level)

def parse_disk_map(input_data: str | list) -> List[int]:
    if isinstance(input_data, list):
        input_data = input_data[0]  # Take first line since input is single-line
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

def find_gaps(blocks: List[Tuple[int, int, int]]) -> List[Tuple[int, int]]:
    """Find all gaps in the current state. Returns list of (start, length) tuples."""
    gaps = []
    current_pos = 0
    
    # Sort blocks by position
    sorted_blocks = sorted(blocks, key=lambda x: x[1])
    
    # Find gaps between blocks
    for _, start, length in sorted_blocks:
        if start > current_pos:
            gaps.append((current_pos, start - current_pos))
        current_pos = start + length
    
    # Always consider remaining space at the end as a gap
    total_length = max((start + length) for _, start, length in blocks) if blocks else 0
    if current_pos < total_length:
        gaps.append((current_pos, total_length - current_pos))
    
    return gaps


def move_blocks_left(blocks: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    """Move blocks from right to left, filling gaps."""
    result = []  # Blocks that have been moved
    unmoved = list(blocks)  # Blocks that haven't been moved yet
    total_length = sum(1 for _, _, length in blocks for _ in range(length)) * 2  # Total disk space including gaps
    
    # Process blocks from right to left
    for i in range(len(blocks) - 1, -1, -1):
        file_id, orig_pos, length = blocks[i]
        logging.debug(f"\nMoving block {file_id} (length {length})")
        
        # Remove this block from unmoved list
        unmoved = [b for b in unmoved if b[0] != file_id]
        
        # Find gaps considering both moved and unmoved blocks
        current_state = result + unmoved
        current_pos = 0
        gaps = []
        
        # Find gaps between blocks
        for _, start, block_length in sorted(current_state, key=lambda x: x[1]):
            if start > current_pos:
                gaps.append((current_pos, start - current_pos))
            current_pos = start + block_length
        
        # Always add remaining space as a gap
        if current_pos < total_length:
            gaps.append((current_pos, total_length - current_pos))
            
        logging.debug(f"Current gaps: {gaps}")
        
        # Fill gaps with current block
        remaining_length = length
        for gap_start, gap_length in gaps:
            if remaining_length <= 0:
                break
                
            # Fill this gap
            fill_length = min(gap_length, remaining_length)
            result.append((file_id, gap_start, fill_length))
            remaining_length -= fill_length
            logging.debug(f"Filled gap at {gap_start} with {fill_length} blocks")
        
        logging.debug(f"Current state: {visualize_state(result + unmoved, total_length)}")
    
    return sorted(result, key=lambda x: x[1])  # Sort by position

def calculate_checksum(positions: List[Tuple[int, int, int]]) -> int:
    """Calculate checksum based on final positions."""
    checksum = 0
    for file_id, start_pos, length in positions:
        for pos in range(start_pos, start_pos + length):
            checksum += pos * file_id
    return checksum

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
