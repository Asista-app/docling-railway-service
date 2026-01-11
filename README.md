# Docling Web Service for Railway

A FastAPI-based web service that wraps the [Docling](https://github.com/docling-project/docling) library (v2.67.0) for document conversion, deployed on Railway.

## 🚀 Features

- Convert documents from URLs (PDF, DOCX, HTML, etc.)
- Upload and convert local files
- Multiple output formats: Markdown, JSON, HTML
- RESTful API with automatic documentation
- Health check endpoints for monitoring
- CORS enabled for cross-origin requests

## 📋 Prerequisites

- Railway account ([sign up here](https://railway.app/))
- Git installed locally
- GitHub account (optional, for GitHub integration)

## 🛠️ Deployment Steps

### Option 1: Deploy from GitHub (Recommended)

1. **Push this code to GitHub:**
   ```bash
   cd /Users/ahmed.hassouna/Dev/Docling
   git init
   git add .
   git commit -m "Initial commit: Docling web service"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Railway:**
   - Go to [Railway Dashboard](https://railway.app/dashboard)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will automatically detect the Dockerfile and deploy

3. **Configure Environment (Optional):**
   - Railway will automatically set the `PORT` variable
   - No additional environment variables needed for basic setup

### Option 2: Deploy using Railway CLI

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Initialize and Deploy:**
   ```bash
   cd /Users/ahmed.hassouna/Dev/Docling
   railway init
   railway up
   ```

4. **Get your deployment URL:**
   ```bash
   railway domain
   ```

## 📡 API Endpoints

Once deployed, your service will be available at `https://your-app.railway.app`

### 1. Health Check
```bash
GET /health
```

### 2. Convert from URL
```bash
POST /convert/url
Content-Type: application/json

{
  "url": "https://arxiv.org/pdf/2408.09869",
  "output_format": "markdown"
}
```

**Example with curl:**
```bash
curl -X POST "https://your-app.railway.app/convert/url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://arxiv.org/pdf/2408.09869", "output_format": "markdown"}'
```

### 3. Convert from File Upload
```bash
POST /convert/file
Content-Type: multipart/form-data

file: [your-file]
output_format: markdown
```

**Example with curl:**
```bash
curl -X POST "https://your-app.railway.app/convert/file" \
  -F "file=@/path/to/document.pdf" \
  -F "output_format=markdown"
```

### 4. API Documentation
Access interactive API docs at:
- Swagger UI: `https://your-app.railway.app/docs`
- ReDoc: `https://your-app.railway.app/redoc`

## 🧪 Local Testing

Before deploying, you can test locally:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```bash
   python main.py
   ```

3. **Test the API:**
   ```bash
   # Health check
   curl http://localhost:8000/health
   
   # Convert a document
   curl -X POST "http://localhost:8000/convert/url" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://arxiv.org/pdf/2408.09869", "output_format": "markdown"}'
   ```

## 🐳 Docker Testing

Test the Docker container locally:

```bash
# Build the image
docker build -t docling-service .

# Run the container
docker run -p 8000:8000 docling-service

# Test
curl http://localhost:8000/health
```

## 📊 Supported Formats

### Input Formats
- PDF
- DOCX (Microsoft Word)
- PPTX (Microsoft PowerPoint)
- HTML
- Images (with OCR)
- Markdown
- AsciiDoc
- XLSX (Excel)

### Output Formats
- `markdown` - Markdown format
- `json` - JSON structure
- `html` - HTML format

## ⚙️ Configuration

### Environment Variables

Railway automatically sets:
- `PORT` - The port your application should listen on

Optional variables you can add:
- `LOG_LEVEL` - Logging level (default: INFO)

### Resource Requirements

Recommended Railway plan:
- **Memory**: 2GB minimum (4GB recommended for large documents)
- **CPU**: 1 vCPU minimum

## 🔧 Troubleshooting

### Build Failures
- Check Railway build logs for specific errors
- Ensure all dependencies in `requirements.txt` are compatible
- System dependencies are installed in the Dockerfile

### Memory Issues
- Upgrade your Railway plan for more memory
- Large PDF files may require more resources

### Timeout Issues
- Increase `healthcheckTimeout` in `railway.toml`
- For large documents, consider implementing async processing

## 📝 Project Structure

```
.
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── railway.toml        # Railway configuration
├── railway.json        # Alternative Railway config
└── README.md           # This file
```

## 🔗 Useful Links

- [Docling Documentation](https://docling-project.github.io/docling/)
- [Docling GitHub](https://github.com/docling-project/docling)
- [Docling Changelog](https://github.com/docling-project/docling/blob/main/CHANGELOG.md)
- [Railway Documentation](https://docs.railway.app/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 📄 License

This wrapper service follows the same MIT license as Docling.

## 🤝 Support

For issues related to:
- **Docling library**: [Docling Issues](https://github.com/docling-project/docling/issues)
- **This wrapper service**: Create an issue in your repository
- **Railway deployment**: [Railway Support](https://railway.app/help)

## 🎯 Next Steps

After deployment:
1. Test all endpoints using the `/docs` interface
2. Monitor your application in Railway dashboard
3. Set up custom domain (optional)
4. Configure environment variables as needed
5. Monitor logs for any issues

---

**Ready to deploy?** Follow the deployment steps above and your Docling service will be live in minutes! 🚀
