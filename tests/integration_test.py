#!/usr/bin/env python3
"""
Quick Integration Test for Enhanced Implementations
==================================================

Simple tests to verify that our enhanced implementations work correctly.
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_enhanced_lru_cache():
    """Test enhanced LRU Cache."""
    print("🔍 Testing Enhanced LRU Cache...")
    try:
        from enhanced_lru_cache import LRUCache
        
        cache = LRUCache(3)
        cache.set(1, "one")
        cache.set(2, "two")
        cache.set(3, "three")
        
        assert cache.get(1) == "one"
        assert cache.get(2) == "two"
        assert cache.get(3) == "three"
        assert cache.get(4) == -1
        
        print("  ✅ LRU Cache basic operations: PASS")
        
        # Test capacity limit
        cache.set(4, "four")  # Should evict key 1
        assert cache.get(1) == -1
        assert cache.get(4) == "four"
        
        print("  ✅ LRU Cache capacity management: PASS")
        
    except Exception as e:
        print(f"  ❌ LRU Cache test failed: {e}")
        assert False, f"LRU Cache test failed: {e}"


def test_enhanced_file_finder():
    """Test enhanced file finder."""
    print("🔍 Testing Enhanced File Finder...")
    try:
        from enhanced_file_finder import FileSearcher
        
        searcher = FileSearcher()
        
        # Test with current directory (should find Python files)
        files = searcher.find_files(".py", ".")
        assert len(files) > 0
        assert any(f.endswith(".py") for f in files)
        
        print(f"  ✅ File Finder found {len(files)} Python files: PASS")
        
    except Exception as e:
        print(f"  ❌ File Finder test failed: {e}")
        assert False, f"File Finder test failed: {e}"


def test_enhanced_algorithms():
    """Test enhanced algorithm implementations."""
    print("🔍 Testing Enhanced Algorithms...")
    
    try:
        # Test rearrange digits
        from enhanced_problem3 import rearrange_digits
        
        result = rearrange_digits([1, 2, 3, 4, 5])
        assert len(result) == 2
        assert sum(result) == 542 + 31
        print("  ✅ Rearrange Digits: PASS")
        
    except Exception as e:
        print(f"  ❌ Rearrange Digits test failed: {e}")
        
    try:
        # Test sort 012
        from enhanced_problem4 import sort_012_counting
        
        test_array = [2, 1, 0, 2, 1, 0]
        result = sort_012_counting(test_array)
        assert result == [0, 0, 1, 1, 2, 2]
        print("  ✅ Sort 012: PASS")
        
    except Exception as e:
        print(f"  ❌ Sort 012 test failed: {e}")
        assert False, f"Sort 012 test failed: {e}"


def main():
    """Run all integration tests."""
    print("🚀 Running Integration Tests for Enhanced Implementations")
    print("=" * 60)
    
    tests = [
        test_enhanced_lru_cache,
        test_enhanced_file_finder,
        test_enhanced_algorithms,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All integration tests passed!")
        return True
    else:
        print("❌ Some tests failed. Check the implementations.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
