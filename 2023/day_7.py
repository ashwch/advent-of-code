"""
URL: https://adventofcode.com/2023/day/7

--- Day 7: Camel Cards ---

Your all-expenses-paid trip turns out to be a one-way, five-minute ride in an airship. (At least it's a cool airship!) It drops you off at the edge of a vast desert and descends back to Island Island.

"Did you bring the parts?"

You turn around to see an Elf completely covered in white clothing, wearing goggles, and riding a large camel.

"Did you bring the parts?" she asks again, louder this time. You aren't sure what parts she's looking for; you're here to figure out why the sand stopped.

"The parts! For the sand, yes! Come with me; I will show you." She beckons you onto the camel.

After riding a bit across the sands of Desert Island, you can see what look like very large rocks covering half of the horizon. The Elf explains that the rocks are all along the part of Desert Island that is directly above Island Island, making it hard to even get there. Normally, they use big machines to move the rocks and filter the sand, but the machines have broken down because Desert Island recently stopped receiving the parts they need to fix the machines.

You've already assumed it'll be your job to figure out why the parts stopped when she asks if you can help. You agree automatically.

Because the journey will take a few days, she offers to teach you the game of Camel Cards. Camel Cards is sort of similar to poker except it's designed to be easier to play while riding a camel.

In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

Every hand is exactly one type. From strongest to weakest, they are:

    Five of a kind, where all five cards have the same label: AAAAA
    Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    High card, where all cards' labels are distinct: 23456

Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.

If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand. If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.

So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have the same first and second card).

To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input). For example:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483

This example shows five hands; each hand is followed by its bid amount. Each hand wins an amount equal to its bid multiplied by its rank, where the weakest hand gets rank 1, the second-weakest hand gets rank 2, and so on up to the strongest hand. Because there are five hands in this example, the strongest hand will have rank 5 and its bid will be multiplied by 5.

So, the first step is to put the hands in order of strength:

    32T3K is the only one pair and the other hands are all a stronger type, so it gets rank 1.
    KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
    T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4.

Now, you can determine the total winnings of this set of hands by adding up the result of multiplying each hand's bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example are 6440.

Find the rank of every hand in your set. What are the total winnings?

--- Part Two ---

To make things a little more interesting, the Elf introduces one additional rule. Now, J cards are jokers - wildcards that can act like whatever card would make the hand the strongest type possible.

To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

J cards can pretend to be whatever card is best for the purpose of determining hand type; for example, QJJQ2 is now considered four of a kind. However, for the purpose of breaking ties between two hands of the same type, J is always treated as J, not the card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

Now, the above example goes very differently:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483

    32T3K is still the only one pair; it doesn't contain any jokers, so its strength doesn't increase.
    KK677 is now the only two pair, making it the second-weakest hand.
    T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3, QQQJA gets rank 4, and KTJJT gets rank 5.

With the new joker rule, the total winnings in this example are 5905.

Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?

"""

from collections import Counter
from functools import partial

from utils import get_input

HANDS = "AKQJT98765432"[::-1]

HANDS_PART_TWO = "AKQT98765432J"[::-1]


def is_five_of_a_kind(hand: str) -> bool:
    """Return True if the hand is five of a kind."""
    return len(set(hand)) == 1

def is_four_of_a_kind(hand: str) -> bool:
    """Return True if the hand is four of a kind."""
    items = list(set(hand))
    counts = Counter(hand)
    return len(items) == 2 and any(counts[item] == 4 for item in items)


def is_full_house(hand: str) -> bool:
    """Return True if the hand is a full house."""
    items = list(set(hand))
    counts = Counter(hand)
    return len(items) == 2 and any(counts[item] == 3 for item in items)


def is_three_of_a_kind(hand: str) -> bool:
    """Return True if the hand is three of a kind."""
    items = list(set(hand))
    counts = Counter(hand)
    return len(items) == 3 and any(counts[item] == 3 for item in items)


def is_two_pair(hand: str) -> bool:
    """Return True if the hand is two pair."""
    items = list(set(hand))
    counts = Counter(hand)
    return len(items) == 3 and sum(counts[item] == 2 for item in items) == 2


def is_one_pair(hand: str) -> bool:
    """Return True if the hand is one pair."""
    items = list(set(hand))
    counts = Counter(hand)
    return len(items) == 4 and sum(counts[item] == 2 for item in items) == 1


def is_high_card(hand: str) -> bool:
    """Return True if the hand is a high card."""
    return len(set(hand)) == 5


def parse_input(data: list[str]) -> tuple[list[str], list[int]]:
    """Parse the input data."""
    hands = []
    bids = []
    for line in data:
        hand, bid = line.split()
        hands.append(hand)
        bids.append(int(bid))
    return hands, bids


def get_hand_rank(hand: str, substitute_joker: bool = False) -> int:
    """Return the rank of the given hand."""
    
    if is_five_of_a_kind(hand):
        rank = 7
    elif is_four_of_a_kind(hand):
        rank = 6
    elif is_full_house(hand):
        rank = 5
    elif is_three_of_a_kind(hand):
        rank = 4
    elif is_two_pair(hand):
        rank = 3
    elif is_one_pair(hand):
        rank = 2
    elif is_high_card(hand):
        rank = 1

    if substitute_joker and "J" in hand and rank != 7:
        # four of a kind
        if rank == 6:
            # AA8AA -> JJ8AA OR AAjAA
            # In either case this can be promoted to a five of a kind
            return 7
        # full house
        if rank == 5:
            # 23332 -> 2JJJ2 OR J333J
            # In either case this can be promoted to a five of a kind
            return 7
        # three of a kind
        if rank == 4:
            # TTT98 -> JJJ98 OR TTTJK OR TTTKJ
            # In either case this can be promoted to a four of a kind
            return 6
        # two pair
        if rank == 3:
            # 23432 -> J343J OR 2J4J2 OR 23J32
            #          33433    22422    23332
            # In either case this can be promoted to a four of a kind
            j_count = hand.count("J")
            if j_count == 2:
                return 6
            return 5
        
        # one pair
        if rank == 2:
            # A23A4 -> J23J4 OR AJ3A4 OR A2JA4 OR A23AJ
            # In either case this can be promoted to a three of a kind
            return 4
        # high card
        if rank == 1:
            # 23456 -> J3456 OR 2J456 OR 23J56 OR 234J6 OR 2345J
            # In either case this can be promoted to a one pair
            return 2

    return rank

def solve_part_one(data):
    """Solve part one."""
    hands, bids = parse_input(data)
    hands_bids_ranked = list(zip(hands, bids))

    hands_bids_ranked.sort(key=lambda x: (get_hand_rank(x[0]), [HANDS.index(item) for item in x[0]]), reverse=True)

    amount = 0

    total_hands = len(hands_bids_ranked)

    for i, (_, bid) in enumerate(hands_bids_ranked):
        amount += bid * (total_hands - i)

    return amount


part_two_get_hand_rank = partial(get_hand_rank, substitute_joker=True)


def solve_part_two(data):
    """Solve part two."""
    hands, bids = parse_input(data)
    hands_bids_ranked = list(zip(hands, bids))

    hands_bids_ranked.sort(key=lambda x: (part_two_get_hand_rank(x[0]), [HANDS_PART_TWO.index(item) for item in x[0]]), reverse=True)

    amount = 0

    total_hands = len(hands_bids_ranked)

    for i, (_, bid) in enumerate(hands_bids_ranked):
        amount += bid * (total_hands - i)

    return amount


if __name__ == "__main__":
    data = get_input(7).splitlines()
    print(solve_part_one(data))
    print(solve_part_two(data))
