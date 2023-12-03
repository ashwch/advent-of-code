"""
URL: https://adventofcode.com/2023/day/3

--- Day 3: Gear Ratios ---

You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?


--- Part Two ---

The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?

"""

from calendar import c
from collections import defaultdict
from ipaddress import ip_address
from typing import Dict, List, Tuple

from traitlets import default
from utils import get_input
from string import punctuation
from itertools import chain, groupby

SYMBOLS = set(punctuation) - set('.')


def get_grid(input):
    return [list(line) for line in input.splitlines()]

def check_adjacent(start: int, end: int, current_row: List[str], above_row: List[str], below_row: List[str]):
    """Check if any of the symbols are adjacent to the numbers, including diagonally."""

    if not set(current_row[start:end]).isdisjoint(SYMBOLS):
        return True
    
    if not set(above_row[start:end]).isdisjoint(SYMBOLS):
        return True
        
    if not set(below_row[start:end]).isdisjoint(SYMBOLS):
        return True

    return False


def solve_part_one_and_two():
    input = get_input(3)
    grid = get_grid(input)

    # Cover the whole grid with a '.' border to make it easier to check for adjacent symbols
    # without ugly index checking.
    row_length = len(grid[0])
    grid.insert(0, ['.'] * row_length)
    grid.append(['.'] * row_length)
    
    for row in grid:
        row.insert(0, '.')
        row.append('.')

    numbers = []

    # Store the positions of the numbers per row so that we can use that in second part
    # We will be storing the number, start and end index of the number in the row.
    # This will helps us know that if the number is adjacent to a star or not.
    number_positions = defaultdict(list)

    for ind, row in enumerate(grid[1:-1], start=1):
        col_index = 1
        for k, g in groupby(row[1:-1], key=str.isdigit):
            item = "".join(g)
            if k:
                if check_adjacent(start=col_index - 1, end=col_index + len(item) + 1, current_row=row, above_row=grid[ind-1], below_row=grid[ind + 1]):
                    numbers.append(int(item))
                    number_positions[ind].append((int(item), col_index, col_index + len(item) - 1))
            col_index += len(item)

    print(sum(numbers))

    # Part two
    total = 0
    for ind, row in enumerate(grid[1:-1], start=1):
        col_index = 1
        for k, g in groupby(row[1:-1], key=lambda x: x == "*"):
            if k:
                total += find_product_of_adjacent_numbers_to_a_star(grid=grid, number_positions=number_positions, star_index=col_index, current_row_index=ind, above_row_index=ind-1, below_row_index=ind+1)
                col_index += 1
            else:
                col_index += sum(1 for _ in g)

    print(total)


def find_product_of_adjacent_numbers_to_a_star(grid: List[List[str]], number_positions: Dict[int, List[Tuple[int, int, int]]], star_index: int, current_row_index: int, above_row_index: int, below_row_index: int):
    """Find the product of the adjacent numbers to a star.
    
    We need to check the numbers above, below and on the same row as the star.
    """

    # 467.114..
    # ...*......
    # ..35..633.
    # Imagine a case like above, here 467, 114 and 35 all are adjacent to the star.
    numbers_above_row = [(number, start, end) for number, start, end in number_positions[above_row_index] if start - 1 <= star_index <= end + 1]
    numbers_below_row = [(number, start, end) for number, start, end in number_positions[below_row_index] if start - 1 <= star_index <= end + 1]

    # If the adjacent numbers are on the same row as the stars then we need to check slightly differently: 617*123...
    numbers_current_row = [(number, start, end) for number, start, end in number_positions[current_row_index] if (start - 1 == star_index) or (end + 1 == star_index)]

    numbers = numbers_above_row + numbers_below_row + numbers_current_row

    if len(numbers) == 2:
        return numbers[0][0] * numbers[1][0]
    
    return 0

if __name__ == "__main__":
    solve_part_one_and_two()
