# Deployment Guide

This guide covers various deployment options for the ChatGPT Archive Search Tool, from local development to production environments.

## 🏠 Local Development

### Quick Start
```bash
# Clone and setup
git clone <repository-url>
cd chatgpt-archive-search
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run development server
python app.py
```

The application will be available at `http://localhost:5000`

### Development Configuration
- **Debug Mode**: Enabled by default in `app.py`
- **Auto-reload**: Flask automatically reloads on code changes
- **Error Details**: Full stack traces displayed in browser
- **Port**: Default 5000, configurable in `app.py`

## 🐳 Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for ChatGPT archives
RUN mkdir -p "ChatGPT chats/ChatGPT chats"

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "app.py"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  chatgpt-search:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./ChatGPT chats:/app/ChatGPT chats:ro
      - ./K:/0din/0din-JEF:/app/jef:ro  # Optional JEF integration
    environment:
      - FLASK_ENV=production
      - PYTHONPATH=/app/jef
    restart: unless-stopped
```

### Building and Running
```bash
# Build image
docker build -t chatgpt-search .

# Run container
docker run -d \
  --name chatgpt-search \
  -p 5000:5000 \
  -v "/path/to/your/ChatGPT chats:/app/ChatGPT chats:ro" \
  chatgpt-search

# With docker-compose
docker-compose up -d
```

## ☁️ Cloud Deployment

### Heroku

#### Procfile
```
web: python app.py
```

#### Runtime
```
python-3.9.6
```

#### Deployment Steps
```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main

# Scale dynos
heroku ps:scale web=1
```

#### Considerations
- **File Storage**: Heroku has ephemeral filesystem
- **Archive Upload**: Need to implement file upload feature
- **Memory Limits**: Consider dyno memory limits for large archives

### AWS EC2

#### Instance Setup
```bash
# Update system
sudo yum update -y

# Install Python 3.9
sudo yum install python39 python39-pip -y

# Install Git
sudo yum install git -y

# Clone repository
git clone <repository-url>
cd chatgpt-archive-search

# Setup virtual environment
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install process manager
sudo pip install gunicorn
```

#### Gunicorn Configuration
```python
# gunicorn_config.py
bind = "0.0.0.0:5000"
workers = 2
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
```

#### Systemd Service
```ini
# /etc/systemd/system/chatgpt-search.service
[Unit]
Description=ChatGPT Archive Search
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/chatgpt-archive-search
Environment=PATH=/home/ec2-user/chatgpt-archive-search/venv/bin
ExecStart=/home/ec2-user/chatgpt-archive-search/venv/bin/gunicorn -c gunicorn_config.py app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static {
        alias /home/ec2-user/chatgpt-archive-search/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Google Cloud Platform

#### App Engine
```yaml
# app.yaml
runtime: python39

env_variables:
  FLASK_ENV: production

automatic_scaling:
  min_instances: 1
  max_instances: 10
  target_cpu_utilization: 0.6

resources:
  cpu: 1
  memory_gb: 2
  disk_size_gb: 10
```

#### Deployment
```bash
# Install gcloud CLI
gcloud auth login
gcloud config set project your-project-id

# Deploy
gcloud app deploy
```

## 🔒 Production Security

### Environment Variables
```bash
# Production settings
export FLASK_ENV=production
export SECRET_KEY=your-secret-key-here
export MAX_CONTENT_LENGTH=16777216  # 16MB
export UPLOAD_FOLDER=/secure/path/to/uploads
```

### Security Headers
```python
# Add to app.py
from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)

# Security headers
Talisman(app, {
    'force_https': True,
    'strict_transport_security': True,
    'content_security_policy': {
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline' cdn.jsdelivr.net",
        'style-src': "'self' 'unsafe-inline' cdn.jsdelivr.net",
    }
})
```

### File Upload Security
```python
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'md', 'txt'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def secure_upload(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Additional validation
        return filename
    return None
```

## 📊 Monitoring and Logging

### Application Logging
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler(
        'logs/chatgpt-search.log', 
        maxBytes=10240000, 
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### Health Check Endpoint
```python
@app.route('/health')
def health_check():
    """Health check endpoint for load balancers"""
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0'
    }
```

### Performance Monitoring
```python
import time
from functools import wraps

def monitor_performance(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()
        app.logger.info(f'{f.__name__} took {end_time - start_time:.2f}s')
        return result
    return decorated_function
```

## 🔧 Configuration Management

### Environment-based Configuration
```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    ARCHIVE_PATH = os.environ.get('ARCHIVE_PATH') or 'ChatGPT chats/ChatGPT chats'
    JEF_PATH = os.environ.get('JEF_PATH') or 'K:/0din/0din-JEF'
    MAX_SEARCH_RESULTS = int(os.environ.get('MAX_SEARCH_RESULTS', 1000))
    SEARCH_TIMEOUT = int(os.environ.get('SEARCH_TIMEOUT', 30))

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    DEBUG = True
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
```

## 🚀 Performance Optimization

### Caching
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@cache.memoize(timeout=300)
def get_file_tree():
    # Expensive file tree generation
    pass

@cache.memoize(timeout=60)
def search_files(query_hash):
    # Cache search results
    pass
```

### Database Integration (Optional)
```python
# For large archives, consider SQLite indexing
import sqlite3

def create_search_index():
    conn = sqlite3.connect('search_index.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
            path TEXT UNIQUE,
            title TEXT,
            content TEXT,
            modified_date TIMESTAMP,
            file_size INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS files_fts 
        USING fts5(title, content, content='files', content_rowid='id')
    ''')
    
    conn.commit()
    conn.close()
```

## 📋 Deployment Checklist

### Pre-deployment
- [ ] Update `requirements.txt` with exact versions
- [ ] Set `FLASK_ENV=production`
- [ ] Configure proper logging
- [ ] Set up monitoring and health checks
- [ ] Test with production-like data volume
- [ ] Security audit (dependencies, configurations)
- [ ] Performance testing under load

### Post-deployment
- [ ] Verify application starts correctly
- [ ] Test all major features
- [ ] Check logs for errors
- [ ] Monitor resource usage
- [ ] Set up automated backups
- [ ] Configure SSL/TLS certificates
- [ ] Set up domain and DNS

### Maintenance
- [ ] Regular dependency updates
- [ ] Log rotation and cleanup
- [ ] Performance monitoring
- [ ] Security patches
- [ ] Backup verification
- [ ] Capacity planning

---

For specific deployment questions or issues, refer to the platform-specific documentation or create an issue in the repository.