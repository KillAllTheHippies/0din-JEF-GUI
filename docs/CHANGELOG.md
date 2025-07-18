# Changelog

All notable changes to the ChatGPT Archive Search Tool will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation updates
- API documentation with request/response examples
- Security considerations documentation
- Architecture overview and system diagrams
- Contributing guidelines for developers
- Testing documentation and coverage information

### Changed
- Enhanced README.md with detailed feature descriptions
- Improved code documentation and inline comments
- Updated installation guide with troubleshooting steps

### Fixed
- Documentation consistency across all files
- Missing docstrings in core functions

## [2.0.0] - 2024-01-17

### Added
- JEF (Jailbreak Evaluation Framework) integration
- Security analysis capabilities for ChatGPT conversations
- Batch analysis functionality for multiple files
- Advanced search with boolean logic (ALL/ANY)
- Exact phrase matching with quotes
- Case-sensitive search option
- Date range filtering
- File explorer with interactive tree view
- Right-click context menus for folder operations
- Include/exclude folder filtering
- Export functionality (CSV, JSON, paths-only)
- Modal file viewer with markdown rendering
- Dark/light theme support with auto-detection
- Responsive design for mobile devices

### Changed
- Complete UI overhaul with Bootstrap 5
- Improved search performance and relevance scoring
- Enhanced file tree navigation
- Better error handling and user feedback

### Security
- Path traversal protection
- Input validation and sanitization
- Local-only processing (no external data transmission)

## [1.0.0] - Initial Release

### Added
- Basic search functionality for ChatGPT markdown archives
- Simple web interface
- File listing and basic filtering
- Export to CSV format

### Features
- Search through ChatGPT conversation archives
- Basic keyword matching
- File metadata extraction
- Simple results display

---

## Version History Notes

### JEF Integration
The JEF (Jailbreak Evaluation Framework) integration was added in version 2.0.0 to provide security analysis capabilities. This integration:

- Analyzes conversation content for potential security issues
- Provides multiple analysis types (Tiananmen, Nerve Agent, Methamphetamine, Harry Potter, Copyright)
- Operates entirely locally without external network access
- Is optional and gracefully degrades if JEF is not available

### Architecture Evolution
The application has evolved from a simple search tool to a comprehensive archive analysis platform:

1. **v1.0**: Basic search and file listing
2. **v2.0**: Advanced search, JEF integration, modern UI
3. **Future**: Plugin system, advanced analytics, collaboration features

### Breaking Changes

#### v2.0.0
- **API Changes**: Search endpoint now expects JSON payload instead of form data
- **File Structure**: Templates moved to dedicated directory
- **Dependencies**: Added markdown, PyYAML, and Pygments requirements
- **Configuration**: JEF path configuration required for security analysis

### Migration Guide

#### From v1.0 to v2.0
1. **Update Dependencies**: Install new requirements from `requirements.txt`
2. **Template Updates**: Replace old templates with new Bootstrap 5 versions
3. **API Updates**: Update any custom integrations to use new JSON API format
4. **JEF Setup**: Optionally install JEF framework for security analysis features

### Known Issues

#### Current Version
- Large archives (>10,000 files) may experience slower search performance
- JEF analysis requires specific Python environment setup
- File tree expansion can be memory-intensive for deep directory structures

#### Workarounds
- Use folder filtering to limit search scope for large archives
- Implement pagination for very large result sets
- Consider indexing for frequently searched archives

### Planned Features

#### Next Release (v2.1.0)
- [ ] Search result caching for improved performance
- [ ] Advanced search operators (regex, wildcards)
- [ ] Keyboard shortcuts for power users
- [ ] Search history and saved searches

#### Future Releases
- [ ] Plugin system for custom analyzers
- [ ] Multi-language support
- [ ] Collaborative features for team archives
- [ ] Advanced visualization and analytics

---

For more information about specific features and changes, see the individual documentation files in the repository.