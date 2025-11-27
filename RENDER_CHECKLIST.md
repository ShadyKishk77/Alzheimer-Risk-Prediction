# Render Deployment Checklist

Use this checklist before deploying to Render.

## Pre-Deployment

- [ ] All code committed to Git
- [ ] GitHub repository is public or Render has access
- [ ] `render.yaml` exists in root directory
- [ ] `build.sh` exists and is executable
- [ ] `requirements.txt` includes all dependencies
- [ ] Model files exist in `models/` OR regeneration script works
- [ ] No secrets/API keys in code (use environment variables)
- [ ] Test locally: `python api/start_api.py`
- [ ] Local health check works: http://localhost:8000/health

## Files Required

- [ ] `render.yaml` - Service configuration
- [ ] `build.sh` - Build script
- [ ] `requirements.txt` - Python dependencies
- [ ] `api/main.py` - FastAPI application
- [ ] `api/config.py` - Configuration
- [ ] `models/` folder OR `scripts/regenerate_models.py`
- [ ] `data/` folder with CSV files (if regenerating models)

## Render Setup

- [ ] Render account created at https://render.com
- [ ] GitHub account connected to Render
- [ ] Repository access authorized

## Deployment Steps

### Option 1: Blueprint (Recommended)

- [ ] Log into Render dashboard
- [ ] Click "New +" → "Blueprint"
- [ ] Select your GitHub repository
- [ ] Verify `render.yaml` detected
- [ ] Click "Apply"
- [ ] Wait for build (5-10 minutes first time)
- [ ] Note the deployed URL

### Option 2: Manual Web Service

- [ ] Click "New +" → "Web Service"
- [ ] Connect GitHub repository
- [ ] Name: `alzheimer-risk-prediction`
- [ ] Region: Oregon (or closest to you)
- [ ] Branch: `main`
- [ ] Runtime: Python 3
- [ ] Build Command: `./build.sh`
- [ ] Start Command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
- [ ] Click "Create Web Service"

## Post-Deployment Verification

- [ ] Service shows "Live" status in Render dashboard
- [ ] Main page loads: `https://your-app.onrender.com`
- [ ] Health check works: `https://your-app.onrender.com/health`
- [ ] API docs accessible: `https://your-app.onrender.com/docs`
- [ ] Can make test prediction via web interface
- [ ] No errors in Render logs

## Testing Endpoints

Test these URLs (replace with your actual Render URL):

```bash
# Health check
curl https://your-app.onrender.com/health

# Features endpoint
curl https://your-app.onrender.com/features

# Test prediction (using curl)
curl -X POST https://your-app.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [75, 1, 2, 12, 28.5, 0, 3, 2.5, 6, 5, 1, 0, 1, 0, 0, 1, 145, 88, 220, 140, 50, 180, 22, 6.5, 1, 0, 7, 1, 0, 0, 1, 1],
    "patient_id": "TEST-001"
  }'
```

## Common Issues

### Build Fails

**Issue**: Dependencies not installing
- [ ] Check `requirements.txt` is complete
- [ ] Verify Python version compatibility
- [ ] Review build logs in Render dashboard

**Issue**: Model generation fails
- [ ] Verify `data/` folder exists with CSV files
- [ ] Check `scripts/regenerate_models.py` runs locally
- [ ] Review build script output

### Service Won't Start

**Issue**: Import errors
- [ ] All `__init__.py` files present
- [ ] Module paths correct in imports
- [ ] Check start command uses correct path

**Issue**: Port binding error
- [ ] Start command includes `--port $PORT`
- [ ] Not hardcoding port number

### Slow Performance

**Issue**: Cold starts (free tier)
- [ ] Expected behavior on free tier
- [ ] First request takes 30-60 seconds after spin-down
- [ ] Consider upgrading to paid tier ($7/month) for always-on

## Optional Enhancements

- [ ] Add custom domain (paid tier only)
- [ ] Set up environment variables for secrets
- [ ] Configure auto-scaling (paid tier)
- [ ] Add health check pinging to prevent spin-down
- [ ] Set up monitoring/alerting
- [ ] Configure CDN for static files

## Documentation Updates

After successful deployment:

- [ ] Update README.md with live URL
- [ ] Add deployment badge to README
- [ ] Document any deployment-specific configuration
- [ ] Update API documentation with production URL

## Continuous Deployment

Render auto-deploys on push to main branch:

- [ ] Test changes locally before pushing
- [ ] Use meaningful commit messages
- [ ] Monitor deployment in Render dashboard
- [ ] Verify deployment succeeded before announcing

## Success Criteria

Your deployment is successful when:

- [x] Service status shows "Live"
- [x] All health checks pass
- [x] Web interface loads and works
- [x] Predictions return valid results
- [x] No errors in logs
- [x] Response times acceptable (<5 seconds including cold start)

## Free Tier Limitations

Be aware of these limits:

- Service spins down after 15 minutes inactivity
- 750 hours/month free (enough for one always-on service)
- Shared resources (slower than paid)
- Cold start adds 30-60 seconds to first request
- No custom domains on free tier

## Upgrade to Paid ($7/month)

Consider upgrading if you need:

- Always-on service (no spin-down)
- Faster response times
- More RAM/CPU
- Custom domains
- Better support

## Rollback Plan

If deployment fails:

- [ ] Check Render logs for errors
- [ ] Revert to last working commit: `git revert HEAD`
- [ ] Redeploy previous version
- [ ] Fix issues locally before redeploying

## Support Resources

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- Project GitHub Issues: For project-specific problems

## Final Verification

Once everything works:

- [ ] Share live URL with team/stakeholders
- [ ] Add to portfolio/resume
- [ ] Update project documentation
- [ ] Monitor usage and performance
- [ ] Plan future improvements

---

**Deployment Complete!** 

Your Alzheimer's Risk Prediction Platform is now live on the internet at:
`https://your-app-name.onrender.com`
