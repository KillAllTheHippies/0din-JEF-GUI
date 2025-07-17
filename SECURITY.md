# Security Policy

## 🛡️ Security Overview

The ChatGPT Archive Search Tool is designed with security and privacy as core principles. This document outlines our security practices, known considerations, and how to report security issues.

## 🔒 Security Principles

### Privacy by Design
- **Local Processing**: All data processing happens locally on your machine
- **No External Transmission**: ChatGPT archive data never leaves your system
- **No Cloud Dependencies**: Core functionality works entirely offline
- **User Control**: You maintain complete control over your data

### Secure Architecture
- **Input Validation**: All user inputs are validated and sanitized
- **Path Traversal Protection**: File access is restricted to the archive directory
- **Memory Safety**: Efficient processing prevents memory exhaustion attacks
- **Error Handling**: Secure error messages that don't leak sensitive information

## 🔍 Security Features

### File Access Security
```python
# Path traversal protection
def secure_path_join(base_path, user_path):
    """Safely join paths preventing directory traversal"""
    safe_path = os.path.normpath(os.path.join(base_path, user_path))
    if not safe_path.startswith(base_path):
        raise SecurityError("Path traversal attempt detected")
    return safe_path
```

### Input Sanitization
- **Search Terms**: Regex patterns are escaped to prevent injection
- **File Paths**: All file paths are validated against allowed directories
- **Export Data**: Output is properly escaped for CSV/JSON formats
- **Upload Validation**: File types and sizes are strictly validated

### Content Security Policy
```html
<!-- Implemented in base.html -->
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' 'unsafe-inline' cdn.jsdelivr.net; 
               style-src 'self' 'unsafe-inline' cdn.jsdelivr.net;">
```

## 🚨 Known Security Considerations

### JEF Integration
- **Optional Dependency**: JEF framework is optional and gracefully degrades
- **Local Analysis**: All JEF analysis happens locally without network access
- **Sandboxed Execution**: JEF analysis runs in isolated Python environment
- **Error Isolation**: JEF failures don't affect core search functionality

### File Processing
- **Memory Limits**: Large files are processed in chunks to prevent DoS
- **File Type Restrictions**: Only `.md` files are processed by default
- **Size Limits**: Configurable file size limits prevent resource exhaustion
- **Encoding Safety**: UTF-8 encoding with error handling for malformed files

### Web Interface
- **CSRF Protection**: Forms include CSRF tokens (implement if adding forms)
- **XSS Prevention**: All user content is properly escaped in templates
- **Clickjacking Protection**: X-Frame-Options header prevents embedding
- **HTTPS Enforcement**: Production deployments should use HTTPS

## 🔧 Security Configuration

### Production Security Headers
```python
# Add to app.py for production
@app.after_request
def security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response
```

### Environment Variables
```bash
# Secure configuration
export SECRET_KEY="your-secure-random-key-here"
export MAX_CONTENT_LENGTH=16777216  # 16MB file upload limit
export SESSION_COOKIE_SECURE=True
export SESSION_COOKIE_HTTPONLY=True
export SESSION_COOKIE_SAMESITE=Lax
```

### File Permissions
```bash
# Secure file permissions
chmod 600 config.py              # Configuration files
chmod 644 *.py                   # Python source files
chmod 755 static/               # Static assets directory
chmod 700 logs/                 # Log files directory
```

## 🛠️ Security Best Practices

### For Users

#### Archive Security
- **File Permissions**: Ensure your ChatGPT archive has appropriate permissions
- **Backup Security**: Encrypt backups of sensitive conversation data
- **Access Control**: Limit who can access the machine running the tool
- **Network Security**: Use firewall rules to restrict access if needed

#### Browser Security
- **Keep Updated**: Use the latest version of your web browser
- **Extensions**: Be cautious with browser extensions that might access page content
- **Private Browsing**: Consider using private/incognito mode for sensitive searches
- **Clear Data**: Clear browser data after use if on shared computers

### For Developers

#### Code Security
- **Dependency Updates**: Regularly update Python dependencies
- **Static Analysis**: Use tools like `bandit` for security scanning
- **Code Review**: Review all changes for security implications
- **Testing**: Include security test cases in the test suite

#### Deployment Security
- **HTTPS Only**: Always use HTTPS in production
- **Firewall Rules**: Restrict network access to necessary ports only
- **Regular Updates**: Keep the operating system and Python updated
- **Monitoring**: Implement logging and monitoring for security events

## 🐛 Vulnerability Disclosure

### Reporting Security Issues

If you discover a security vulnerability, please report it responsibly:

1. **Do NOT** create a public GitHub issue
2. **Email**: Send details to [security@example.com] (replace with actual email)
3. **Include**: 
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact assessment
   - Suggested fix (if any)

### Response Process

1. **Acknowledgment**: We'll acknowledge receipt within 24 hours
2. **Investigation**: We'll investigate and assess the issue within 72 hours
3. **Fix Development**: We'll develop and test a fix
4. **Disclosure**: We'll coordinate disclosure timing with you
5. **Credit**: We'll credit you in the security advisory (if desired)

### Security Advisory Process

For confirmed vulnerabilities:
- Security advisory will be published on GitHub
- Fix will be released as soon as possible
- Users will be notified through multiple channels
- Detailed mitigation steps will be provided

## 🔍 Security Auditing

### Self-Assessment Checklist

#### Code Security
- [ ] All user inputs are validated and sanitized
- [ ] File paths are checked for traversal attempts
- [ ] Error messages don't leak sensitive information
- [ ] Dependencies are up to date and vulnerability-free
- [ ] Secrets are not hardcoded in source code

#### Deployment Security
- [ ] HTTPS is enforced in production
- [ ] Security headers are properly configured
- [ ] File permissions are restrictive
- [ ] Logging captures security-relevant events
- [ ] Regular security updates are applied

#### Data Security
- [ ] Sensitive data is not logged
- [ ] Archive files have appropriate permissions
- [ ] Temporary files are securely cleaned up
- [ ] Export files don't contain unexpected data
- [ ] Memory is efficiently managed

### Security Testing

#### Automated Testing
```bash
# Install security testing tools
pip install bandit safety

# Run security scans
bandit -r . -f json -o security-report.json
safety check --json --output security-deps.json

# Check for known vulnerabilities
pip-audit
```

#### Manual Testing
- **Input Validation**: Test with malicious inputs
- **Path Traversal**: Attempt directory traversal attacks
- **File Upload**: Test with malicious file types and sizes
- **XSS**: Test for cross-site scripting vulnerabilities
- **CSRF**: Test for cross-site request forgery

## 📚 Security Resources

### Documentation
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/2.0.x/security/)
- [Python Security Guidelines](https://python.org/dev/security/)

### Tools
- **Static Analysis**: `bandit`, `semgrep`
- **Dependency Scanning**: `safety`, `pip-audit`
- **Web Security**: `OWASP ZAP`, `Burp Suite`
- **Code Quality**: `sonarqube`, `codeclimate`

### Training
- [Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
- [Python Security](https://realpython.com/python-security/)
- [Web Application Security](https://portswigger.net/web-security)

## 📞 Contact

For security-related questions or concerns:
- **Security Issues**: [security@example.com]
- **General Questions**: Create a GitHub issue
- **Documentation**: Refer to this security policy

---

**Security is a shared responsibility. Thank you for helping keep the ChatGPT Archive Search Tool secure!**