from typing import List

from anchor import interval


def analyze_canonical_interval_structure(anchor_intervals_played: List[int]):
    if anchor_intervals_played:
        lowest_interval = min(anchor_intervals_played)
        return [interval.get_anchor_interval_representative(anchor_interval - lowest_interval) for anchor_interval in anchor_intervals_played]
    else:
        return []


def analyze_relative_anchor_interval_structure(anchor_intervals):
    relative_anchor_intervals_to_frequency = {}
    num_anchor_intervals = len(anchor_intervals)
    for i in range(num_anchor_intervals):
        for j in range(i + 1, num_anchor_intervals):
            first_interval, second_interval = anchor_intervals[i], anchor_intervals[j]
            relative_interval = interval.get_anchor_interval_representative(second_interval - first_interval)
            if relative_interval not in relative_anchor_intervals_to_frequency:
                relative_anchor_intervals_to_frequency[relative_interval] = 0
            relative_anchor_intervals_to_frequency[relative_interval] += 1
    return relative_anchor_intervals_to_frequency




