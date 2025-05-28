"""
Enhanced Task 4: Telemarketer Detection

This module provides an improved implementation for identifying potential
telemarketers based on call and text patterns.

A telemarketer is defined as a number that:
- Makes outgoing calls
- Never sends texts
- Never receives texts  
- Never receives incoming calls

Improvements:
- Type hints and proper documentation
- Set-based operations for better performance
- Modular design with clear separation of concerns
- Comprehensive error handling
- Performance analysis and testing
"""

import csv
from pathlib import Path
from typing import List, Set, Tuple


class TelemarketerDetector:
    """Detector for potential telemarketer phone numbers."""
    
    def __init__(self):
        self.outgoing_callers: Set[str] = set()
        self.incoming_receivers: Set[str] = set()
        self.text_senders: Set[str] = set()
        self.text_receivers: Set[str] = set()
    
    def process_call_record(self, caller: str, receiver: str) -> None:
        """
        Process a call record to track callers and receivers.
        
        Args:
            caller: Phone number making the call
            receiver: Phone number receiving the call
        """
        self.outgoing_callers.add(caller)
        self.incoming_receivers.add(receiver)
    
    def process_text_record(self, sender: str, receiver: str) -> None:
        """
        Process a text record to track senders and receivers.
        
        Args:
            sender: Phone number sending the text
            receiver: Phone number receiving the text
        """
        self.text_senders.add(sender)
        self.text_receivers.add(receiver)
    
    def get_legitimate_numbers(self) -> Set[str]:
        """
        Get all numbers that show legitimate user behavior.
        
        Returns:
            Set of phone numbers that are NOT potential telemarketers
        """
        return (self.incoming_receivers | 
                self.text_senders | 
                self.text_receivers)
    
    def get_potential_telemarketers(self) -> Set[str]:
        """
        Identify potential telemarketers using set operations.
        
        Returns:
            Set of phone numbers that could be telemarketers
        """
        legitimate_numbers = self.get_legitimate_numbers()
        return self.outgoing_callers - legitimate_numbers
    
    def get_statistics(self) -> dict:
        """
        Get statistics about the phone number analysis.
        
        Returns:
            Dictionary with various statistics
        """
        legitimate = self.get_legitimate_numbers()
        potential_telemarketers = self.get_potential_telemarketers()
        
        return {
            'total_outgoing_callers': len(self.outgoing_callers),
            'total_incoming_receivers': len(self.incoming_receivers),
            'total_text_senders': len(self.text_senders),
            'total_text_receivers': len(self.text_receivers),
            'total_legitimate_numbers': len(legitimate),
            'potential_telemarketers': len(potential_telemarketers),
            'telemarketer_percentage': (
                len(potential_telemarketers) * 100.0 / len(self.outgoing_callers)
                if self.outgoing_callers else 0.0
            )
        }


def read_csv_file(filepath: Path) -> List[List[str]]:
    """
    Read CSV file safely with proper error handling.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        List of rows from the CSV file
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            return list(reader)
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found: {filepath}")
    except Exception as e:
        raise Exception(f"Error reading CSV file {filepath}: {e}")


def detect_telemarketers(calls_filepath: str = 'calls.csv',
                        texts_filepath: str = 'texts.csv') -> Tuple[List[str], dict]:
    """
    Main function to detect potential telemarketers.
    
    Args:
        calls_filepath: Path to the calls CSV file
        texts_filepath: Path to the texts CSV file
        
    Returns:
        Tuple of (sorted_telemarketer_list, statistics)
    """
    # Initialize detector
    detector = TelemarketerDetector()
    
    # Try multiple possible locations for CSV files
    def try_load_csv(filename):
        possible_paths = [
            Path("sample_data") / filename,
            Path(filename),
            Path("..") / "sample_data" / filename
        ]
        
        for path in possible_paths:
            try:
                data = read_csv_file(path)
                print(f"Successfully loaded {filename} from: {path}")
                return data
            except FileNotFoundError:
                continue
        return None
      # Read and process call data
    calls_data = try_load_csv(calls_filepath)
    if calls_data:
        # Skip header row if present
        data_rows = calls_data[1:] if calls_data and 'calling number' in str(calls_data[0]) else calls_data
        for record in data_rows:
            if len(record) >= 2:  # Need at least caller and receiver
                caller, receiver = record[0], record[1]
                detector.process_call_record(caller, receiver)
    else:
        print(f"Warning: Could not process calls data: CSV file not found: {calls_filepath}")
    
    # Read and process text data
    texts_data = try_load_csv(texts_filepath)
    if texts_data:
        # Skip header row if present
        data_rows = texts_data[1:] if texts_data and 'sending number' in str(texts_data[0]) else texts_data
        for record in data_rows:
            if len(record) >= 2:  # Need at least sender and receiver
                sender, receiver = record[0], record[1]
                detector.process_text_record(sender, receiver)
    else:
        print(f"Warning: Could not process texts data: CSV file not found: {texts_filepath}")
    
    # Get results
    potential_telemarketers = detector.get_potential_telemarketers()
    statistics = detector.get_statistics()
    
    return sorted(potential_telemarketers), statistics


def print_telemarketer_results(telemarketers: List[str], statistics: dict) -> None:
    """
    Print the telemarketer detection results.
    
    Args:
        telemarketers: Sorted list of potential telemarketer numbers
        statistics: Dictionary with analysis statistics
    """
    print("These numbers could be telemarketers: ")
    for number in telemarketers:
        print(number)
    
    # Print statistics
    print(f"\nAnalysis Statistics:")
    print(f"Total outgoing callers: {statistics['total_outgoing_callers']}")
    print(f"Potential telemarketers: {statistics['potential_telemarketers']}")
    print(f"Telemarketer percentage: {statistics['telemarketer_percentage']:.2f}%")


def get_algorithm_complexity() -> str:
    """Return the time complexity analysis of the algorithm."""
    return """
    Time Complexity Analysis:
    - Reading calls CSV: O(c) where c is number of call records
    - Reading texts CSV: O(t) where t is number of text records
    - Processing records: O(c + t) for set operations
    - Set difference operation: O(n) where n is number of unique callers
    - Sorting results: O(k log k) where k is number of telemarketers
    - Overall: O(c + t + k log k)
    
    Space Complexity: O(n) where n is total number of unique phone numbers
    
    The algorithm is highly efficient using set operations for O(1) average
    case lookups and avoiding nested loops.
    """


def run_comprehensive_test() -> None:
    """Run comprehensive tests with sample data."""
    print("Testing TelemarketerDetector with sample data:")
    
    detector = TelemarketerDetector()
    
    # Sample call data: (caller, receiver)
    call_records = [
        ("1234567890", "0987654321"),  # 1234567890 calls someone
        ("1111111111", "2222222222"),  # 1111111111 calls someone
        ("3333333333", "1234567890"),  # Someone calls 1234567890
    ]
    
    # Sample text data: (sender, receiver)
    text_records = [
        ("0987654321", "5555555555"),  # 0987654321 sends text
        ("6666666666", "0987654321"),  # Someone texts 0987654321
    ]
    
    # Process records
    for caller, receiver in call_records:
        detector.process_call_record(caller, receiver)
    
    for sender, receiver in text_records:
        detector.process_text_record(sender, receiver)
    
    # Get results
    telemarketers = detector.get_potential_telemarketers()
    stats = detector.get_statistics()
    
    print(f"Potential telemarketers: {sorted(telemarketers)}")
    print(f"Expected: ['1111111111'] (only makes calls, no other activity)")
    print(f"Statistics: {stats}")


if __name__ == "__main__":
    try:
        # Run the main detection
        telemarketers, statistics = detect_telemarketers()
        print_telemarketer_results(telemarketers, statistics)
        
        print("\n" + "="*60)
        print("ALGORITHM COMPLEXITY ANALYSIS")
        print("="*60)
        print(get_algorithm_complexity())
        
        print("\n" + "="*60)
        print("COMPREHENSIVE TESTING")
        print("="*60)
        run_comprehensive_test()
        
    except Exception as e:
        print(f"Error: {e}")
