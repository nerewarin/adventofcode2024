"""
--- Day 8: Resonant Collinearity ---
You find yourselves on the roof of a top-secret Easter Bunny installation.

While The Historians do their thing, you take a look at the familiar huge antenna. Much to your surprise, it seems to have been reconfigured to emit a signal that makes people 0.1% more likely to buy Easter Bunny brand Imitation Mediocre Chocolate as a Christmas gift! Unthinkable!

Scanning across the city, you find that there are actually many such antennas. Each antenna is tuned to a specific frequency indicated by a single lowercase letter, uppercase letter, or digit. You create a map (your puzzle input) of these antennas. For example:

............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
The signal only applies its nefarious effect at specific antinodes based on the resonant frequencies of the antennas. In particular, an antinode occurs at any point that is perfectly in line with two antennas of the same frequency - but only when one of the antennas is twice as far away as the other. This means that for any pair of antennas with the same frequency, there are two antinodes, one on either side of them.

So, for these two antennas with frequency a, they create the two antinodes marked with #:

..........
...#......
..........
....a.....
..........
.....a....
..........
......#...
..........
..........
Adding a third antenna with the same frequency creates several more antinodes. It would ideally add four antinodes, but two are off the right side of the map, so instead it adds only two:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......#...
..........
..........
Antennas with different frequencies don't create antinodes; A and a count as different frequencies. However, antinodes can occur at locations that contain antennas. In this diagram, the lone antenna with frequency capital A creates no antinodes but has a lowercase-a-frequency antinode at its location:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......A...
..........
..........
The first example has antennas with two different frequencies, so the antinodes they create look like this, plus an antinode overlapping the topmost A-frequency antenna:

......#....#
...#....0...
....#0....#.
..#....0....
....0....#..
.#....A.....
...#........
#......#....
........A...
.........A..
..........#.
..........#.
Because the topmost A-frequency antenna overlaps with a 0-frequency antinode, there are 14 total unique locations that contain an antinode within the bounds of the map.

Calculate the impact of the signal. How many unique locations within the bounds of the map contain an antinode?
"""
from collections import defaultdict

from utils.test_and_run import test, run

def calculate_antinodes(input_map):
    # Parse the input map and identify the positions of all antennas
    antennas = {}
    for y, row in enumerate(input_map):
        for x, char in enumerate(row):
            if char.isalnum():  # Check if the character is an antenna
                antennas.setdefault(char, []).append((x, y))

    # Find antinodes for each pair of antennas with the same frequency
    antinodes = set()
    for freq, positions in antennas.items():
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                p1 = positions[i]
                p2 = positions[j]
                # Calculate the potential antinode positions
                antinode1 = (p1[0] - (p2[0] - p1[0]), p1[1] - (p2[1] - p1[1]))
                antinode2 = (p2[0] + (p2[0] - p1[0]), p2[1] + (p2[1] - p1[1]))
                # Add the antinodes to the set if they are within the map bounds
                if 0 <= antinode1[0] < len(input_map[0]) and 0 <= antinode1[1] < len(input_map):
                    antinodes.add(antinode1)
                if 0 <= antinode2[0] < len(input_map[0]) and 0 <= antinode2[1] < len(input_map):
                    antinodes.add(antinode2)

    # Return the total number of unique antinode positions
    return len(antinodes)

def calculate_antinodes_part2(input_map):
    # Parse the input map and identify the positions of all antennas
    antennas = defaultdict(list)
    for y, row in enumerate(input_map):
        for x, char in enumerate(row):
            if char.isalnum():  # Check if the character is an antenna
                antennas[char].append((x, y))

    # Function to check if points are aligned (collinear)
    def check_aligned(p1, p2, p3):
        return (p1[0] - p2[0]) * (p2[1] - p3[1]) == (p1[1] - p2[1]) * (p2[0] - p3[0])

    # Find antinodes for each frequency
    antinodes = set()
    for freq, positions in antennas.items():
        if len(positions) < 3:
            continue
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                for k in range(j + 1, len(positions)):
                    p1 = positions[i]
                    p2 = positions[j]
                    p3 = positions[k]
                    if check_aligned(p1, p2, p3):
                        # Calculate the potential antinode positions
                        antinode1 = (2 * p2[0] - p1[0], 2 * p2[1] - p1[1])
                        antinode2 = (2 * p1[0] - p2[0], 2 * p1[1] - p2[1])
                        # Add the antinodes to the set if they are within the map bounds
                        if 0 <= antinode1[0] < len(input_map[0]) and 0 <= antinode1[1] < len(input_map):
                            antinodes.add(antinode1)
                        if 0 <= antinode2[0] < len(input_map[0]) and 0 <= antinode2[1] < len(input_map):
                            antinodes.add(antinode2)
                        antinodes.add(p1)
                        antinodes.add(p2)
                        antinodes.add(p3)

    # Return the total number of unique antinode positions
    return len(antinodes)


# Update the main block to include the new function and test it with the provided input
if __name__ == "__main__":
    # Test and run the function
    test(calculate_antinodes, expected=14)
    run(calculate_antinodes)

    test(calculate_antinodes_part2, expected=34)
    run(calculate_antinodes_part2)