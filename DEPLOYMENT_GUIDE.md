# 🚀 Quick Deployment Guide for Railway

## Step-by-Step Deployment Process

### Step 1: Prepare Your Repository

1. **Initialize Git repository:**
   ```bash
   cd /Users/ahmed.hassouna/Dev/Docling
   git init
   git add .
   git commit -m "Initial commit: Docling web service for Railway"
   ```

2. **Create a GitHub repository:**
   - Go to https://github.com/new
   - Name it: `docling-railway-service`
   - Don't initialize with README (we already have one)
   - Click "Create repository"

3. **Push to GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/docling-railway-service.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Railway

#### Option A: Deploy from GitHub (Easiest)

1. **Go to Railway:**
   - Visit https://railway.app/
   - Sign in or create an account

2. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your GitHub
   - Select your `docling-railway-service` repository

3. **Railway Auto-Detection:**
   - Railway will automatically detect the `Dockerfile`
   - It will start building immediately
   - Wait for the build to complete (5-10 minutes)

4. **Generate Domain:**
   - Go to your project settings
   - Click "Generate Domain" under "Networking"
   - Copy your URL: `https://your-app.railway.app`

#### Option B: Deploy using Railway CLI

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   # or
   brew install railway
   ```

2. **Login:**
   ```bash
   railway login
   ```

3. **Initialize Project:**
   ```bash
   cd /Users/ahmed.hassouna/Dev/Docling
   railway init
   ```
   - Select "Create new project"
   - Give it a name: "docling-service"

4. **Deploy:**
   ```bash
   railway up
   ```

5. **Get Your URL:**
   ```bash
   railway domain
   ```

### Step 3: Verify Deployment

1. **Check Health:**
   ```bash
   curl https://your-app.railway.app/health
   ```
   Expected response: `{"status":"healthy"}`

2. **Test API:**
   ```bash
   curl -X POST "https://your-app.railway.app/convert/url" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://arxiv.org/pdf/2408.09869", "output_format": "markdown"}'
   ```

3. **View API Docs:**
   Open in browser: `https://your-app.railway.app/docs`

### Step 4: Monitor Your Service

1. **View Logs:**
   - In Railway dashboard, click on your project
   - Go to "Deployments" tab
   - Click on the latest deployment
   - View real-time logs

2. **Check Metrics:**
   - CPU usage
   - Memory usage
   - Request count

### Step 5: Configure (Optional)

#### Add Custom Domain
1. In Railway dashboard, go to Settings
2. Click "Add Custom Domain"
3. Follow DNS configuration instructions

#### Set Environment Variables
1. Go to Variables tab
2. Add any custom variables you need
3. Redeploy if necessary

## 🔍 Troubleshooting

### Build Fails
- **Check logs** in Railway dashboard
- **Common issues:**
  - Dockerfile syntax errors
  - Missing dependencies
  - Python version compatibility

### Service Won't Start
- **Check health check timeout** (set to 300s in railway.toml)
- **Verify PORT variable** is being used correctly
- **Check memory limits** (upgrade plan if needed)

### Slow Response Times
- **Large documents** take time to process
- **Consider upgrading** to a higher Railway plan
- **Add caching** for frequently accessed documents

## 📊 Resource Requirements

### Minimum (Hobby Plan)
- **Memory**: 512MB
- **CPU**: Shared
- **Cost**: $5/month
- **Good for**: Testing, small documents

### Recommended (Pro Plan)
- **Memory**: 2GB+
- **CPU**: 1 vCPU
- **Cost**: ~$20/month
- **Good for**: Production, large PDFs

### Heavy Usage
- **Memory**: 4GB+
- **CPU**: 2+ vCPU
- **Cost**: Custom pricing
- **Good for**: High traffic, concurrent requests

## 🎯 Next Steps After Deployment

1. ✅ Test all endpoints
2. ✅ Set up monitoring/alerts
3. ✅ Configure custom domain (optional)
4. ✅ Add authentication if needed
5. ✅ Set up CI/CD for automatic deployments
6. ✅ Monitor costs and usage

## 📞 Getting Help

- **Railway Issues**: https://railway.app/help
- **Docling Issues**: https://github.com/docling-project/docling/issues
- **API Documentation**: Check `/docs` endpoint on your deployment

## 🎉 Success Checklist

- [ ] Repository created and pushed to GitHub
- [ ] Railway project created
- [ ] Service deployed successfully
- [ ] Health check passing
- [ ] API endpoints responding
- [ ] Documentation accessible at `/docs`
- [ ] Test conversion working
- [ ] Domain configured (optional)
- [ ] Monitoring set up

---

**Congratulations!** Your Docling service is now live on Railway! 🚀
