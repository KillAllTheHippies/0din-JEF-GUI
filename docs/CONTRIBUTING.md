# Contributing to ChatGPT Archive Search Tool

Thank you for your interest in contributing to the ChatGPT Archive Search Tool! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues
1. **Search existing issues** first to avoid duplicates
2. **Use issue templates** when available
3. **Provide detailed information**:
   - Operating system and version
   - Python version
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages and logs

### Suggesting Features
1. **Check existing feature requests** in issues
2. **Describe the use case** and problem being solved
3. **Provide mockups or examples** when helpful
4. **Consider implementation complexity** and maintenance burden

### Code Contributions

#### Development Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/chatgpt-archive-search.git
cd chatgpt-archive-search

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy
```

#### Code Standards
- **Python Style**: Follow PEP 8 guidelines
- **Formatting**: Use `black` for code formatting
- **Linting**: Use `flake8` for linting
- **Type Hints**: Use type hints where appropriate
- **Documentation**: Document all public functions and classes

#### Testing Requirements
- **Unit Tests**: Add tests for new functionality
- **Integration Tests**: Test JEF integration if applicable
- **Manual Testing**: Test UI changes in multiple browsers
- **Performance**: Consider impact on search performance

#### Pull Request Process
1. **Fork the repository** and create a feature branch
2. **Make your changes** following code standards
3. **Add or update tests** as needed
4. **Update documentation** if required
5. **Run the test suite** to ensure nothing breaks
6. **Submit a pull request** with clear description

### Documentation Contributions
- **Fix typos and errors** in existing documentation
- **Add missing documentation** for features
- **Improve clarity** of installation instructions
- **Add examples** and use cases
- **Update screenshots** when UI changes

## 🏗️ Project Structure

```
chatgpt-archive-search/
├── app.py                              # Main Flask application
├── requirements.txt                    # Python dependencies
├── templates/                          # HTML templates
│   ├── base.html                      # Base template with styling
│   └── index.html                     # Main search interface
├── test_*.py                          # Test files
├── debug_tree.py                      # Debug utilities
├── README.md                          # Main documentation
├── INSTALLATION.md                    # Installation guide
├── CONTRIBUTING.md                    # This file
├── JEF_INTEGRATION_*.md              # JEF integration docs
└── .rovodev/                         # Development tools
```

## 🔧 Development Guidelines

### Code Organization
- **Single Responsibility**: Each function should have one clear purpose
- **Modularity**: Break complex functionality into smaller modules
- **Error Handling**: Implement proper error handling and logging
- **Configuration**: Use environment variables for configuration

### Frontend Development
- **Bootstrap**: Use Bootstrap components for consistency
- **JavaScript**: Keep JavaScript modular and well-commented
- **Accessibility**: Ensure UI is accessible (ARIA labels, keyboard navigation)
- **Responsive Design**: Test on different screen sizes

### Backend Development
- **Flask Best Practices**: Follow Flask application patterns
- **Security**: Validate all inputs and sanitize file paths
- **Performance**: Optimize search algorithms for large archives
- **Logging**: Add appropriate logging for debugging

### JEF Integration
- **Optional Dependency**: JEF integration should be optional
- **Error Handling**: Gracefully handle JEF unavailability
- **Documentation**: Document JEF-specific features clearly
- **Testing**: Test both with and without JEF available

## 🧪 Testing Guidelines

### Test Categories
1. **Unit Tests**: Test individual functions and classes
2. **Integration Tests**: Test component interactions
3. **UI Tests**: Test user interface functionality
4. **Performance Tests**: Test with large datasets

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python test_search_simple.py

# Test JEF integration
python test_jef_integration.py

# Debug file tree
python debug_tree.py
```

### Test Data
- Use sample markdown files for testing
- Test with various file sizes and structures
- Include edge cases (empty files, special characters)
- Test with and without JEF framework

## 📝 Documentation Standards

### Code Documentation
```python
def search_files(self, search_terms: str, mode: str = "ALL") -> List[Dict]:
    """
    Search for terms in markdown files.
    
    Args:
        search_terms: Space-separated search terms
        mode: Search mode - "ALL" (AND) or "ANY" (OR)
        
    Returns:
        List of dictionaries containing file information and match details
        
    Raises:
        ValueError: If search_terms is empty
        FileNotFoundError: If base path doesn't exist
        
    Example:
        >>> engine = ChatSearchEngine("./archive")
        >>> results = engine.search_files("python code", "ALL")
        >>> len(results)
        5
    """
```

### Markdown Documentation
- Use clear headings and structure
- Include code examples with syntax highlighting
- Add screenshots for UI features
- Link between related documentation files
- Keep language clear and concise

## 🚀 Release Process

### Version Numbering
- Follow [Semantic Versioning](https://semver.org/)
- **Major**: Breaking changes
- **Minor**: New features, backward compatible
- **Patch**: Bug fixes, backward compatible

### Release Checklist
- [ ] Update version numbers
- [ ] Update CHANGELOG.md
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Test installation process
- [ ] Create release notes
- [ ] Tag release in Git

## 🎯 Priority Areas for Contribution

### High Priority
- **Performance optimization** for large archives
- **Additional export formats** (PDF, HTML)
- **Advanced search operators** (regex, wildcards)
- **Improved error handling** and user feedback

### Medium Priority
- **Plugin system** for custom analyzers
- **Search result caching** for better performance
- **Keyboard shortcuts** for power users
- **Dark/light theme improvements**

### Low Priority
- **Additional JEF analysis types**
- **Search history** and saved searches
- **File preview thumbnails**
- **Multi-language support**

## 📞 Getting Help

### Communication Channels
- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Code Review**: Through pull request comments

### Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Semantic Versioning](https://semver.org/)

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

Thank you for contributing to the ChatGPT Archive Search Tool! 🎉