def parse_input(input_text):
    # Split input into rules and updates
    rules_text, updates_text = input_text.strip().split('\n\n')
    
    # Parse rules
    rules = {}
    for line in rules_text.split('\n'):
        if '|' not in line:
            continue
        before, after = map(int, line.split('|'))
        if before not in rules:
            rules[before] = set()
        rules[before].add(after)
    
    # Parse updates
    updates = []
    for line in updates_text.split('\n'):
        if ',' not in line:
            continue
        update = list(map(int, line.split(',')))
        updates.append(update)
    
    return rules, updates

def is_valid_order(pages, rules):
    # Check if the order of pages satisfies all applicable rules
    for i, page in enumerate(pages):
        if page in rules:
            # For each rule where this page must come before others
            for must_come_after in rules[page]:
                # If the page that must come after is in our list
                if must_come_after in pages:
                    # Find its position
                    after_pos = pages.index(must_come_after)
                    # If it comes before our current page, the order is invalid
                    if after_pos < i:
                        return False
    return True

def solve_day5(input_text):
    # Parse input
    rules, updates = parse_input(input_text)
    
    # Find valid updates and their middle numbers
    middle_sum = 0
    for update in updates:
        if is_valid_order(update, rules):
            # Get middle number
            middle_index = len(update) // 2
            middle_sum += update[middle_index]
    
    return middle_sum

def main():
    # Read input from file
    with open('./inputs/5/run', 'r') as file:
        input_text = file.read()
    
    # Solve the puzzle
    result = solve_day5(input_text)
    print(f"The sum of middle page numbers from correctly-ordered updates is: {result}")

if __name__ == "__main__":
    main()
