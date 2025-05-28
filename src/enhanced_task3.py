"""
Enhanced Task 3: Bangalore Area Code Analysis

This module provides an improved implementation for analyzing calls from
Bangalore fixed lines to identify area codes and calculate call percentages.

Improvements:
- Type hints and proper error handling
- Regular expressions for robust phone number parsing
- Modular design with clear separation of concerns
- Better documentation and code organization
- Comprehensive test cases
"""

import csv
import re
from pathlib import Path
from typing import List, Optional, Set, Tuple


class PhoneNumberAnalyzer:
    """Analyzer for phone number patterns and area codes."""

    # Regular expressions for different phone number types
    FIXED_LINE_PATTERN = re.compile(r"^\((\d+)\)")
    MOBILE_PATTERN = re.compile(r"^([789]\d{3})\s\d{6}$")
    TELEMARKETER_PATTERN = re.compile(r"^140")
    BANGALORE_PREFIX = "(080)"

    def __init__(self) -> None:
        self.bangalore_calls: List[Tuple[str, str]] = []
        self.called_codes: Set[str] = set()
        self.bangalore_to_bangalore_count = 0
        self.total_bangalore_calls = 0

    def classify_phone_number(self, number: str) -> Optional[str]:
        """
        Classify a phone number and extract its code/prefix.

        Args:
            number: Phone number string

        Returns:
            Area code or prefix, or None if unrecognized
        """
        # Fixed line (area code in parentheses)
        fixed_match = self.FIXED_LINE_PATTERN.match(number)
        if fixed_match:
            return f"({fixed_match.group(1)})"

        # Telemarketer (starts with 140)
        if self.TELEMARKETER_PATTERN.match(number):
            return "140"

        # Mobile (7/8/9 followed by space)
        mobile_match = self.MOBILE_PATTERN.match(number)
        if mobile_match:
            return mobile_match.group(1)

        # Fallback: extract first 4 digits for mobile-like numbers
        if len(number) >= 4 and number[0] in "789":
            return number[:4]

        return None

    def is_bangalore_number(self, number: str) -> bool:
        """Check if a number is from Bangalore (080 area code)."""
        return number.startswith(self.BANGALORE_PREFIX)

    def process_call_record(self, caller: str, receiver: str) -> None:
        """
        Process a single call record if caller is from Bangalore.

        Args:
            caller: Caller's phone number
            receiver: Receiver's phone number
        """
        if not self.is_bangalore_number(caller):
            return

        self.total_bangalore_calls += 1

        # Extract receiver's code
        receiver_code = self.classify_phone_number(receiver)
        if receiver_code:
            self.called_codes.add(receiver_code)

            # Check if call is to another Bangalore number
            if receiver_code == self.BANGALORE_PREFIX:
                self.bangalore_to_bangalore_count += 1

    def get_called_codes_sorted(self) -> List[str]:
        """Get sorted list of all area codes called from Bangalore."""
        return sorted(self.called_codes)

    def get_bangalore_call_percentage(self) -> float:
        """Calculate percentage of Bangalore-to-Bangalore calls."""
        if self.total_bangalore_calls == 0:
            return 0.0
        return (self.bangalore_to_bangalore_count * 100.0) / self.total_bangalore_calls


def read_csv_data(filepath: Path) -> List[List[str]]:
    """
    Read CSV file safely with proper error handling.

    Args:
        filepath: Path to the CSV file

    Returns:
        List of rows from the CSV file
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            return list(reader)
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found: {filepath}")
    except Exception as e:
        raise Exception(f"Error reading CSV file {filepath}: {e}")


def analyze_bangalore_calls(
    calls_filepath: str = "calls.csv",
) -> Tuple[List[str], float]:
    """
    Analyze calls from Bangalore to find area codes and calculate percentages.

    Args:
        calls_filepath: Path to the calls CSV file

    Returns:
        Tuple of (sorted_area_codes, bangalore_percentage)
    """
    # Try multiple possible locations for the CSV file
    possible_paths = [
        Path("sample_data") / calls_filepath,
        Path(calls_filepath),
        Path("..") / "sample_data" / calls_filepath,
    ]

    calls_data = None

    for path in possible_paths:
        try:
            calls_data = read_csv_data(path)
            print(f"Successfully loaded calls data from: {path}")
            break
        except FileNotFoundError:
            continue

    if calls_data is None:
        raise FileNotFoundError(f"CSV file not found: {calls_filepath}")

    if not calls_data:
        return [], 0.0
    # Initialize analyzer
    analyzer = PhoneNumberAnalyzer()

    # Skip header row if present
    data_rows = (
        calls_data[1:]
        if calls_data and "calling number" in str(calls_data[0])
        else calls_data
    )

    # Process each call record
    for record in data_rows:
        if len(record) >= 2:  # Need at least caller and receiver
            caller, receiver = record[0], record[1]
            analyzer.process_call_record(caller, receiver)

    # Get results
    called_codes = analyzer.get_called_codes_sorted()
    bangalore_percentage = analyzer.get_bangalore_call_percentage()

    return called_codes, bangalore_percentage


def print_analysis_results(
    called_codes: List[str], bangalore_percentage: float
) -> None:
    """
    Print the analysis results in the required format.

    Args:
        called_codes: Sorted list of area codes
        bangalore_percentage: Percentage of Bangalore-to-Bangalore calls
    """
    # Part A: Print area codes
    print("The numbers called by people in Bangalore have codes:")
    for code in called_codes:
        print(code)

    # Part B: Print percentage
    print(
        f"{bangalore_percentage:.2f} percent of calls from fixed lines in Bangalore "
        f"are calls to other fixed lines in Bangalore."
    )


def get_algorithm_complexity() -> str:
    """Return the time complexity analysis of the algorithm."""
    return """
    Time Complexity Analysis:
    - Reading CSV file: O(n) where n is number of call records
    - Processing records: O(n) for classification and analysis
    - Sorting area codes: O(k log k) where k is number of unique codes
    - Overall: O(n + k log k) where n >> k in typical cases

    Space Complexity: O(k) where k is the number of unique area codes

    The algorithm is efficient for large datasets as it processes each
    record only once and uses sets for deduplication.
    """


def run_comprehensive_test() -> None:
    """Run comprehensive tests with sample data."""
    analyzer = PhoneNumberAnalyzer()

    # Test phone number classification
    test_cases = [
        ("(080)12345678", "(080)"),
        ("(022)87654321", "(022)"),
        ("9876 543210", "9876"),
        ("8123 456789", "8123"),
        ("7890123456", "7890"),
        ("14012345678", "140"),
        ("1234567890", "1234"),  # Fallback case
    ]

    print("Testing phone number classification:")
    for number, expected in test_cases:
        result = analyzer.classify_phone_number(number)
        status = "✓" if result == expected else "✗"
        print(f"{status} {number} -> {result} (expected: {expected})")


if __name__ == "__main__":
    try:
        # Run the main analysis
        called_codes, bangalore_percentage = analyze_bangalore_calls()
        print_analysis_results(called_codes, bangalore_percentage)

        print("\n" + "=" * 60)
        print("ALGORITHM COMPLEXITY ANALYSIS")
        print("=" * 60)
        print(get_algorithm_complexity())

        print("\n" + "=" * 60)
        print("COMPREHENSIVE TESTING")
        print("=" * 60)
        run_comprehensive_test()

    except Exception as e:
        print(f"Error: {e}")
