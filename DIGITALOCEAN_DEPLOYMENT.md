# Deploying to DigitalOcean App Platform

This guide will help you deploy the Alzheimer's Risk Prediction Platform to DigitalOcean App Platform.

## Why DigitalOcean?

### Advantages
- **Predictable pricing**: $5/month for basic apps (no free tier surprises)
- **Better performance**: Dedicated resources from start
- **No cold starts**: App is always running
- **Simple interface**: Easy to use dashboard
- **Great documentation**: Comprehensive guides
- **Global CDN**: Fast content delivery

### Comparison with Render

| Feature | DigitalOcean | Render |
|---------|--------------|--------|
| Free Tier | No | Yes (750hrs) |
| Starter Price | $5/month | $7/month |
| Cold Starts | No | Yes (free tier) |
| Performance | Better | Good |
| Ease of Setup | Easy | Very Easy |

---

## Prerequisites

- DigitalOcean account (https://cloud.digitalocean.com)
- GitHub account with your repository
- Credit card for account verification (even for free trial)

---

## Deployment Methods

### Method 1: Using App Spec (Recommended)

This uses a YAML file similar to render.yaml for automated deployment.

### Method 2: Dashboard Setup

Manual setup through DigitalOcean's web interface.

---

## Method 1: App Spec Deployment

### Step 1: Create App Spec File

The `.do/app.yaml` file has already been created in your project.

### Step 2: Push to GitHub

```bash
cd "F:\Cs\Projects\DEPI\DEPI Grad Project\Alzheimer"
git add .
git commit -m "Add DigitalOcean deployment configuration"
git push origin main
```

### Step 3: Create App on DigitalOcean

1. Go to https://cloud.digitalocean.com/apps
2. Click **"Create App"**
3. Choose **GitHub** as source
4. Authorize DigitalOcean to access your GitHub
5. Select repository: **ShadyKishk77/Alzheimer-Risk-Prediction**
6. Select branch: **main**
7. DigitalOcean auto-detects Python app
8. Click **"Next"**

### Step 4: Configure Resources

**App Name**: `alzheimer-risk-prediction`

**Component Settings**:
- **Type**: Web Service
- **Name**: web
- **Source Directory**: `/`
- **Build Command**: `pip install -r requirements.txt && python scripts/regenerate_models.py`
- **Run Command**: `uvicorn api.main:app --host 0.0.0.0 --port 8080`
- **HTTP Port**: 8080
- **Health Check**: `/health`

**Instance Size**:
- **Basic** ($5/month): 512 MB RAM, 1 vCPU - Recommended for demo/testing
- **Professional** ($12/month): 1 GB RAM, 1 vCPU - Better for production

### Step 5: Environment Variables

Add these in the "Environment Variables" section:

```
ENVIRONMENT=production
LOG_LEVEL=info
PYTHON_VERSION=3.9
```

### Step 6: Deploy

1. Review configuration
2. Click **"Create Resources"**
3. Wait 5-10 minutes for build and deployment

### Step 7: Access Your App

Once deployed, your app will be at:
```
https://alzheimer-risk-prediction-xxxxx.ondigitalocean.app
```

Test endpoints:
- Main app: https://your-app.ondigitalocean.app
- Health: https://your-app.ondigitalocean.app/health
- API docs: https://your-app.ondigitalocean.app/docs

---

## Method 2: Dashboard Setup (Manual)

### Step 1: Go to Apps

1. Log into https://cloud.digitalocean.com
2. Click **"Create"** → **"Apps"**
3. Or go directly to: https://cloud.digitalocean.com/apps/new

### Step 2: Connect Repository

1. Choose **"GitHub"** as source
2. Authorize DigitalOcean
3. Select your repository: **Alzheimer-Risk-Prediction**
4. Select branch: **main**
5. Click **"Next"**

### Step 3: Configure App

**General Settings**:
```
App Name: alzheimer-risk-prediction
Region: New York (or closest to you)
```

**Web Service Configuration**:
```
Environment: Python
Build Command: pip install -r requirements.txt && python scripts/regenerate_models.py
Run Command: uvicorn api.main:app --host 0.0.0.0 --port 8080
HTTP Port: 8080
Health Check Path: /health
```

**Plan**:
- Basic ($5/month) - 512 MB RAM, 1 vCPU
- Professional ($12/month) - 1 GB RAM, 1 vCPU

### Step 4: Environment Variables (Optional)

```
ENVIRONMENT=production
LOG_LEVEL=info
```

### Step 5: Launch

1. Review all settings
2. Click **"Launch Basic App"** or **"Launch Professional App"**
3. Wait for deployment

---

## App Spec YAML Configuration

If you want to use infrastructure-as-code, create `.do/app.yaml`:

```yaml
name: alzheimer-risk-prediction
region: nyc
services:
  - name: web
    github:
      repo: ShadyKishk77/Alzheimer-Risk-Prediction
      branch: main
      deploy_on_push: true
    build_command: pip install -r requirements.txt && python scripts/regenerate_models.py
    run_command: uvicorn api.main:app --host 0.0.0.0 --port 8080
    environment_slug: python
    envs:
      - key: ENVIRONMENT
        value: production
      - key: LOG_LEVEL
        value: info
    health_check:
      http_path: /health
    http_port: 8080
    instance_count: 1
    instance_size_slug: basic-xxs
```

Deploy with:
```bash
doctl apps create --spec .do/app.yaml
```

---

## Pricing

### Basic Plan ($5/month)
- 512 MB RAM
- 1 vCPU
- 1 GB storage
- 40 GB bandwidth
- Perfect for: Demos, portfolios, small projects

### Professional Plans
- **$12/month**: 1 GB RAM, 1 vCPU
- **$24/month**: 2 GB RAM, 2 vCPU
- **$48/month**: 4 GB RAM, 4 vCPU

### Free Trial
- DigitalOcean often provides $200 credit for 60 days
- Check for promo codes when signing up

---

## Custom Domain Setup

### Step 1: Add Domain

1. Go to your app in DigitalOcean dashboard
2. Click **"Settings"** → **"Domains"**
3. Click **"Add Domain"**
4. Enter your domain: `alzheimer-prediction.yourdomain.com`

### Step 2: Update DNS

Add these DNS records at your domain provider:

```
Type: CNAME
Name: alzheimer-prediction
Value: your-app.ondigitalocean.app
TTL: 3600
```

### Step 3: Verify

Wait 5-60 minutes for DNS propagation, then access:
```
https://alzheimer-prediction.yourdomain.com
```

---

## Environment Variables

### Required
None (app works with defaults)

### Recommended
```
ENVIRONMENT=production
LOG_LEVEL=info
PYTHON_VERSION=3.9
```

### For Production
```
CORS_ORIGINS=["https://yourdomain.com"]
MAX_REQUEST_SIZE=1048576
```

---

## Monitoring & Logs

### View Logs

1. Go to your app in DigitalOcean
2. Click **"Runtime Logs"**
3. Real-time logs appear

Or use CLI:
```bash
doctl apps logs <app-id> --type run
```

### Metrics

1. Click **"Insights"** tab
2. View:
   - CPU usage
   - Memory usage
   - Bandwidth
   - Request count
   - Response times

### Alerts

Set up alerts for:
- High CPU usage (>80%)
- High memory usage (>90%)
- Error rate spikes
- Downtime

---

## Scaling

### Horizontal Scaling

Increase instance count:

1. Go to app → **Components** → **web**
2. Change **Instance Count**: 1 → 2 or more
3. Click **"Save"**
4. Load balancer automatically distributes traffic

### Vertical Scaling

Upgrade instance size:

1. Go to app → **Components** → **web**
2. Change **Instance Size**: 
   - Basic ($5) → Professional ($12)
   - Professional-XS ($12) → Professional-S ($24)
3. Click **"Save"**
4. Brief restart required

---

## Continuous Deployment

### Auto-Deploy on Push

1. Go to app → **Settings** → **App Settings**
2. Under **Source**, check:
   - ✅ **Autodeploy**: ON
3. Now every push to `main` branch triggers deployment

### Manual Deployment

```bash
# Using DigitalOcean CLI
doctl apps create-deployment <app-id>
```

Or click **"Deploy"** in dashboard.

---

## Troubleshooting

### Build Fails

**Issue**: Dependencies not installing

**Fix**:
```bash
# Test locally
pip install -r requirements.txt
python scripts/regenerate_models.py

# Check requirements.txt is complete
# Verify Python 3.9 compatibility
```

### App Crashes on Start

**Issue**: Import errors or missing models

**Check**:
1. Build logs for errors
2. Run command is correct
3. Port 8080 is used (not 8000)

**Fix**:
```bash
# Update run command to use port 8080
uvicorn api.main:app --host 0.0.0.0 --port 8080
```

### Health Check Fails

**Issue**: App running but health check failing

**Fix**:
1. Verify `/health` endpoint works locally
2. Check health check path: `/health` (not `/health/`)
3. Increase health check timeout

### High Memory Usage

**Issue**: App uses >90% RAM

**Solutions**:
1. Upgrade to larger instance
2. Optimize model loading
3. Add memory limits in code

---

## Security Best Practices

### 1. Update CORS

In `api/config.py`:
```python
CORS_ORIGINS: List[str] = [
    "https://alzheimer-prediction.yourdomain.com",
    "https://your-app.ondigitalocean.app"
]
```

### 2. Add Rate Limiting

```python
# In api/main.py
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.post("/predict")
@limiter.limit("10/minute")
async def predict(...):
    ...
```

### 3. Use Environment Variables

Store secrets in app settings, not code:
```python
API_KEY = os.getenv("API_KEY")
```

### 4. Enable HTTPS

DigitalOcean provides automatic HTTPS with Let's Encrypt.

---

## Cost Optimization

### For Demo/Portfolio
- Use **Basic** plan ($5/month)
- Single instance
- Scale up only when needed

### For Production
- Start with **Professional-XS** ($12/month)
- Add monitoring
- Scale horizontally for high traffic

### For Development
- Use free trial credits ($200 for 60 days)
- Destroy app when not testing

---

## Backup & Recovery

### Database Backups
Not applicable (stateless app, no database)

### Model Files
Models regenerate on deployment from code

### Configuration Backup
- App spec stored in `.do/app.yaml`
- All settings in Git repository

---

## Migration from Render

If moving from Render to DigitalOcean:

1. Same codebase works on both platforms
2. Update start command port: 8000 → 8080
3. Update environment variables
4. Point DNS to new DigitalOcean URL
5. Test thoroughly before switching

---

## DigitalOcean CLI Setup (Optional)

### Install CLI

**Windows**:
```powershell
iwr -useb https://github.com/digitalocean/doctl/releases/download/v1.94.0/doctl-1.94.0-windows-amd64.zip -OutFile doctl.zip
Expand-Archive doctl.zip
Move-Item doctl\doctl.exe C:\Windows\System32\
```

**Linux/Mac**:
```bash
brew install doctl  # Mac
snap install doctl  # Linux
```

### Authenticate

```bash
doctl auth init
# Enter your API token from: https://cloud.digitalocean.com/account/api/tokens
```

### Deploy via CLI

```bash
# Create app from spec
doctl apps create --spec .do/app.yaml

# List apps
doctl apps list

# Get app info
doctl apps get <app-id>

# View logs
doctl apps logs <app-id> --type run

# Create deployment
doctl apps create-deployment <app-id>
```

---

## Support Resources

- **DigitalOcean Docs**: https://docs.digitalocean.com/products/app-platform/
- **Community**: https://www.digitalocean.com/community
- **Status**: https://status.digitalocean.com
- **Tutorials**: https://www.digitalocean.com/community/tutorials

---

## Comparison: DigitalOcean vs Render vs Others

| Feature | DigitalOcean | Render | Heroku | Railway |
|---------|--------------|--------|--------|---------|
| Free Tier | No | Yes | No | Yes |
| Min Price | $5/mo | $7/mo | $7/mo | $5/mo |
| Cold Starts | No | Yes (free) | No | No |
| Auto-scale | Yes | Yes | Yes | Limited |
| Custom Domain | Yes | Yes (paid) | Yes | Yes |
| Database | Add-on | Add-on | Add-on | Included |
| Regions | 8+ | 3 | Many | 5 |
| Performance | Excellent | Good | Good | Good |
| Setup | Easy | Easy | Easy | Easy |

**Choose DigitalOcean if**:
- You want predictable pricing
- No cold starts required
- Need better performance from start
- Want room to grow (droplets, kubernetes, etc.)

**Choose Render if**:
- You want free tier for demos
- Okay with cold starts
- Simple project

---

## Success Checklist

Before deploying:
- [ ] GitHub repository up to date
- [ ] DigitalOcean account created
- [ ] Payment method added
- [ ] Region selected (closest to users)
- [ ] Plan chosen (Basic for start)

After deployment:
- [ ] App shows "Deployed" status
- [ ] Health endpoint returns 200
- [ ] Web interface loads
- [ ] Predictions work
- [ ] Custom domain configured (optional)
- [ ] Monitoring set up

---

## Next Steps

1. **Sign up**: https://cloud.digitalocean.com (get $200 credit with promo)
2. **Deploy**: Follow Method 1 or Method 2 above
3. **Test**: Verify all endpoints work
4. **Monitor**: Set up alerts and check logs
5. **Scale**: Upgrade plan when needed

---

## Estimated Costs

**Basic Setup**:
- App Platform Basic: $5/month
- Bandwidth: Included (40 GB)
- Total: **$5/month**

**Production Setup**:
- App Platform Professional: $12/month
- Custom domain: $0 (if you own domain)
- CDN: $0 (included)
- Total: **$12/month**

**With Database** (if needed later):
- Managed PostgreSQL: +$15/month (basic)
- Redis: +$15/month (basic)

---

Your Alzheimer's Risk Prediction Platform is ready to deploy on DigitalOcean! Choose your preferred method above and follow the steps. The app will be live in about 10 minutes.
