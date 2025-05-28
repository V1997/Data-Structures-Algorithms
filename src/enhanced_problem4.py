"""
Enhanced Problem 4: Dutch National Flag Problem (Sort 012)

This module provides improved implementations for sorting an array containing
only 0s, 1s, and 2s in a single traversal.

Implements the Dutch National Flag algorithm by Edsger Dijkstra for optimal
O(n) time complexity with O(1) space complexity.

Improvements:
- Multiple algorithm implementations (counting sort vs. three-way partitioning)
- Proper in-place sorting (original was creating new array)
- Type hints and comprehensive documentation
- Extensive test cases and performance analysis
- Error handling and input validation
"""

import random
import time
from typing import List


def sort_012_counting(input_list: List[int]) -> List[int]:
    """
    Sort array of 0s, 1s, and 2s using counting sort.

    This was the approach used in the original implementation.
    Simple but creates a new array instead of in-place sorting.

    Args:
        input_list: List containing only 0s, 1s, and 2s

    Returns:
        New sorted list

    Time Complexity: O(n)
    Space Complexity: O(1) for counting array + O(n) for result
    """
    if not input_list:
        return []

    # Validate input
    if not all(x in [0, 1, 2] for x in input_list):
        raise ValueError("Array must contain only 0s, 1s, and 2s")

    # Count occurrences
    count = [0, 0, 0]
    for num in input_list:
        count[num] += 1

    # Build result array
    result = []
    for value in range(3):
        result.extend([value] * count[value])

    return result


def sort_012_inplace(input_list: List[int]) -> None:
    """
    Sort array of 0s, 1s, and 2s in-place using Dutch National Flag algorithm.

    This is the optimal solution using three-way partitioning:
    - Keep track of three regions: [0s][1s][2s]
    - Use three pointers: low (end of 0s), mid (current), high (start of 2s)

    Args:
        input_list: List to sort in-place (modified)

    Time Complexity: O(n) - single pass
    Space Complexity: O(1) - only uses pointer variables
    """
    if not input_list:
        return

    # Validate input
    if not all(x in [0, 1, 2] for x in input_list):
        raise ValueError("Array must contain only 0s, 1s, and 2s")

    low = 0  # End of 0s region
    mid = 0  # Current element being examined
    high = len(input_list) - 1  # Start of 2s region

    while mid <= high:
        if input_list[mid] == 0:
            # Move 0 to the left region
            input_list[low], input_list[mid] = input_list[mid], input_list[low]
            low += 1
            mid += 1
        elif input_list[mid] == 1:
            # 1 is already in correct position
            mid += 1
        else:  # input_list[mid] == 2
            # Move 2 to the right region
            input_list[mid], input_list[high] = input_list[high], input_list[mid]
            high -= 1
            # Don't increment mid as we need to examine the swapped element


def sort_012_functional(input_list: List[int]) -> List[int]:
    """
    Functional version that returns sorted copy without modifying original.

    Args:
        input_list: List containing only 0s, 1s, and 2s

    Returns:
        New sorted list
    """
    result = input_list.copy()
    sort_012_inplace(result)
    return result


class Sort012Analyzer:
    """Analyzer for different sorting approaches."""

    @staticmethod
    def validate_result(original: List[int], sorted_list: List[int]) -> bool:
        """
        Validate that sorting was performed correctly.

        Args:
            original: Original input list
            sorted_list: Sorted result

        Returns:
            True if result is valid
        """
        # Check length
        if len(original) != len(sorted_list):
            return False

        # Check sorted order
        if sorted_list != sorted(sorted_list):
            return False

        # Check same elements (count each value)
        for value in [0, 1, 2]:
            if original.count(value) != sorted_list.count(value):
                return False

        return True

    @staticmethod
    def generate_test_data(size: int, seed: int = 42) -> List[int]:
        """Generate random test data."""
        random.seed(seed)
        return [random.randint(0, 2) for _ in range(size)]

    @staticmethod
    def benchmark_algorithms(sizes: List[int]) -> None:
        """Benchmark different sorting approaches."""
        print("Performance Comparison:")
        print("=" * 70)
        print(
            f"{'Size':<8} {'Counting':<12} {'In-place':<12} "
            f"{'Functional':<12} {'Speedup':<10}"
        )
        print("-" * 70)

        for size in sizes:
            test_data = Sort012Analyzer.generate_test_data(size)

            # Benchmark counting sort
            data_copy = test_data.copy()
            start_time = time.time()
            sort_012_counting(data_copy)
            counting_time = time.time() - start_time

            # Benchmark in-place sort
            data_copy = test_data.copy()
            start_time = time.time()
            sort_012_inplace(data_copy)
            inplace_time = time.time() - start_time

            # Benchmark functional sort
            data_copy = test_data.copy()
            start_time = time.time()
            sort_012_functional(data_copy)
            functional_time = time.time() - start_time

            speedup = counting_time / inplace_time if inplace_time > 0 else float("inf")

            print(
                f"{size:<8} {counting_time*1000:<12.3f} {inplace_time*1000:<12.3f} "
                f"{functional_time*1000:<12.3f} {speedup:<10.2f}x"
            )


def run_comprehensive_tests() -> None:
    """Run comprehensive test cases for all sorting methods."""
    test_cases = [
        # (input, description)
        ([0, 0, 2, 2, 2, 1, 1, 1, 2, 0, 2], "Standard mixed case"),
        ([], "Empty array"),
        ([2, 1, 0], "Reverse order"),
        ([0, 0, 0], "All zeros"),
        ([1, 1, 1], "All ones"),
        ([2, 2, 2], "All twos"),
        ([0, 1, 2], "Already sorted"),
        (
            [
                2,
                1,
                2,
                0,
                0,
                2,
                1,
                0,
                1,
                0,
                0,
                2,
                2,
                2,
                1,
                2,
                0,
                0,
                0,
                2,
                1,
                0,
                2,
                0,
                0,
                1,
            ],
            "Long array",
        ),
        ([0], "Single element 0"),
        ([1], "Single element 1"),
        ([2], "Single element 2"),
        ([1, 0, 2, 1, 0, 2], "Alternating pattern"),
    ]

    print("Comprehensive Testing:")
    print("=" * 80)

    analyzer = Sort012Analyzer()

    for i, (test_input, description) in enumerate(test_cases, 1):
        print(f"\nTest {i}: {description}")
        print(f"Input:  {test_input}")

        # Test counting sort
        try:
            result_counting = sort_012_counting(test_input.copy())
            valid_counting = analyzer.validate_result(test_input, result_counting)
            print(f"Counting: {result_counting} {'✓' if valid_counting else '✗'}")
        except Exception as e:
            print(f"Counting: ERROR - {e}")

        # Test in-place sort
        try:
            test_copy = test_input.copy()
            sort_012_inplace(test_copy)
            valid_inplace = analyzer.validate_result(test_input, test_copy)
            print(f"In-place: {test_copy} {'✓' if valid_inplace else '✗'}")
        except Exception as e:
            print(f"In-place: ERROR - {e}")

        # Test functional sort
        try:
            result_functional = sort_012_functional(test_input.copy())
            valid_functional = analyzer.validate_result(test_input, result_functional)
            print(f"Functional: {result_functional} {'✓' if valid_functional else '✗'}")
        except Exception as e:
            print(f"Functional: ERROR - {e}")


def get_algorithm_explanation() -> str:
    """Return detailed explanation of the Dutch National Flag algorithm."""
    return """
    DUTCH NATIONAL FLAG ALGORITHM (Edsger Dijkstra):

    CONCEPT:
    Partition array into three regions: [0s | 1s | 2s]
    Use three pointers to maintain these regions:

    low:  End of 0s region (everything before low is 0)
    mid:  Current element being examined
    high: Start of 2s region (everything after high is 2)

    ALGORITHM:
    1. Initialize: low = 0, mid = 0, high = n-1
    2. While mid <= high:
       - If arr[mid] == 0: swap with arr[low], increment both low and mid
       - If arr[mid] == 1: just increment mid (already in correct region)
       - If arr[mid] == 2: swap with arr[high], decrement high (don't increment mid!)

    WHY DON'T WE INCREMENT MID WHEN SWAPPING WITH HIGH?
    Because the element we just swapped from high position hasn't been examined yet!

    EXAMPLE: [2, 0, 1, 2, 1, 0]
    Initial: low=0, mid=0, high=5

    Step 1: arr[0]=2, swap with arr[5]=0 → [0, 0, 1, 2, 1, 2], high=4
    Step 2: arr[0]=0, swap with arr[0]=0 → [0, 0, 1, 2, 1, 2], low=1, mid=1
    Step 3: arr[1]=0, swap with arr[1]=0 → [0, 0, 1, 2, 1, 2], low=2, mid=2
    Step 4: arr[2]=1, increment mid → mid=3
    Step 5: arr[3]=2, swap with arr[4]=1 → [0, 0, 1, 1, 2, 2], high=3
    Step 6: mid > high, done!

    COMPLEXITY:
    Time: O(n) - each element examined at most once
    Space: O(1) - only uses a few pointer variables
    """


if __name__ == "__main__":
    # Run comprehensive tests
    run_comprehensive_tests()

    print("\n" + "=" * 80)
    print("ALGORITHM EXPLANATION")
    print("=" * 80)
    print(get_algorithm_explanation())

    print("\n" + "=" * 80)
    print("PERFORMANCE ANALYSIS")
    print("=" * 80)
    Sort012Analyzer.benchmark_algorithms([100, 1000, 10000, 100000])
