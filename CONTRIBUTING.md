# Contributing to Data Structures & Algorithms

Thank you for your interest in contributing to this project! This guide will help you get started.

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Git

### Setup Instructions

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/Data-Structures-Algorithms.git
   cd Data-Structures-Algorithms
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

## Development Workflow

### Code Style
This project follows strict code quality standards:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Run quality checks before committing:
```bash
python scripts/dev_tools.py --check-quality
```

### Testing
We maintain comprehensive test coverage:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_comprehensive.py -v

# Run performance benchmarks
python tests/test_comprehensive.py
```

### Type Hints
All new code must include proper type hints:

```python
from typing import List, Dict, Optional

def process_data(items: List[int]) -> Dict[str, int]:
    """Process a list of integers and return summary statistics."""
    return {"count": len(items), "sum": sum(items)}
```

## Contributing Guidelines

### Issue Reporting
When reporting issues, please include:

1. **Clear Description**: What you expected vs. what happened
2. **Minimal Reproduction**: Steps to reproduce the issue
3. **Environment**: Python version, OS, relevant package versions
4. **Code Samples**: Minimal code that demonstrates the problem

### Pull Request Process

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write clean, well-documented code
   - Add tests for new functionality
   - Update documentation if needed
   - Follow the existing code style

3. **Test Your Changes**
   ```bash
   # Run all quality checks
   python scripts/dev_tools.py --check-quality
   
   # Run tests
   pytest
   
   # Test performance impact
   python notebooks/performance_analysis.ipynb
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add new algorithm implementation
   
   - Implement efficient merge sort algorithm
   - Add comprehensive test cases
   - Include performance benchmarks
   - Update documentation"
   ```

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Convention
We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` new features
- `fix:` bug fixes
- `docs:` documentation changes
- `test:` test additions or modifications
- `refactor:` code refactoring
- `perf:` performance improvements
- `chore:` maintenance tasks

### Code Review Guidelines

**For Reviewers:**
- Focus on correctness, performance, and maintainability
- Check test coverage for new features
- Verify documentation is updated
- Ensure code follows project conventions

**For Contributors:**
- Be responsive to feedback
- Make requested changes promptly
- Ask questions if feedback is unclear
- Update tests and docs as requested

## Project Structure

```
Data-Structures-Algorithms/
├── src/                    # Enhanced implementations
│   ├── enhanced_lru_cache.py
│   ├── enhanced_file_finder.py
│   └── ...
├── tests/                  # Comprehensive test suite
│   └── test_comprehensive.py
├── scripts/               # Development automation
│   └── dev_tools.py
├── notebooks/             # Performance analysis
│   └── performance_analysis.ipynb
├── docs/                  # Documentation
├── .github/              # CI/CD workflows
│   └── workflows/
└── original_modules/     # Original course assignments
    ├── 01 Unscramble Computer Science Problems/
    ├── 02 Show Me The Data Structures/
    ├── 03 Problems vs. Algorithms/
    └── 04 Route Planner/
```

## What to Contribute

### High Priority
1. **Missing Algorithm Implementations**
   - Huffman Coding improvements
   - Blockchain implementation enhancements
   - Advanced graph algorithms
   - Dynamic programming problems

2. **Performance Optimizations**
   - Algorithmic complexity improvements
   - Memory usage optimizations
   - Large-scale data handling

3. **Test Coverage**
   - Edge case testing
   - Performance regression tests
   - Integration tests
   - Fuzzing tests

### Medium Priority
1. **Documentation**
   - Algorithm explanations
   - Usage examples
   - Performance comparisons
   - Tutorial notebooks

2. **Developer Experience**
   - Better error messages
   - Debugging tools
   - Profiling utilities
   - Visualization tools

### Enhancement Ideas
1. **Visualization**
   - Algorithm step-by-step visualization
   - Performance charts
   - Complexity analysis graphs

2. **Benchmarking**
   - Cross-language performance comparisons
   - Real-world dataset testing
   - Scalability analysis

3. **Educational Content**
   - Interactive tutorials
   - Problem-solving guides
   - Interview preparation materials

## Code Quality Standards

### Performance Requirements
- All algorithms must meet their theoretical complexity bounds
- New implementations should be benchmarked against existing solutions
- Performance regressions are not acceptable without justification

### Documentation Requirements
- All public functions must have docstrings with examples
- Complex algorithms need detailed explanations
- Type hints are required for all function signatures
- README updates for new features

### Testing Requirements
- Minimum 90% code coverage for new features
- Edge cases must be tested
- Performance tests for time-critical algorithms
- Integration tests for complex features

## Getting Help

- **Documentation**: Check the README and inline documentation first
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Code Review**: Request reviews from maintainers

## Recognition

Contributors will be recognized in:
- README contributors section
- Release notes
- Documentation credits
- Special recognition for significant contributions

Thank you for contributing to make this project better for everyone!
