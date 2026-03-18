from typing import Optional
from dataclasses import dataclass
from typing import Optional
from functools import lru_cache
import math
from pallet import Pallet, FloorUnit

# Given variables:
Trailer_Width = 96
Half_Width = 48

def single_unit(p: Pallet) -> FloorUnit:
    return FloorUnit(length=p.length, width=p.width)


def stacked_unit(a: Pallet, b: Pallet) -> FloorUnit:
    # Assumption: if two skids are stacked, the floor footprint is the larger
    # of the two in each dimension.
    return FloorUnit(
        length=max(a.length, b.length),
        width=max(a.width, b.width),
    )


def generate_floor_unit_sets(pallets):
    n = len(pallets)
    results = []

    def dfs(used_mask, current_units):
        if used_mask == (1 << n) - 1:
            results.append(tuple(current_units))
            return

        # Finding First unused pallet
        i = 0
        while used_mask & (1 << i):
            i += 1

        # Option 1: leave pallet i unstacked
        dfs(
            used_mask | (1 << i),
            current_units + [single_unit(pallets[i])]
        )

        # Option 2: stack pallet i with another unused stackable pallet j
        if pallets[i].stackable:
            for j in range(i + 1, n):
                if not (used_mask & (1 << j)) and pallets[j].stackable:
                    dfs(
                        used_mask | (1 << i) | (1 << j),
                        current_units + [stacked_unit(pallets[i], pallets[j])]
                    )

    dfs(0, [])
    return results


def min_billed_feet_for_units(units):
    m = len(units)

    def column_cost_twice(width_sum, max_length):
        # Return twice the billed inches to avoid floats.
        return max_length if width_sum <= Half_Width else 2 * max_length

    @lru_cache(None)
    def best(mask):
        if mask == 0:
            return 0

        # Find first remaining unit
        i = 0
        while not (mask & (1 << i)):
            i += 1

        candidates = [j for j in range(i + 1, m) if mask & (1 << j)]
        answer = float("inf")

        def build_columns(pos, subset_mask, width_sum, max_length):
            nonlocal answer

            # Current subset is a valid column
            cost = column_cost_twice(width_sum, max_length)
            answer = min(answer, cost + best(mask ^ subset_mask))

            # Try adding more units to this column
            for k in range(pos, len(candidates)):
                j = candidates[k]
                new_width = width_sum + units[j].width
                if new_width <= Trailer_Width:
                    build_columns(
                        k + 1,
                        subset_mask | (1 << j),
                        new_width,
                        max(max_length, units[j].length),
                    )

        # Start with unit i in the column
        build_columns(
            0,
            1 << i,
            units[i].width,
            units[i].length,
        )

        return answer

    twice_billed_inches = best((1 << m) - 1)
    billed_inches = twice_billed_inches / 2.0
    return math.ceil(billed_inches / 12.0)


def optimal_linear_feet(pallets):
    best_feet = float("inf")
    for units in generate_floor_unit_sets(pallets):
        best_feet = min(best_feet, min_billed_feet_for_units(units))
    return best_feet