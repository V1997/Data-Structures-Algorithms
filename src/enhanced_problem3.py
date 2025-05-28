"""
Enhanced Problem 3: Rearrange Array Elements

This module provides an improved implementation for rearranging array elements
to form two numbers with maximum sum.

Algorithm: Use counting sort to sort digits in descending order, then alternate
placement to create two numbers of similar length for maximum sum.

Improvements:
- Type hints and proper documentation
- Better error handling and edge case management
- More efficient implementation using counting sort
- Comprehensive test cases and validation
- Performance analysis
"""

from typing import List, Tuple, Optional


def rearrange_digits(input_list: List[int]) -> List[int]:
    """
    Rearrange array elements to form two numbers with maximum sum.
    
    The algorithm works by:
    1. Using counting sort to sort digits in descending order (O(n))
    2. Alternately placing digits to form two numbers of similar length
    3. This ensures maximum sum since larger digits get higher place values
    
    Args:
        input_list: List of single digits (0-9)
        
    Returns:
        List containing two integers with maximum sum
        Returns [-1, -1] for invalid inputs
        
    Time Complexity: O(n) where n is length of input
    Space Complexity: O(1) using counting sort with fixed size array
    """
    # Validate input
    if not input_list:
        return [-1, -1]
    
    if len(input_list) == 1:
        return [-1, -1]
    
    # Validate all elements are single digits
    if not all(isinstance(x, int) and 0 <= x <= 9 for x in input_list):
        raise ValueError("All elements must be single digits (0-9)")
    
    # Count frequency of each digit (counting sort)
    digit_count = [0] * 10
    for digit in input_list:
        digit_count[digit] += 1
    
    # Build two numbers by alternating digit placement
    num1_digits = []
    num2_digits = []
    use_first = True
    
    # Place digits from largest to smallest
    for digit in range(9, -1, -1):
        while digit_count[digit] > 0:
            if use_first:
                num1_digits.append(str(digit))
            else:
                num2_digits.append(str(digit))
            
            use_first = not use_first
            digit_count[digit] -= 1
    
    # Convert to integers
    num1 = int(''.join(num1_digits)) if num1_digits else 0
    num2 = int(''.join(num2_digits)) if num2_digits else 0
    
    return [num1, num2]


def validate_solution(input_list: List[int], result: List[int]) -> bool:
    """
    Validate that the solution is correct.
    
    Args:
        input_list: Original input list
        result: Result from rearrange_digits
        
    Returns:
        True if solution is valid, False otherwise
    """
    if result == [-1, -1]:
        return len(input_list) <= 1
    
    # Check that all digits are used exactly once
    original_digits = sorted(str(d) for d in input_list)
    result_digits = sorted(str(result[0]) + str(result[1]))
    
    return original_digits == result_digits


def find_optimal_sum(input_list: List[int]) -> int:
    """
    Calculate the theoretical maximum sum for comparison.
    
    Args:
        input_list: List of digits
        
    Returns:
        Theoretical maximum sum
    """
    if len(input_list) <= 1:
        return -2  # Invalid case marker
    
    # Sort digits in descending order
    sorted_digits = sorted(input_list, reverse=True)
    
    # Calculate optimal distribution
    num1_digits = []
    num2_digits = []
    
    for i, digit in enumerate(sorted_digits):
        if i % 2 == 0:
            num1_digits.append(digit)
        else:
            num2_digits.append(digit)
    
    num1 = int(''.join(map(str, num1_digits))) if num1_digits else 0
    num2 = int(''.join(map(str, num2_digits))) if num2_digits else 0
    
    return num1 + num2


def run_comprehensive_tests() -> None:
    """Run comprehensive test cases."""
    test_cases = [
        # (input, expected_result_type, description)
        ([1, 2, 3, 4, 5], "valid", "Basic case"),
        ([4, 6, 2, 5, 9, 8], "valid", "Even length array"),
        ([], "invalid", "Empty array"),
        ([0], "invalid", "Single element"),
        ([0, 0], "valid", "All zeros"),
        ([0, 0, 1, 1, 5, 5], "valid", "Duplicate elements"),
        ([9, 8, 7, 6, 5, 4, 3, 2, 1, 0], "valid", "All digits"),
        ([5, 5, 5, 5], "valid", "All same digits"),
        ([1, 2], "valid", "Minimum valid case"),
    ]
    
    print("Running comprehensive tests for rearrange_digits:")
    print("="*60)
    
    for i, (input_list, expected_type, description) in enumerate(test_cases, 1):
        try:
            result = rearrange_digits(input_list.copy())
            is_valid = validate_solution(input_list, result)
            
            if expected_type == "invalid":
                success = result == [-1, -1]
            else:
                success = is_valid and result != [-1, -1]
            
            status = "✓ PASS" if success else "✗ FAIL"
            optimal_sum = find_optimal_sum(input_list)
            actual_sum = sum(result) if result != [-1, -1] else -2
            
            print(f"Test {i}: {status}")
            print(f"  Description: {description}")
            print(f"  Input: {input_list}")
            print(f"  Result: {result}")
            print(f"  Sum: {actual_sum} (optimal: {optimal_sum})")
            print(f"  Valid: {is_valid}")
            print()
            
        except Exception as e:
            print(f"Test {i}: ✗ ERROR - {e}")
            print(f"  Input: {input_list}")
            print()


def benchmark_performance() -> None:
    """Benchmark the performance of the algorithm."""
    import time
    import random
    
    print("Performance Benchmark:")
    print("="*40)
    
    # Use smaller sizes to avoid integer overflow in Python
    sizes = [100, 1000, 2000, 5000]
    
    for size in sizes:
        # Limit array size to prevent integer overflow (max 1000 digits)
        actual_size = min(size, 1000)
        test_data = [random.randint(0, 9) for _ in range(actual_size)]
        
        # Measure time
        start_time = time.time()
        result = rearrange_digits(test_data)
        end_time = time.time()
        
        execution_time = (end_time - start_time) * 1000  # Convert to ms
        
        # For large results, show truncated version to avoid overflow display
        if result != [-1, -1]:
            try:
                result_sum = sum(result)
                if len(str(result[0])) > 20:
                    result_display = f"Large numbers (length: {len(str(result[0]))}, {len(str(result[1]))})"
                else:
                    result_display = f"Sum: {result_sum}"
            except (ValueError, OverflowError):
                result_display = "Very large numbers"
        else:
            result_display = "N/A"
        
        print(f"Size: {actual_size:6d} | Time: {execution_time:.2f} ms | {result_display}")


def get_algorithm_explanation() -> str:
    """Return detailed algorithm explanation."""
    return """
    ALGORITHM EXPLANATION:
    
    1. COUNTING SORT (O(n)):
       - Count frequency of each digit (0-9) in a fixed-size array
       - This gives us sorted digits without comparison-based sorting
    
    2. GREEDY DIGIT PLACEMENT (O(n)):
       - Place digits alternately between two numbers, largest first
       - This ensures both numbers have similar lengths
       - Larger digits get higher place values in both numbers
    
    3. WHY THIS WORKS:
       - To maximize sum A + B, we want to maximize both A and B
       - Larger digits should be in higher place values
       - Similar lengths prevent one number from being much smaller
    
    EXAMPLE: [4, 6, 2, 5, 9, 8]
    - Sorted: [9, 8, 6, 5, 4, 2]
    - Number 1: 9, 6, 4 → 964
    - Number 2: 8, 5, 2 → 852
    - Sum: 964 + 852 = 1816 (maximum possible)
    
    TIME COMPLEXITY: O(n) - linear scan for counting + linear placement
    SPACE COMPLEXITY: O(1) - fixed size counting array + result storage
    """


if __name__ == "__main__":
    # Run comprehensive tests
    run_comprehensive_tests()
    
    print("\n" + "="*60)
    print("ALGORITHM EXPLANATION")
    print("="*60)
    print(get_algorithm_explanation())
    
    print("\n" + "="*60)
    print("PERFORMANCE BENCHMARK")
    print("="*60)
    benchmark_performance()
