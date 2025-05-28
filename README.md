# 🚀 Data Structures & Algorithms Project

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://img.shields.io/badge/tests-pytest-green.svg)](https://pytest.org)

A comprehensive collection of **Data Structures & Algorithms** implementations and solutions from the Udacity Computer Science program. This project demonstrates efficient algorithmic thinking, optimal data structure usage, and modern Python development practices.

## 📚 Project Overview

This repository contains solutions to algorithmic challenges organized into 4 progressive modules:

### 🔍 **Module 1: Unscramble Computer Science Problems**
**Focus**: Time & Space Complexity Analysis
- **Task 0**: Data extraction and basic operations
- **Task 1**: Set operations for unique telephone numbers  
- **Task 2**: Longest duration call analysis
- **Task 3**: Area code pattern analysis
- **Task 4**: Telemarketer detection algorithm

### 🏗️ **Module 2: Show Me The Data Structures**
**Focus**: Custom Data Structure Implementation
- **Problem 1**: LRU Cache (Least Recently Used)
- **Problem 2**: File Recursion (Directory traversal)
- **Problem 3**: Huffman Coding (Compression algorithm)
- **Problem 4**: Active Directory (User group management)
- **Problem 5**: Blockchain (Distributed ledger)
- **Problem 6**: Union & Intersection (Linked lists)

### ⚡ **Module 3: Problems vs. Algorithms**
**Focus**: Advanced Algorithm Design
- **Problem 1**: Square Root (Binary search implementation)
- **Problem 2**: Search in Rotated Array
- **Problem 3**: Rearrange Array Digits
- **Problem 4**: Dutch National Flag Problem
- **Problem 5**: Autocomplete with Tries
- **Problem 6**: Unsorted Integer Array (Min/Max)
- **Problem 7**: HTTP Router using Trie

### 🗺️ **Module 4: Route Planner**
**Focus**: Graph Algorithms & Pathfinding
- **Implementation**: A* Search Algorithm
- **Application**: GPS-style shortest path finder
- **Visualization**: Interactive map navigation

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Data-Structures-Algorithms.git
cd Data-Structures-Algorithms

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running Solutions

```bash
# Execute specific problems
python "01 Unscramble Computer Science Problems/submit/Task0.py"
python "02 Show Me The Data Structures/single/problem_1.py"

# Run tests
pytest tests/ -v --cov=src/

# Format code
black src/ tests/
isort src/ tests/

# Run Route Planner (Jupyter Notebook)
cd "04 Route Planner/home"
jupyter notebook project_notebook.ipynb
```

## 🧪 Testing & Validation

Comprehensive test suite covering:
- ✅ **Unit Tests**: Individual function validation
- ✅ **Integration Tests**: End-to-end workflows  
- ✅ **Performance Tests**: Time & space complexity verification
- ✅ **Edge Cases**: Boundary conditions and error handling

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src/ --cov-report=html

# Run specific module tests
pytest tests/test_lru_cache.py -v
```

## 📊 Performance Analysis

Each solution includes:
- **Time Complexity**: Big O analysis
- **Space Complexity**: Memory usage assessment
- **Benchmarking**: Performance comparisons
- **Optimization Notes**: Trade-offs and improvements

## 🔧 Development Tools

- **Code Formatting**: Black, isort
- **Linting**: flake8, mypy
- **Testing**: pytest, coverage
- **Documentation**: Jupyter notebooks
- **Pre-commit Hooks**: Automated quality checks

## 📁 Project Structure

```
Data-Structures-Algorithms/
├── 01 Unscramble Computer Science Problems/
│   ├── submit/           # Solution files
│   └── data/            # Input datasets
├── 02 Show Me The Data Structures/
│   ├── single/          # Implementation files
│   └── explanations/    # Algorithm analysis
├── 03 Problems vs. Algorithms/
│   ├── single/          # Advanced solutions
│   └── tests/           # Unit tests
├── 04 Route Planner/
│   ├── home/            # A* implementation
│   └── maps/            # Graph data
├── src/                 # Enhanced implementations
├── tests/               # Comprehensive test suite
├── docs/                # Documentation
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## 🎯 Key Learning Outcomes

- **Algorithm Design**: Problem decomposition and solution strategies
- **Data Structure Mastery**: Choosing optimal structures for specific use cases
- **Complexity Analysis**: Understanding time/space trade-offs
- **Code Quality**: Writing maintainable, efficient Python code
- **Testing**: Comprehensive validation and edge case handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/enhancement`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push to branch (`git push origin feature/enhancement`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Udacity**: Course structure and problem sets
- **Python Community**: Libraries and best practices
- **Contributors**: Code reviews and enhancements

---

**📈 Project Status**: ✅ Active Development | 🧪 Tests Passing | 📚 Well Documented
