# Installation Guide

This guide provides detailed installation instructions for the ChatGPT Archive Search Tool across different operating systems and environments.

## 📋 System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 512 MB available
- **Storage**: 100 MB for application + space for your archive
- **Browser**: Modern web browser (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)

### Recommended Requirements
- **Python**: 3.9 or higher
- **RAM**: 2 GB available
- **Storage**: 1 GB+ for large archives
- **Browser**: Latest version of Chrome, Firefox, or Edge

## 🖥️ Operating System Specific Instructions

### Windows Installation

#### Option 1: Using Command Prompt
1. **Open Command Prompt** as Administrator
2. **Check Python installation**:
   ```cmd
   python --version
   ```
   If Python is not installed, download from [python.org](https://python.org)

3. **Navigate to your desired directory**:
   ```cmd
   cd C:\Users\YourName\Documents
   ```

4. **Create project directory**:
   ```cmd
   mkdir chatgpt-search-tool
   cd chatgpt-search-tool
   ```

5. **Download application files** (copy all files to this directory)

6. **Install dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```

7. **Run the application**:
   ```cmd
   python app.py
   ```

#### Option 2: Using PowerShell
1. **Open PowerShell** as Administrator
2. **Check execution policy**:
   ```powershell
   Get-ExecutionPolicy
   ```
   If restricted, run:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Follow steps 2-7 from Command Prompt method**

#### Windows Troubleshooting
- **"python is not recognized"**: Add Python to PATH or use `py` instead of `python`
- **Permission denied**: Run Command Prompt as Administrator
- **Module not found**: Ensure pip is installed: `python -m ensurepip --upgrade`

### macOS Installation

#### Using Terminal
1. **Open Terminal** (Applications > Utilities > Terminal)

2. **Check Python installation**:
   ```bash
   python3 --version
   ```
   If not installed, install via Homebrew:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   brew install python
   ```

3. **Create project directory**:
   ```bash
   mkdir ~/chatgpt-search-tool
   cd ~/chatgpt-search-tool
   ```

4. **Download application files** to this directory

5. **Create virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

6. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

7. **Run the application**:
   ```bash
   python app.py
   ```

#### macOS Troubleshooting
- **Permission denied**: Use `sudo` for system-wide installation
- **Command not found**: Use `python3` and `pip3` instead of `python` and `pip`
- **SSL certificate errors**: Update certificates: `pip install --upgrade certifi`

### Linux Installation

#### Ubuntu/Debian
1. **Update package list**:
   ```bash
   sudo apt update
   ```

2. **Install Python and pip**:
   ```bash
   sudo apt install python3 python3-pip python3-venv
   ```

3. **Create project directory**:
   ```bash
   mkdir ~/chatgpt-search-tool
   cd ~/chatgpt-search-tool
   ```

4. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

5. **Download application files** to this directory

6. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

7. **Run the application**:
   ```bash
   python app.py
   ```

#### CentOS/RHEL/Fedora
1. **Install Python and pip**:
   ```bash
   # CentOS/RHEL
   sudo yum install python3 python3-pip
   
   # Fedora
   sudo dnf install python3 python3-pip
   ```

2. **Follow steps 3-7 from Ubuntu instructions**

#### Linux Troubleshooting
- **Permission denied**: Check file permissions: `chmod +x app.py`
- **Port already in use**: Change port in app.py or kill existing process
- **Module not found**: Ensure virtual environment is activated

## 🐳 Docker Installation

### Using Docker
1. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 5000
   
   CMD ["python", "app.py"]
   ```

2. **Build Docker image**:
   ```bash
   docker build -t chatgpt-search-tool .
   ```

3. **Run container**:
   ```bash
   docker run -p 5000:5000 -v /path/to/your/archive:/app/ChatGPT\ chats chatgpt-search-tool
   ```

### Using Docker Compose
1. **Create docker-compose.yml**:
   ```yaml
   version: '3.8'
   services:
     chatgpt-search:
       build: .
       ports:
         - "5000:5000"
       volumes:
         - ./ChatGPT chats:/app/ChatGPT chats
       environment:
         - FLASK_ENV=production
   ```

2. **Run with Docker Compose**:
   ```bash
   docker-compose up
   ```

## 🌐 Virtual Environment Setup

### Why Use Virtual Environments?
- **Isolation**: Prevents conflicts with other Python projects
- **Reproducibility**: Ensures consistent dependencies
- **Clean uninstall**: Easy to remove without affecting system Python

### Creating Virtual Environment

#### Windows
```cmd
python -m venv chatgpt-search-env
chatgpt-search-env\Scripts\activate
```

#### macOS/Linux
```bash
python3 -m venv chatgpt-search-env
source chatgpt-search-env/bin/activate
```

### Deactivating Virtual Environment
```bash
deactivate
```

## 📁 Archive Setup

### Supported Archive Structures
```
Option 1: Direct structure
ChatGPT chats/
└── ChatGPT chats/
    ├── 2022/
    ├── 2023/
    └── 2024/

Option 2: Custom structure
my-chatgpt-archive/
├── conversations/
│   ├── 2022/
│   └── 2023/
└── exports/
```

### Configuring Custom Archive Path
Edit `app.py` line 286:
```python
# Change this line to your archive path
search_engine = ChatSearchEngine("path/to/your/archive")
```

### File Format Requirements
- **Extension**: `.md` (markdown)
- **Encoding**: UTF-8
- **YAML frontmatter**: Optional but recommended
- **Content structure**: ChatGPT conversation format

## 🔧 Configuration Options

### Environment Variables
Create `.env` file:
```env
FLASK_ENV=development
FLASK_DEBUG=True
ARCHIVE_PATH=ChatGPT chats/ChatGPT chats
MAX_TREE_DEPTH=3
PORT=5000
HOST=0.0.0.0
```

### Application Settings
Edit `app.py` for custom configuration:
```python
# Server configuration
app.run(
    debug=True,          # Set to False for production
    host='0.0.0.0',      # Listen on all interfaces
    port=5000,           # Change port if needed
    threaded=True        # Enable threading
)

# Search configuration
max_depth = 3            # File tree depth limit
debounce_delay = 500     # Search delay in milliseconds
max_results = 1000       # Maximum search results
```

## 🚀 Production Deployment

### Using Gunicorn (Recommended)
1. **Install Gunicorn**:
   ```bash
   pip install gunicorn
   ```

2. **Create WSGI entry point** (`wsgi.py`):
   ```python
   from app import app
   
   if __name__ == "__main__":
       app.run()
   ```

3. **Run with Gunicorn**:
   ```bash
   gunicorn --bind 0.0.0.0:5000 wsgi:app
   ```

### Using Apache with mod_wsgi
1. **Install mod_wsgi**:
   ```bash
   pip install mod_wsgi
   ```

2. **Create Apache configuration**:
   ```apache
   <VirtualHost *:80>
       ServerName your-domain.com
       DocumentRoot /path/to/chatgpt-search-tool
       WSGIScriptAlias / /path/to/chatgpt-search-tool/app.wsgi
   </VirtualHost>
   ```

### Using Nginx + Gunicorn
1. **Nginx configuration**:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## 🔍 Verification

### Testing Installation
1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Check console output**:
   ```
   Initializing search engine with path: ChatGPT chats/ChatGPT chats
   Found X markdown files
   * Running on http://127.0.0.1:5000
   ```

3. **Open browser** and navigate to `http://localhost:5000`

4. **Verify functionality**:
   - File tree loads in sidebar
   - Search box accepts input
   - Theme toggle works
   - Export buttons appear after search

### Health Check Endpoints
- **Main page**: `http://localhost:5000/`
- **File tree API**: `http://localhost:5000/api/file-tree`
- **Search API**: `POST http://localhost:5000/search`

## 🆘 Installation Troubleshooting

### Common Issues

#### Python Not Found
```bash
# Windows
py --version
python3 --version

# macOS/Linux
python3 --version
which python3
```

#### Pip Not Found
```bash
# Install pip
python -m ensurepip --upgrade

# Or download get-pip.py
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

#### Permission Errors
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or use virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

#### Port Already in Use
```bash
# Find process using port 5000
netstat -tulpn | grep :5000  # Linux
netstat -an | findstr :5000  # Windows

# Kill process or change port in app.py
```

#### Module Import Errors
```bash
# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

### Getting Help
1. **Check logs**: Look at console output for error messages
2. **Browser console**: Press F12 and check for JavaScript errors
3. **File permissions**: Ensure read access to archive files
4. **Network issues**: Check firewall and antivirus settings
5. **Python environment**: Verify virtual environment activation

## 📞 Support Resources

- **Python Installation**: [python.org/downloads](https://python.org/downloads)
- **Pip Documentation**: [pip.pypa.io](https://pip.pypa.io)
- **Flask Documentation**: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- **Virtual Environments**: [docs.python.org/3/tutorial/venv.html](https://docs.python.org/3/tutorial/venv.html)

---

**Installation complete!** 🎉 You're ready to start searching your ChatGPT archive.