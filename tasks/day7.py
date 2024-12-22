import sys
from pathlib import Path
from utils.test_and_run import test, run
import itertools

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

# Define operators as a constant
OPERATORS = ['+', '*']

def evaluate_expression(numbers, operators):
    """Evaluate the expression based on the numbers and operators."""
    result = numbers[0]
    for i in range(len(operators)):
        if operators[i] == '+':
            result += numbers[i + 1]
        elif operators[i] == '*':
            result *= numbers[i + 1]
    return result

def can_make_true(test_value, numbers):
    """Check if the test value can be made true with any combination of operators."""
    for operators in itertools.product(OPERATORS, repeat=len(numbers) - 1):
        if evaluate_expression(numbers, operators) == test_value:
            return True
    return False

def part1(data):
    total_sum = 0
    for line in data:
        test_value, numbers_str = line.split(':')
        test_value = int(test_value.strip())
        numbers = list(map(int, numbers_str.strip().split()))
        
        # Check if the test value can be made true with the given numbers
        if can_make_true(test_value, numbers):
            total_sum += test_value
            
    return total_sum

if __name__ == "__main__":
    # Use the test function to validate part1
    test(part1, 3749)  # Expected output for the test data is 3749
    
    # Run the actual input data
    run(part1)