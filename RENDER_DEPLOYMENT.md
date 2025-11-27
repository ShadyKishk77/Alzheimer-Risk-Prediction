# Deploying to Render

This guide will help you deploy the Alzheimer's Risk Prediction Platform to Render.

## Prerequisites

- GitHub account
- Render account (free tier available at https://render.com)
- Project pushed to GitHub repository

## Step 1: Prepare Your Repository

Ensure these files are in your repository:
- `render.yaml` - Render service configuration
- `build.sh` - Build script for deploying
- `requirements.txt` - Python dependencies
- `api/`, `models/`, `web/`, `data/` folders

## Step 2: Create Render Account

1. Go to https://render.com
2. Sign up with your GitHub account
3. Authorize Render to access your repositories

## Step 3: Deploy from Dashboard

### Option A: Using Blueprint (Recommended)

1. Click "New +" button → "Blueprint"
2. Connect your GitHub repository
3. Render will automatically detect `render.yaml`
4. Click "Apply"
5. Wait for deployment (5-10 minutes first time)

### Option B: Manual Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `alzheimer-risk-prediction`
   - **Region**: Oregon (US West)
   - **Branch**: `main`
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
4. Click "Create Web Service"

## Step 4: Environment Variables (Optional)

Add these in Render dashboard under "Environment":

```
ENVIRONMENT=production
PYTHON_VERSION=3.9.0
```

## Step 5: Verify Deployment

Once deployed, Render will provide a URL like:
```
https://alzheimer-risk-prediction.onrender.com
```

Test these endpoints:
- Main app: `https://your-app.onrender.com/`
- Health check: `https://your-app.onrender.com/health`
- API docs: `https://your-app.onrender.com/docs`

## Step 6: Monitor Your Service

- View logs in Render dashboard
- Check deployment status
- Monitor performance metrics

## Render Free Tier Limitations

- Service spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- 750 hours/month free
- Shared CPU/RAM

## Upgrading to Paid Tier

For production use, upgrade to paid tier ($7/month):
- No spin-down
- Faster performance
- More resources
- Custom domains

## Troubleshooting

### Build Fails

**Issue**: Missing dependencies
```bash
# Check requirements.txt includes all packages
# Verify Python version compatibility
```

**Issue**: Model generation fails
```bash
# Check data/ folder exists with CSV files
# Verify scripts/regenerate_models.py is present
```

### Service Won't Start

**Issue**: Port binding error
```bash
# Ensure start command uses $PORT variable:
uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

**Issue**: Import errors
```bash
# Check all __init__.py files exist
# Verify module paths in imports
```

### Slow First Request

This is normal on free tier due to spin-down. Solutions:
- Upgrade to paid tier
- Use a keep-alive service (ping every 14 minutes)
- Accept cold starts for demo/portfolio projects

## Custom Domain (Paid)

1. Go to service settings
2. Add custom domain
3. Update DNS records with your provider
4. Enable automatic HTTPS

## Continuous Deployment

Render automatically redeploys when you push to your main branch:

```bash
git add .
git commit -m "Update model"
git push origin main
```

Render will:
1. Pull latest code
2. Run build.sh
3. Restart service
4. Deploy updates

## Cost Estimation

**Free Tier**: $0/month
- Perfect for portfolio/demo
- Spins down after inactivity

**Starter**: $7/month
- Always-on service
- Better performance
- 0.5 GB RAM

**Standard**: $25/month
- Production-ready
- 2 GB RAM
- Faster CPU

## Security Recommendations

For production deployment:

1. **Update CORS origins** in `api/config.py`:
```python
CORS_ORIGINS: List[str] = ["https://yourdomain.com"]
```

2. **Add authentication** for sensitive endpoints

3. **Enable HTTPS** (automatic on Render)

4. **Set environment variables** for secrets

5. **Monitor logs** for unusual activity

## Backup Strategy

- Models auto-regenerate on deployment
- Database: Not applicable (stateless service)
- Data files: Committed to Git repository

## Support

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- Project Issues: GitHub repository issues

## Alternative Deployment Options

If Render doesn't meet your needs:

- **Heroku**: Similar PaaS, paid only
- **Railway**: Free tier with better limits
- **Fly.io**: Edge deployment
- **AWS/Azure/GCP**: Full control, more complex
- **Docker + VPS**: Self-hosted option

## Success Checklist

- [ ] Project pushed to GitHub
- [ ] render.yaml configured
- [ ] build.sh is executable
- [ ] requirements.txt complete
- [ ] Render account created
- [ ] Service deployed successfully
- [ ] Health endpoint returns "healthy"
- [ ] Web interface loads correctly
- [ ] Predictions work as expected
- [ ] API documentation accessible

Your Alzheimer's Risk Prediction Platform is now live on the internet!
