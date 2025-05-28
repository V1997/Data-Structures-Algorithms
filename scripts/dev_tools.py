#!/usr/bin/env python3
"""
Development and Testing Scripts
==============================

Utility scripts for development workflow automation.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command: str, description: str = "") -> int:
    """Run a shell command and return exit code."""
    if description:
        print(f"\n🔄 {description}")
    print(f"Running: {command}")
    
    result = subprocess.run(command, shell=True)
    if result.returncode == 0:
        print("✅ Success")
    else:
        print("❌ Failed")
    return result.returncode


def setup_development():
    """Set up development environment."""
    print("🚀 Setting up development environment...")
    
    commands = [
        ("python -m pip install --upgrade pip", "Upgrading pip"),
        ("pip install -e .[dev,docs,performance]", "Installing dependencies"),
        ("pre-commit install", "Installing pre-commit hooks"),
    ]
    
    for command, description in commands:
        if run_command(command, description) != 0:
            print(f"❌ Setup failed at: {description}")
            return False
    
    print("\n✅ Development environment setup complete!")
    return True


def run_tests():
    """Run the complete test suite."""
    print("🧪 Running test suite...")
    
    # Standard tests with coverage
    test_commands = [
        ("pytest tests/ -v --cov=src --cov-report=term-missing", "Running unit tests with coverage"),
        ("python tests/test_comprehensive.py", "Running performance benchmarks"),
    ]
    
    all_passed = True
    for command, description in test_commands:
        if run_command(command, description) != 0:
            all_passed = False
    
    if all_passed:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
    
    return all_passed


def run_enhanced_demos():
    """Run demonstrations of enhanced implementations."""
    print("🎯 Running enhanced algorithm demonstrations...")
    
    demo_commands = [
        ("python src/enhanced_lru_cache.py", "LRU Cache Demo"),
        ("python src/enhanced_file_finder.py", "File Finder Demo"),
        ("python src/enhanced_task2.py", "Call Duration Analysis Demo"),
        ("python src/enhanced_task3.py", "Bangalore Area Code Analysis Demo"),
        ("python src/enhanced_task4.py", "Telemarketer Detection Demo"),
        ("python src/enhanced_problem3.py", "Array Rearrangement Demo"),
        ("python src/enhanced_problem4.py", "Dutch National Flag Demo"),
    ]
    
    for command, description in demo_commands:
        print(f"\n{'='*60}")
        print(f"🔍 {description}")
        print(f"{'='*60}")
        run_command(command)


def run_quality_checks():
    """Run all code quality checks."""
    print("🔍 Running code quality checks...")
    
    commands = [
        ("black --check src/ tests/", "Checking code formatting"),
        ("isort --check-only src/ tests/", "Checking import sorting"),
        ("flake8 src/ tests/", "Running linter"),
        ("mypy src/", "Running type checker"),
        ("bandit -r src/", "Running security scanner"),
    ]
    
    all_passed = True
    for command, description in commands:
        if run_command(command, description) != 0:
            all_passed = False
    
    if all_passed:
        print("\n✅ All quality checks passed!")
    else:
        print("\n❌ Some quality checks failed!")
    
    return all_passed


def format_code():
    """Format code with black and isort."""
    print("🎨 Formatting code...")
    
    commands = [
        ("black src/ tests/", "Formatting with Black"),
        ("isort src/ tests/", "Sorting imports"),
    ]
    
    for command, description in commands:
        run_command(command, description)
    
    print("\n✅ Code formatting complete!")


def clean_project():
    """Clean up project artifacts."""
    print("🧹 Cleaning project...")
    
    patterns_to_remove = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyd",
        "**/.pytest_cache",
        "**/htmlcov",
        "**/.coverage",
        "**/*.egg-info",
        "**/build",
        "**/dist",
    ]
    
    for pattern in patterns_to_remove:
        for path in Path(".").glob(pattern):
            if path.is_file():
                path.unlink()
                print(f"Removed file: {path}")
            elif path.is_dir():
                import shutil
                shutil.rmtree(path)
                print(f"Removed directory: {path}")
    
    print("✅ Project cleaned!")


def generate_docs():
    """Generate project documentation."""
    print("📚 Generating documentation...")
    
    # Create docs directory if it doesn't exist
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    
    commands = [
        ("jupyter nbconvert --to html notebooks/*.ipynb --output-dir docs/", 
         "Converting notebooks to HTML"),
        ("python -c \"import src.enhanced_lru_cache; help(src.enhanced_lru_cache)\" > docs/lru_cache_help.txt", 
         "Generating help documentation"),
    ]
    
    for command, description in commands:
        run_command(command, description)
    
    print("✅ Documentation generated!")


def main():
    """Main CLI interface."""
    if len(sys.argv) < 2:
        print("""
🛠️  Data Structures & Algorithms Development Tools

Usage: python scripts/dev_tools.py <command>

Commands:
  setup     - Set up development environment
  test      - Run test suite
  quality   - Run code quality checks
  format    - Format code with Black and isort
  clean     - Clean project artifacts
  docs      - Generate documentation
  demos     - Run enhanced implementation demos
  all       - Run quality checks and tests
  
Examples:
  python scripts/dev_tools.py setup
  python scripts/dev_tools.py test
  python scripts/dev_tools.py quality
        """)
        return
    
    command = sys.argv[1].lower()
    
    if command == "setup":
        setup_development()
    elif command == "test":
        run_tests()
    elif command == "quality":
        run_quality_checks()
    elif command == "format":
        format_code()
    elif command == "clean":
        clean_project()
    elif command == "docs":
        generate_docs()
    elif command == "demos":
        run_enhanced_demos()
    elif command == "all":
        print("🚀 Running complete quality pipeline...")
        if run_quality_checks() and run_tests():
            print("\n🎉 All checks passed! Ready for commit.")
        else:
            print("\n❌ Some checks failed. Please fix issues before committing.")
            sys.exit(1)
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
