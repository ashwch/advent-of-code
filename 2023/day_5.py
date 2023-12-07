"""
URL: https://adventofcode.com/2023/day/5

--- Day 5: If You Give A Seed A Fertilizer ---

You take the boat and find the gardener right where you were told he would be: managing a giant "garden" that looks more to you like a farm.

"A water source? Island Island is the water source!" You point out that Snow Island isn't receiving any water.

"Oh, we had to stop the water because we ran out of sand to filter it with! Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand soon; we only turned off the water a few days... weeks... oh no." His face sinks into a look of horrified realization.

"I've been so busy making sure everyone here has food that I completely forgot to check why we stopped getting more sand! There's a ferry leaving soon that is headed over in that direction - it's much faster than your boat. Could you please go check it out?"

You barely have time to agree to this request when he brings up another. "While you wait for the ferry, maybe you can help us with our food production problem. The latest Island Island Almanac just arrived and we're having trouble making sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be k,ed. It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:

seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4

The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert a seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by one, the maps describe entire ranges of numbers that can be converted. Each line within a map contains three numbers: the destination range start, the source range start, and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48

The first line has a destination range start of 50, a source range start of 98, and a range length of 2. This line means that the source range starts at 98 and contains two values: 98 and 99. The destination range is the same length, but it starts at 50, so its two values are 50 and 51. With this information, you know that seed number 98 corresponds to soil number 50 and that seed number 99 corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51

With this map, you can look up the soil number required for each initial seed number:

    Seed number 79 corresponds to soil number 81.
    Seed number 14 corresponds to soil number 14.
    Seed number 55 corresponds to soil number 57.
    Seed number 13 corresponds to soil number 13.

The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do this, you'll need to convert each seed number through other categories until you can find its corresponding location number. In this example, the corresponding types are:

    Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
    Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
    Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
    Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.

So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?
"""

from calendar import c
from io import TextIOWrapper
from itertools import groupby
from operator import ge
from typing import Dict, Iterable, List, Tuple, NamedTuple

from utils import get_input

_print = print
print = lambda *args, **kwargs: None


class XtoYMapInfo(NamedTuple):
    destination_start: int
    source_start: int
    range: int


def parse_map(lines: Iterable[str]) -> Dict[int, int]:
    """Parse lines of input containing maps"""
    # print(f"Processing map: {lines[0]}")
    ranges = []

    for line in lines[1:]:
        destination_start, source_start, _range = map(int, line.split())
        ranges.append(XtoYMapInfo(destination_start, source_start, _range))

    return ranges

_T = (XtoYMapInfo, XtoYMapInfo, XtoYMapInfo, XtoYMapInfo, XtoYMapInfo, XtoYMapInfo, XtoYMapInfo)

def parse_input_part_one(input_file: TextIOWrapper) -> Tuple[List[int], *_T]:
    """Parse lines of input into maps"""
    seeds = [int(x) for x in next(input_file).split(": ")[1].split()]
    next(input_file)

    ranges = []
    for group in input_file.read().split("\n\n"):
        lines = group.splitlines()
        ranges.append(parse_map(lines))

    return seeds, *ranges


def parse_input_part_two(input_file: TextIOWrapper) -> Tuple[List[int], *_T]:
    numbers = [int(x) for x in next(input_file).split(": ")[1].split()]
    starts, ranges = numbers[::2], numbers[1::2]
    seed_ranges = []
    for start, _range in zip(starts, ranges):
        seed_ranges.append((start, start + _range))

    next(input_file)
    ranges = []
    for group in input_file.read().split("\n\n"):
        lines = group.splitlines()
        ranges.append(parse_map(lines))

    return seed_ranges, *ranges


def solve_part_one(lines: Iterable[str]) -> int:
    """Solve part one"""
    seeds, *ranges = parse_input_part_one (lines)
    min_distance = float("inf")

    for seed in seeds:
        key = seed
        for _ranges in ranges:
            for _range in _ranges:
                if _range.source_start <= key < _range.source_start + _range.range:
                    key = _range.destination_start + (key - _range.source_start)
                    break
        
        min_distance = min(min_distance, key)
    
    return min_distance


def solve_part_two(lines: Iterable[str]) -> int:
    """Solve part two"""
    seed_ranges, *ranges = parse_input_part_two(lines)

    # This ones' a doozy!!
    # Give the input is in millions and billions in terms of range in part 2,
    # the brute-force solution will take a long time. Probably not so long with PyPy :-)

    # A great explanation of the solution can be found here: https://youtu.be/NmxHw_bHhGM?si=1BL08HGMD1OWvTiR

    # This is my implementation and explanation based on the excellent video above

    # The way to understand this is:
    # For every range we try to break down the seed range into further ranges.
    # seed-to-soil map(or map-ranges) will give us the initial breakdown of the seed ranges. This new breakdown maps to the destination range
    # provided in the map.
    # The new seed ranges are then further broken down by the soil-to-fertilizer map and so on.
    # Eventually we'll end up with a seed range that maps to a location range and the minimum of that location range is the answer.

    # How the seed range breakdown happens for every map-range is as follows:
    # 1. The part before the overlap(from seed start)
    # 2. The part that overlaps (this is the part we're interested in and is mapped to the destination range)
    # 3. The part after the overlap(till seed end)

    # The part that overlaps includes the range from the destinations start to the destinations start + the range of the map-range
    # as that's because that's where we actually have a match
    # The part before(1) and after the overlap(3) are the parts that don't match YET, but they might match with another map-range

    # https://i.imgur.com/9Dhssos.jpg

    for _ranges in ranges:
        new_seed_ranges = []
        while len(seed_ranges) > 0:
            seed_start, seed_end = seed_ranges.pop(0)

            for _range in _ranges:
                print(_range)
                _range_destination_start, _range_source_start, _range_range = _range
                overlap_start = max(seed_start, _range_source_start)
                overlap_end = min(seed_end, _range_source_start + _range_range)

                print(
                    f"Seed range: {seed_start} - {seed_end}, "
                    f"Map range: {_range_source_start} - {_range_source_start + _range_range}, "
                    f"Overlap: {overlap_start} - {overlap_end}",
                    end=" --> "
                )

                if overlap_start < overlap_end:
                    new_seed_ranges.append((overlap_start - _range_source_start + _range_destination_start, overlap_end - _range_source_start + _range_destination_start))
                    if overlap_start > seed_start:
                        new_seed_ranges.append((seed_start, overlap_start))
                    if overlap_end < seed_end:
                        new_seed_ranges.append((overlap_end, seed_end))
                    
                    print("Overlap")
                    break
                else:
                    print("No overlap in this range")

            else:
                print("No overlap in any range")
                new_seed_ranges.append((seed_start, seed_end))

            print("New seed ranges", new_seed_ranges)
            print()
        print(f"End of map {_ranges}.")
        print(f"New seed ranges: {new_seed_ranges}")
        seed_ranges = new_seed_ranges
        print("-" * 20)
        print()

    print(sorted(seed_ranges))
    _print(min(seed_ranges)[0])


if __name__ == "__main__":
    input_file = get_input(5, iterator=True)
    print(solve_part_one(input_file))
    input_file = get_input(5, iterator=True)
    print(solve_part_two(input_file))
