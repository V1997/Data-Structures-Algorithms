"""
Enhanced Task 2: Find telephone number with longest call duration

This module provides an improved implementation for finding the telephone number
that spent the longest time on the phone during September 2016.

Improvements:
- Type hints for better code clarity
- Proper error handling and validation
- More efficient data processing
- Better variable naming and documentation
- Configurable date filtering
"""

import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional


def read_csv_file(filepath: Path) -> List[List[str]]:
    """
    Read CSV file safely with proper error handling.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        List of rows from the CSV file
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        PermissionError: If the file can't be read
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            return list(reader)
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found: {filepath}")
    except PermissionError:
        raise PermissionError(f"Cannot read CSV file: {filepath}")


def parse_call_duration(calls_data: List[List[str]], 
                       year: int = 2016, 
                       month: int = 9) -> Dict[str, int]:
    """
    Parse call data and calculate total duration for each phone number.
    
    Args:
        calls_data: List of call records [caller, receiver, timestamp, duration]
        year: Year to filter calls (default: 2016)
        month: Month to filter calls (default: 9)
        
    Returns:
        Dictionary mapping phone numbers to total call duration
    """
    call_durations = defaultdict(int)
    
    # Skip header row if present
    data_rows = calls_data[1:] if calls_data and 'calling number' in str(calls_data[0]) else calls_data
    
    for record in data_rows:
        if len(record) != 4:
            continue  # Skip malformed records
            
        caller, receiver, timestamp, duration_str = record
        
        try:
            # Parse timestamp
            call_date = datetime.strptime(timestamp, "%d-%m-%Y %H:%M:%S")
            
            # Filter by date
            if call_date.year != year or call_date.month != month:
                continue
                
            # Parse duration
            duration = int(duration_str)
            
            # Add duration to both caller and receiver
            call_durations[caller] += duration
            call_durations[receiver] += duration
            
        except (ValueError, TypeError) as e:
            print(f"Warning: Skipping invalid record {record}: {e}")
            continue
    
    return call_durations


def find_longest_caller(call_durations: Dict[str, int]) -> Optional[Tuple[str, int]]:
    """
    Find the phone number with the longest total call duration.
    
    Args:
        call_durations: Dictionary mapping phone numbers to durations
        
    Returns:
        Tuple of (phone_number, duration) or None if no data
    """
    if not call_durations:
        return None
    
    return max(call_durations.items(), key=lambda x: x[1])


def analyze_call_data(calls_filepath: str = 'calls.csv',
                     year: int = 2016,
                     month: int = 9) -> None:
    """
    Main function to analyze call data and find longest caller.
    
    Args:
        calls_filepath: Path to the calls CSV file
        year: Year to filter calls
        month: Month to filter calls
    """
    try:
        # Try multiple possible locations for the CSV file
        possible_paths = [
            Path("sample_data") / calls_filepath,
            Path(calls_filepath),
            Path("..") / "sample_data" / calls_filepath
        ]
        
        calls_data = None
        used_path = None
        
        for path in possible_paths:
            try:
                calls_data = read_csv_file(path)
                used_path = path
                print(f"Successfully loaded calls data from: {path}")
                break
            except FileNotFoundError:
                continue
        
        if calls_data is None:
            print(f"Error analyzing call data: CSV file not found: {calls_filepath}")
            print("Please ensure calls.csv exists in the current directory or sample_data/ folder")
            return
        
        if not calls_data:
            print("No call data found.")
            return
        
        # Parse call durations
        call_durations = parse_call_duration(calls_data, year, month)
        
        if not call_durations:
            print(f"No calls found for {month:02d}/{year}")
            return
        
        # Find longest caller
        result = find_longest_caller(call_durations)
        
        if result:
            phone_number, duration = result
            print(f"{phone_number} spent the longest time, {duration} seconds, "
                  f"on the phone during {datetime(year, month, 1).strftime('%B %Y')}.")
            
            # Show additional statistics
            print(f"\nAdditional Statistics:")
            print(f"Total unique phone numbers: {len(call_durations)}")
            
            # Show top 5 phones by duration
            top_phones = sorted(call_durations.items(), key=lambda x: x[1], reverse=True)[:5]
            print(f"Top 5 phones by total call duration:")
            for i, (phone, dur) in enumerate(top_phones, 1):
                print(f"{i}. {phone}: {dur} seconds")
        else:
            print("No valid call data found.")
            
    except Exception as e:
        print(f"Error analyzing call data: {e}")


# Performance analysis
def get_algorithm_complexity() -> str:
    """Return the time complexity analysis of the algorithm."""
    return """
    Time Complexity Analysis:
    - Reading CSV file: O(n) where n is number of records
    - Processing records: O(n) for parsing and filtering
    - Finding maximum: O(m) where m is number of unique phone numbers
    - Overall: O(n) where n is the number of call records
    
    Space Complexity: O(m) where m is the number of unique phone numbers
    """


if __name__ == "__main__":
    # Run the analysis
    analyze_call_data()
    
    # Print complexity analysis
    print("\n" + "="*50)
    print(get_algorithm_complexity())
