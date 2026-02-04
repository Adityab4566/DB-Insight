# Contributing to Database Performance Monitoring Dashboard

Thank you for your interest in contributing to this project! We welcome contributions from everyone.

## How to Contribute

### Reporting Bugs

1. **Check existing issues** first to avoid duplicates
2. **Use the bug report template** when creating new issues
3. **Include detailed information**:
   - Operating system and version
   - Python version
   - MySQL version
   - Steps to reproduce the issue
   - Expected vs actual behavior
   - Screenshots if applicable

### Suggesting Features

1. **Check existing feature requests** to avoid duplicates
2. **Clearly describe the feature** and its benefits
3. **Provide use cases** and examples
4. **Consider the scope** - keep features focused and relevant

### Code Contributions

#### Getting Started

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/db-performance-monitor.git
   cd db-performance-monitor
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

#### Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Make your changes** following the coding standards
3. **Test your changes** thoroughly
4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

#### Coding Standards

- **Python**: Follow PEP 8 style guidelines
- **JavaScript**: Use consistent indentation (2 spaces)
- **HTML/CSS**: Use semantic HTML and organized CSS
- **Comments**: Write clear, concise comments for complex logic
- **Naming**: Use descriptive variable and function names

#### Commit Message Format

Use clear, descriptive commit messages:

```
Type: Brief description

Detailed explanation if needed

Types:
- Add: New feature or functionality
- Fix: Bug fixes
- Update: Changes to existing features
- Remove: Removing code or features
- Docs: Documentation changes
- Style: Code formatting changes
- Refactor: Code restructuring without functionality changes
```

#### Testing

- **Test your changes** on different browsers
- **Verify database connectivity** with different MySQL versions
- **Check responsive design** on mobile devices
- **Test API endpoints** with different scenarios

#### Pull Request Process

1. **Update documentation** if needed
2. **Ensure all tests pass**
3. **Create a pull request** with:
   - Clear title and description
   - Reference to related issues
   - Screenshots for UI changes
   - Testing instructions

### Development Setup

#### Database Setup for Development

```sql
-- Create test database
CREATE DATABASE IF NOT EXISTS db_monitoring_test;
CREATE USER IF NOT EXISTS 'test_user'@'localhost' IDENTIFIED BY 'test123';
GRANT ALL PRIVILEGES ON db_monitoring_test.* TO 'test_user'@'localhost';
GRANT SELECT ON performance_schema.* TO 'test_user'@'localhost';
GRANT SELECT ON information_schema.* TO 'test_user'@'localhost';
FLUSH PRIVILEGES;
```

#### Environment Configuration

Create `.env.development`:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=db_monitoring_test
DB_USER=test_user
DB_PASSWORD=test123
FLASK_ENV=development
FLASK_DEBUG=True
```

### Code Review Process

1. **All contributions** require code review
2. **Maintainers will review** pull requests
3. **Address feedback** promptly and professionally
4. **Be patient** - reviews take time

### Community Guidelines

- **Be respectful** and inclusive
- **Help others** learn and grow
- **Stay focused** on the project goals
- **Follow the code of conduct**

### Getting Help

- **Check the documentation** first
- **Search existing issues** for similar problems
- **Ask questions** in issue discussions
- **Be specific** about your problem

### Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Project documentation

Thank you for contributing to make this project better! 🚀