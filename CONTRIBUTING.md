# Contributing to EasySLAM

Thank you for your interest in contributing to EasySLAM! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues
- Use the [GitHub Issues](https://github.com/Sherin-SEF-AI/EasySLAM/issues) page
- Include a clear description of the problem
- Provide steps to reproduce the issue
- Include system information (OS, Python version, etc.)
- Add error messages and logs if applicable

### Feature Requests
- Use the [GitHub Issues](https://github.com/Sherin-SEF-AI/EasySLAM/issues) page
- Describe the feature you'd like to see
- Explain why this feature would be useful
- Provide examples of how it would work

### Code Contributions
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass: `pytest tests/`
6. Commit your changes: `git commit -m 'Add feature: description'`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## 🛠️ Development Setup

### Prerequisites
- Python 3.7 or higher
- Git
- pip

### Local Development
```bash
# Clone the repository
git clone https://github.com/Sherin-SEF-AI/EasySLAM.git
cd EasySLAM

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .[dev]

# Run tests
pytest tests/

# Run linting
flake8 easy_slam/
black easy_slam/
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=easy_slam

# Run specific test file
pytest tests/test_core.py

# Run with verbose output
pytest -v
```

## 📝 Code Style

### Python Style Guide
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use type hints for function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions small and focused

### Example Code Style
```python
from typing import Optional, List, Dict, Any
import numpy as np

def process_frame(
    frame: np.ndarray,
    algorithm: str = 'orb_slam',
    config: Optional[Dict[str, Any]] = None
) -> Optional[np.ndarray]:
    """
    Process a frame with the specified SLAM algorithm.
    
    Args:
        frame: Input frame as numpy array
        algorithm: SLAM algorithm to use
        config: Optional configuration dictionary
        
    Returns:
        Processed frame or None if processing failed
        
    Raises:
        ValueError: If algorithm is not supported
    """
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    # Process the frame
    result = _apply_algorithm(frame, algorithm, config)
    return result
```

### Documentation
- Write clear, concise docstrings
- Include examples in docstrings
- Update README.md for new features
- Add inline comments for complex logic

## 🧪 Testing Guidelines

### Test Structure
- Place tests in the `tests/` directory
- Name test files as `test_*.py`
- Use descriptive test function names
- Group related tests in classes

### Example Test
```python
import pytest
import numpy as np
from easy_slam import EasySLAM

class TestEasySLAM:
    def test_initialization(self):
        """Test EasySLAM initialization with default parameters."""
        slam = EasySLAM()
        assert slam is not None
        assert slam.algorithm == 'orb_slam'
    
    def test_invalid_camera(self):
        """Test initialization with invalid camera."""
        with pytest.raises(ValueError):
            EasySLAM(camera='invalid_camera')
    
    def test_algorithm_selection(self):
        """Test different algorithm selections."""
        algorithms = ['orb_slam', 'fastslam', 'graphslam']
        for alg in algorithms:
            slam = EasySLAM(algorithm=alg)
            assert slam.algorithm == alg
```

### Test Requirements
- All new code must have corresponding tests
- Maintain at least 80% code coverage
- Tests should be fast and reliable
- Use fixtures for common test data

## 🔧 Pull Request Guidelines

### Before Submitting
1. Ensure all tests pass
2. Update documentation if needed
3. Add tests for new functionality
4. Follow the code style guidelines
5. Update CHANGELOG.md if applicable

### Pull Request Template
```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes (or documented)
```

## 📋 Issue Templates

### Bug Report Template
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
A clear description of what you expected to happen.

**Environment:**
- OS: [e.g. Ubuntu 20.04]
- Python version: [e.g. 3.8]
- EasySLAM version: [e.g. 0.1.0]

**Additional context**
Add any other context about the problem here.
```

### Feature Request Template
```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
A clear description of any alternative solutions.

**Additional context**
Add any other context or screenshots about the feature request.
```

## 🏷️ Versioning

We follow [Semantic Versioning](https://semver.org/) (SemVer):
- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality
- **PATCH** version for backwards-compatible bug fixes

## 📞 Contact

- **Email**: sherin.joseph2217@gmail.com
- **GitHub Issues**: [Create an issue](https://github.com/Sherin-SEF-AI/EasySLAM/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Sherin-SEF-AI/EasySLAM/discussions)

## 🙏 Acknowledgments

Thank you to all contributors who help make EasySLAM better!

---

**Happy coding! 🚀** 