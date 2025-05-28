"""
Comprehensive Test Suite for Data Structures & Algorithms
=========================================================

Test cases covering:
- LRU Cache implementation
- File search functionality
- Square root algorithm
- Edge cases and error conditions
"""

import pytest
import os
import tempfile
import shutil
from pathlib import Path
import sys

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from enhanced_lru_cache import LRUCache
from enhanced_file_finder import FileSearcher
from enhanced_task2 import parse_call_duration, find_longest_caller
from enhanced_task3 import PhoneNumberAnalyzer
from enhanced_task4 import TelemarketerDetector
from enhanced_problem3 import rearrange_digits, validate_solution
from enhanced_problem4 import sort_012_inplace, sort_012_counting, sort_012_functional


class TestLRUCache:
    """Comprehensive tests for LRU Cache implementation."""
    
    def test_basic_operations(self):
        """Test basic get and set operations."""
        cache = LRUCache(3)
        
        # Test set and get
        cache.set(1, "one")
        cache.set(2, "two")
        assert cache.get(1) == "one"
        assert cache.get(2) == "two"
        assert cache.get(3) == -1  # Key doesn't exist
    
    def test_capacity_limit(self):
        """Test that cache respects capacity limits."""
        cache = LRUCache(2)
        
        cache.set(1, "one")
        cache.set(2, "two")
        cache.set(3, "three")  # Should evict key 1
        
        assert cache.get(1) == -1  # Evicted
        assert cache.get(2) == "two"
        assert cache.get(3) == "three"
        assert cache.size() == 2
    
    def test_lru_eviction_order(self):
        """Test that least recently used items are evicted first."""
        cache = LRUCache(3)
        
        cache.set(1, "one")
        cache.set(2, "two")
        cache.set(3, "three")
        
        # Access key 1 to make it recently used
        cache.get(1)
        
        # Add key 4, should evict key 2 (least recently used)
        cache.set(4, "four")
        
        assert cache.get(1) == "one"    # Still present
        assert cache.get(2) == -1       # Evicted
        assert cache.get(3) == "three"  # Still present
        assert cache.get(4) == "four"   # Newly added
    
    def test_update_existing_key(self):
        """Test updating value for existing key."""
        cache = LRUCache(2)
        
        cache.set(1, "one")
        cache.set(2, "two")
        cache.set(1, "ONE")  # Update existing
        
        assert cache.get(1) == "ONE"
        assert cache.size() == 2
    
    def test_zero_capacity(self):
        """Test cache with zero capacity."""
        with pytest.raises(ValueError):
            LRUCache(0)
    
    def test_negative_capacity(self):
        """Test cache with negative capacity."""
        with pytest.raises(ValueError):
            LRUCache(-1)
    
    def test_single_capacity(self):
        """Test cache with capacity of 1."""
        cache = LRUCache(1)
        
        cache.set(1, "one")
        assert cache.get(1) == "one"
        
        cache.set(2, "two")  # Should evict key 1
        assert cache.get(1) == -1
        assert cache.get(2) == "two"
    
    def test_large_capacity(self):
        """Test cache with large capacity."""
        cache = LRUCache(1000)
        
        # Add many items
        for i in range(500):
            cache.set(i, f"value_{i}")
        
        # All should be present
        for i in range(500):
            assert cache.get(i) == f"value_{i}"
        
        assert cache.size() == 500


class TestFileSearcher:
    """Comprehensive tests for file search functionality."""
    
    @pytest.fixture
    def temp_dir_structure(self):
        """Create temporary directory structure for testing."""
        temp_dir = tempfile.mkdtemp()
        
        # Create directory structure
        dirs = [
            "subdir1",
            "subdir2",
            "subdir1/nested",
            "empty_dir"
        ]
        
        for dir_path in dirs:
            os.makedirs(os.path.join(temp_dir, dir_path), exist_ok=True)
        
        # Create test files
        files = [
            "file1.txt",
            "file2.py",
            "file3.c",
            "subdir1/nested_file.txt",
            "subdir1/nested_file.py", 
            "subdir1/nested/deep_file.c",
            "subdir2/another.txt",
            "README.md"
        ]
        
        for file_path in files:
            full_path = os.path.join(temp_dir, file_path)
            Path(full_path).touch()
        
        yield temp_dir
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    def test_find_files_basic(self, temp_dir_structure):
        """Test basic file finding functionality."""
        searcher = FileSearcher()
          # Find Python files
        py_files = searcher.find_files(".py", temp_dir_structure)
        assert len(py_files) == 2
        assert any("file2.py" in f for f in py_files)
        assert any("nested_file.py" in f for f in py_files)
    
    def test_find_files_with_depth_limit(self, temp_dir_structure):
        """Test file search with depth limitation."""
        searcher = FileSearcher()
        
        # Find .txt files with max depth 1 (root level only)
        txt_files = searcher.find_files(".txt", temp_dir_structure, max_depth=1)
        
        # Should find root level only
        assert len(txt_files) == 1
        assert any("file1.txt" in f for f in txt_files)
        
        # Find .txt files with max depth 2 (root + 1 subdirectory level)
        txt_files_depth2 = searcher.find_files(".txt", temp_dir_structure, max_depth=2)
        
        # Should find root level and first subdirectory level
        assert len(txt_files_depth2) == 3  # file1.txt, subdir1/nested_file.txt, subdir2/another.txt
        assert any("file1.txt" in f for f in txt_files_depth2)
        assert any("nested_file.txt" in f for f in txt_files_depth2)
        assert any("another.txt" in f for f in txt_files_depth2)
        
        # Should not find deeply nested files even with depth 2
        deep_files = [f for f in txt_files_depth2 if "deep_file" in f]
        assert len(deep_files) == 0
    
    def test_case_sensitivity(self, temp_dir_structure):
        """Test case sensitive and insensitive searches."""
        # Create file with uppercase extension
        upper_file = os.path.join(temp_dir_structure, "test.TXT")
        Path(upper_file).touch()
        
        # Case sensitive search
        case_sensitive = FileSearcher(case_sensitive=True)
        files = case_sensitive.find_files(".txt", temp_dir_structure)
        upper_files = [f for f in files if "test.TXT" in f]
        assert len(upper_files) == 0  # Shouldn't find .TXT when searching .txt
        
        # Case insensitive search
        case_insensitive = FileSearcher(case_sensitive=False)
        files = case_insensitive.find_files(".txt", temp_dir_structure)
        upper_files = [f for f in files if "test.TXT" in f]
        assert len(upper_files) == 1  # Should find .TXT when searching .txt
    
    def test_multiple_extensions(self, temp_dir_structure):
        """Test searching for multiple file extensions."""
        searcher = FileSearcher()
        
        results = searcher.find_multiple_extensions(
            {".py", ".txt", ".c"}, 
            temp_dir_structure
        )
        
        assert len(results[".py"]) == 2
        assert len(results[".txt"]) >= 3  # At least 3 .txt files
        assert len(results[".c"]) == 2
        assert ".md" not in results  # Wasn't requested
    
    def test_nonexistent_directory(self):
        """Test behavior with nonexistent directory."""
        searcher = FileSearcher()
        
        with pytest.raises(FileNotFoundError):
            searcher.find_files(".txt", "/nonexistent/directory")
    
    def test_file_as_path(self, temp_dir_structure):
        """Test behavior when path is a file, not directory.""" 
        searcher = FileSearcher()
        file_path = os.path.join(temp_dir_structure, "file1.txt")
        
        with pytest.raises(ValueError):
            searcher.find_files(".txt", file_path)
    
    def test_empty_directory(self, temp_dir_structure):
        """Test search in empty directory."""
        searcher = FileSearcher()
        empty_dir = os.path.join(temp_dir_structure, "empty_dir")
        
        files = searcher.find_files(".txt", empty_dir)
        assert len(files) == 0


class TestSquareRootAlgorithm:
    """Tests for square root implementation using binary search."""
    
    def sqrt_binary_search(self, number: int) -> int:
        """Binary search implementation of integer square root."""
        if number < 0:
            raise ValueError("Cannot compute square root of negative number")
        
        if number <= 1:
            return number
        
        left, right = 0, number
        
        while left <= right:
            mid = (left + right) // 2
            square = mid * mid
            
            if square == number:
                return mid
            elif square < number:
                # Check if mid is the floor of square root
                if (mid + 1) * (mid + 1) > number:
                    return mid
                left = mid + 1
            else:
                right = mid - 1
        
        return right
    
    def test_perfect_squares(self):
        """Test square roots of perfect squares."""
        perfect_squares = [(0, 0), (1, 1), (4, 2), (9, 3), (16, 4), (25, 5), (100, 10)]
        
        for number, expected in perfect_squares:
            assert self.sqrt_binary_search(number) == expected
    
    def test_non_perfect_squares(self):
        """Test square roots of non-perfect squares."""
        test_cases = [(2, 1), (3, 1), (5, 2), (8, 2), (15, 3), (24, 4), (99, 9)]
        
        for number, expected in test_cases:
            assert self.sqrt_binary_search(number) == expected
    
    def test_large_numbers(self):
        """Test square roots of large numbers."""
        assert self.sqrt_binary_search(10000) == 100
        assert self.sqrt_binary_search(999999) == 999
        assert self.sqrt_binary_search(1000000) == 1000
    
    def test_negative_numbers(self):
        """Test that negative numbers raise appropriate error."""
        with pytest.raises(ValueError):
            self.sqrt_binary_search(-1)
        
        with pytest.raises(ValueError):
            self.sqrt_binary_search(-10)


def run_performance_tests():
    """Run performance benchmarks for key algorithms."""
    import time
    import random
    
    print("\n=== Performance Benchmarks ===")
    
    # LRU Cache performance
    print("\n1. LRU Cache Performance:")
    cache = LRUCache(1000)
    
    start_time = time.time()
    for i in range(10000):
        cache.set(i, f"value_{i}")
    set_time = time.time() - start_time
    
    start_time = time.time()
    for i in range(10000):
        cache.get(random.randint(0, 9999))
    get_time = time.time() - start_time
    
    print(f"  10,000 SET operations: {set_time:.4f} seconds")
    print(f"  10,000 GET operations: {get_time:.4f} seconds")
    
    # File search performance
    print("\n2. File Search Performance:")
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create many test files
        for i in range(100):
            subdir = os.path.join(temp_dir, f"dir_{i}")
            os.makedirs(subdir, exist_ok=True)
            for j in range(10):
                file_path = os.path.join(subdir, f"file_{j}.txt")
                Path(file_path).touch()
        
        searcher = FileSearcher()
        start_time = time.time()
        files = searcher.find_files(".txt", temp_dir)
        search_time = time.time() - start_time
        
        print(f"  Found {len(files)} files in {search_time:.4f} seconds")


class TestUnscrambleCSProblems:
    """Tests for enhanced Unscramble CS Problems implementations."""
    
    def test_call_duration_parsing(self):
        """Test call duration parsing functionality."""
        # Sample call data
        calls_data = [
            ["12345", "67890", "01-09-2016 10:00:00", "120"],
            ["67890", "12345", "15-09-2016 14:30:00", "300"],
            ["11111", "22222", "20-08-2016 09:00:00", "180"],  # Wrong month
        ]
        
        durations = parse_call_duration(calls_data, 2016, 9)
        
        assert "12345" in durations
        assert "67890" in durations
        assert durations["12345"] == 420  # 120 + 300 (caller + receiver)
        assert durations["67890"] == 420  # 120 + 300 (caller + receiver)
        assert "11111" not in durations  # Wrong month
    
    def test_find_longest_caller(self):
        """Test finding caller with longest duration."""
        durations = {"12345": 100, "67890": 300, "11111": 50}
        
        result = find_longest_caller(durations)
        assert result == ("67890", 300)
        
        # Test empty case
        assert find_longest_caller({}) is None
    
    def test_phone_number_analyzer(self):
        """Test phone number classification."""
        analyzer = PhoneNumberAnalyzer()
        
        # Test different phone number types
        assert analyzer.classify_phone_number("(080)12345678") == "(080)"
        assert analyzer.classify_phone_number("(022)87654321") == "(022)"
        assert analyzer.classify_phone_number("9876 543210") == "9876"
        assert analyzer.classify_phone_number("14012345678") == "140"
        
        # Test Bangalore number detection
        assert analyzer.is_bangalore_number("(080)12345678") == True
        assert analyzer.is_bangalore_number("(022)87654321") == False
    
    def test_telemarketer_detector(self):
        """Test telemarketer detection logic."""
        detector = TelemarketerDetector()
        
        # Process test data
        detector.process_call_record("1111", "2222")  # 1111 calls 2222
        detector.process_call_record("3333", "1111")  # 3333 calls 1111
        detector.process_text_record("2222", "4444")  # 2222 texts 4444
        
        telemarketers = detector.get_potential_telemarketers()
        
        # 1111 receives calls and makes calls - not telemarketer
        # 2222 receives calls and sends texts - not telemarketer  
        # 3333 only makes calls - potential telemarketer
        assert "3333" in telemarketers
        assert "1111" not in telemarketers
        assert "2222" not in telemarketers


class TestProblemsVsAlgorithms:
    """Tests for enhanced Problems vs Algorithms implementations."""
    
    def test_rearrange_digits_basic(self):
        """Test basic rearrange digits functionality."""
        # Test case 1
        result = rearrange_digits([1, 2, 3, 4, 5])
        assert sum(result) == 542 + 31
        assert validate_solution([1, 2, 3, 4, 5], result)
        
        # Test case 2
        result = rearrange_digits([4, 6, 2, 5, 9, 8])
        expected_sum = 964 + 852
        assert sum(result) == expected_sum
        assert validate_solution([4, 6, 2, 5, 9, 8], result)
    
    def test_rearrange_digits_edge_cases(self):
        """Test edge cases for rearrange digits."""
        # Empty array
        assert rearrange_digits([]) == [-1, -1]
        
        # Single element
        assert rearrange_digits([5]) == [-1, -1]
        
        # All zeros
        result = rearrange_digits([0, 0])
        assert result == [0, 0]
        
        # Duplicate elements
        result = rearrange_digits([5, 5, 5, 5])
        assert sum(result) == 55 + 55
        assert validate_solution([5, 5, 5, 5], result)
    
    def test_sort_012_implementations(self):
        """Test all three sort 012 implementations."""
        test_cases = [
            [0, 0, 2, 2, 2, 1, 1, 1, 2, 0, 2],
            [2, 1, 0],
            [0, 0, 0],
            [1, 1, 1],
            [2, 2, 2],
            [],
            [1],
            [0, 1, 2],
        ]
        
        for test_input in test_cases:
            expected = sorted(test_input)
            
            # Test counting sort
            result_counting = sort_012_counting(test_input.copy())
            assert result_counting == expected
            
            # Test in-place sort
            test_copy = test_input.copy()
            sort_012_inplace(test_copy)
            assert test_copy == expected
            
            # Test functional sort
            result_functional = sort_012_functional(test_input.copy())
            assert result_functional == expected
            assert test_input == test_input  # Original unchanged
    
    def test_sort_012_invalid_input(self):
        """Test sort 012 with invalid input."""
        with pytest.raises(ValueError):
            sort_012_counting([0, 1, 2, 3])  # Invalid element
        
        with pytest.raises(ValueError):
            sort_012_inplace([0, 1, 2, -1])  # Invalid element


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
    
    # Run performance tests
    run_performance_tests()
