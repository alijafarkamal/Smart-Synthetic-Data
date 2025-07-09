# 🚀 Deployment Guide

## Local Development

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Access the app**:
   Open your browser and go to `http://localhost:8501`

## Cloud Deployment

### Render.com

1. **Create a new Web Service**
2. **Connect your GitHub repository**
3. **Configure the service**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
4. **Deploy**

### Replit

1. **Create a new Python repl**
2. **Upload all project files**
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the app**:
   ```bash
   streamlit run app.py --server.port 8080 --server.address 0.0.0.0
   ```

### Heroku

1. **Create a new Heroku app**
2. **Add buildpack**: `heroku buildpacks:set heroku/python`
3. **Create `Procfile`**:
   ```
   web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
   ```
4. **Deploy**:
   ```bash
   git push heroku main
   ```

### Railway

1. **Connect your GitHub repository**
2. **Set environment variables** (if needed)
3. **Deploy automatically**

## Environment Variables

The application doesn't require any environment variables for basic functionality. However, you can set:

- `STREAMLIT_SERVER_PORT`: Custom port (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Server address (default: localhost)

## Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   streamlit run app.py --server.port 8502
   ```

2. **Dependencies not found**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Permission denied**:
   ```bash
   chmod +x app.py
   ```

### Performance Tips

- For large datasets (>1000 rows), consider increasing memory limits
- Use virtual environments to avoid dependency conflicts
- Monitor resource usage in cloud deployments

## Security Considerations

- The app doesn't store any user data
- All data generation happens locally
- No external API calls are made
- Generated data is temporary and not persisted

## Monitoring

For production deployments, consider:
- Application performance monitoring
- Error logging and alerting
- Resource usage monitoring
- User analytics (if needed) 