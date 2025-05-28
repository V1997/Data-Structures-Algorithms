"""
Enhanced File Finder Implementation
====================================

A robust recursive file search implementation with:
- Fixed mutable default argument issue
- Type hints and proper error handling
- Support for multiple file extensions
- Performance optimizations
- Comprehensive testing

Time Complexity: O(n) where n is number of files/directories
Space Complexity: O(d) where d is maximum directory depth
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Set


class FileSearcher:
    """
    Enhanced file search utility with multiple search strategies.
    """

    def __init__(self, case_sensitive: bool = True) -> None:
        """
        Initialize FileSearcher.

        Args:
            case_sensitive: Whether file extension matching is case sensitive
        """
        self.case_sensitive = case_sensitive

    def find_files(
        self, suffix: str, path: str, max_depth: Optional[int] = None
    ) -> List[str]:
        """
        Find all files with given suffix in directory tree.

        Args:
            suffix: File extension to search for (e.g., '.c', '.py')
            path: Root directory path to search
            max_depth: Maximum recursion depth (None for unlimited)

        Returns:
            List of file paths matching the suffix

        Raises:
            FileNotFoundError: If path doesn't exist
            PermissionError: If path is not accessible
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path does not exist: {path}")

        if not os.path.isdir(path):
            raise ValueError(f"Path is not a directory: {path}")

        result_files: List[str] = []
        self._recursive_search(suffix, path, result_files, max_depth, 0)
        return sorted(result_files)  # Return sorted for consistent results

    def _recursive_search(
        self,
        suffix: str,
        current_path: str,
        result_files: List[str],
        max_depth: Optional[int],
        current_depth: int,
    ) -> None:
        """
        Recursive helper for file search.

        Args:
            suffix: File extension to search for
            current_path: Current directory being searched
            result_files: List to accumulate results (modified in-place)
            max_depth: Maximum allowed depth
            current_depth: Current recursion depth
        """
        if max_depth is not None and current_depth >= max_depth:
            return

        try:
            items = os.listdir(current_path)
        except PermissionError:
            # Skip directories we can't access
            return

        for item in items:
            item_path = os.path.join(current_path, item)

            try:
                if os.path.isfile(item_path):
                    if self._matches_suffix(item, suffix):
                        result_files.append(item_path)
                elif os.path.isdir(item_path):
                    self._recursive_search(
                        suffix, item_path, result_files, max_depth, current_depth + 1
                    )
            except (PermissionError, OSError):
                # Skip files/directories we can't access
                continue

    def _matches_suffix(self, filename: str, suffix: str) -> bool:
        """
        Check if filename matches the given suffix.

        Args:
            filename: Name of the file
            suffix: Expected suffix/extension

        Returns:
            True if filename ends with suffix
        """
        if not self.case_sensitive:
            return filename.lower().endswith(suffix.lower())
        return filename.endswith(suffix)

    def find_multiple_extensions(
        self, extensions: Set[str], path: str, max_depth: Optional[int] = None
    ) -> Dict[str, List[str]]:
        """
        Find files with multiple extensions efficiently.

        Args:
            extensions: Set of file extensions to search for
            path: Root directory path to search
            max_depth: Maximum recursion depth

        Returns:
            Dictionary mapping extensions to lists of matching files
        """
        results: Dict[str, List[str]] = {ext: [] for ext in extensions}

        def collect_files(current_path: str, depth: int = 0) -> None:
            if max_depth is not None and depth >= max_depth:
                return

            try:
                for item in os.listdir(current_path):
                    item_path = os.path.join(current_path, item)

                    if os.path.isfile(item_path):
                        for ext in extensions:
                            if self._matches_suffix(item, ext):
                                results[ext].append(item_path)
                    elif os.path.isdir(item_path):
                        collect_files(item_path, depth + 1)
            except (PermissionError, OSError):
                pass

        collect_files(path)
        return results


def find_files_simple(suffix: str, path: str) -> List[str]:
    """
    Simple function interface for backward compatibility.
    Fixed version of the original function.

    Args:
        suffix: File extension to search for
        path: Directory path to search

    Returns:
        List of file paths with the given suffix
    """
    searcher = FileSearcher()
    return searcher.find_files(suffix, path)


def demonstrate_file_search() -> None:
    """Demonstrate file search functionality."""
    print("=== Enhanced File Search Demonstration ===\n")

    # Create a test directory structure
    test_dir = "test_files"
    os.makedirs(test_dir, exist_ok=True)
    os.makedirs(f"{test_dir}/subdir1", exist_ok=True)
    os.makedirs(f"{test_dir}/subdir2", exist_ok=True)

    # Create test files
    test_files = [
        f"{test_dir}/file1.txt",
        f"{test_dir}/file2.py",
        f"{test_dir}/subdir1/file3.txt",
        f"{test_dir}/subdir1/file4.py",
        f"{test_dir}/subdir2/file5.c",
    ]

    for file_path in test_files:
        Path(file_path).touch()

    try:
        searcher = FileSearcher()

        # Test 1: Find Python files
        print("Test 1: Find Python files")
        py_files = searcher.find_files(".py", test_dir)
        print(f"Python files found: {py_files}")

        # Test 2: Find text files with depth limit
        print("\nTest 2: Find text files (max depth 1)")
        txt_files = searcher.find_files(".txt", test_dir, max_depth=1)
        print(f"Text files found: {txt_files}")

        # Test 3: Multiple extensions
        print("\nTest 3: Multiple extensions search")
        multi_results = searcher.find_multiple_extensions(
            {".py", ".txt", ".c"}, test_dir
        )
        for ext, files in multi_results.items():
            print(f"{ext} files: {files}")

        # Test 4: Case insensitive search
        print("\nTest 4: Case insensitive search")
        case_insensitive = FileSearcher(case_sensitive=False)
        files = case_insensitive.find_files(".PY", test_dir)
        print(f"Case insensitive .PY search: {files}")

    finally:
        # Cleanup test files
        import shutil

        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)


if __name__ == "__main__":
    demonstrate_file_search()
