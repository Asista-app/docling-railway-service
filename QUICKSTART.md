# ⚡ Quick Start - Deploy Docling to Railway in 5 Minutes

## Prerequisites
- Railway account (free tier available)
- GitHub account

## 🚀 Deploy Now (3 Steps)

### Step 1: Push to GitHub (2 minutes)
```bash
cd /Users/ahmed.hassouna/Dev/Docling

# Initialize git
git init
git add .
git commit -m "Initial commit"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/docling-railway.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Railway (2 minutes)
1. Go to https://railway.app/new
2. Click "Deploy from GitHub repo"
3. Select your `docling-railway` repository
4. Wait for build to complete (~5-10 minutes)

### Step 3: Get Your URL (1 minute)
1. In Railway dashboard, go to Settings
2. Click "Generate Domain"
3. Copy your URL: `https://your-app.railway.app`

## ✅ Test Your Deployment

```bash
# Replace with your Railway URL
export API_URL="https://your-app.railway.app"

# Test health
curl $API_URL/health

# Convert a PDF
curl -X POST "$API_URL/convert/url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://arxiv.org/pdf/2408.09869", "output_format": "markdown"}'
```

## 📖 View API Documentation
Open in browser: `https://your-app.railway.app/docs`

## 🎯 What You Get

- ✅ REST API for document conversion
- ✅ Support for PDF, DOCX, HTML, and more
- ✅ Multiple output formats (Markdown, JSON, HTML)
- ✅ Automatic scaling
- ✅ HTTPS enabled
- ✅ Interactive API documentation

## 📁 Project Files

| File | Purpose |
|------|---------|
| `main.py` | FastAPI application |
| `Dockerfile` | Container configuration |
| `requirements.txt` | Python dependencies |
| `railway.toml` | Railway settings |
| `README.md` | Full documentation |
| `DEPLOYMENT_GUIDE.md` | Detailed deployment steps |
| `test_api.py` | API testing script |
| `example_client.py` | Usage examples |

## 🔧 Common Commands

```bash
# Test locally
pip install -r requirements.txt
python main.py

# Run tests
python test_api.py

# View examples
python example_client.py
```

## 💡 Tips

1. **Free Tier**: Railway offers $5 free credit monthly
2. **Monitoring**: Check logs in Railway dashboard
3. **Scaling**: Upgrade plan for more resources
4. **Custom Domain**: Add in Railway settings

## 📞 Need Help?

- **Full docs**: See `README.md`
- **Deployment guide**: See `DEPLOYMENT_GUIDE.md`
- **Railway help**: https://railway.app/help
- **Docling docs**: https://docling-project.github.io/docling/

---

**That's it!** Your Docling service is now live! 🎉
