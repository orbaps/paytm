# 📋 Deployment Checklist - Smart Reserve AI

Complete this checklist to successfully deploy your application.

---

## 🔧 Pre-Deployment (Local Setup)

- [ ] Project is in GitHub repository
- [ ] Code is committed and pushed to GitHub
- [ ] All dependencies installed locally
- [ ] Frontend builds successfully: `npm run build` in phase4/frontend
- [ ] Backend runs locally: `python -m uvicorn app.main:app --reload` in phase4/backend
- [ ] Environment variables documented in `.env.example`
- [ ] Database schema works locally

---

## 🌐 Frontend Deployment (Vercel)

### Create Vercel Account
- [ ] Sign up at https://vercel.com/
- [ ] Connect GitHub account
- [ ] Create new project

### Configure Vercel Project
- [ ] Select GitHub repository
- [ ] Framework: Vite
- [ ] Build Command: `npm run build`
- [ ] Output Directory: `dist`
- [ ] Install Directory: `phase4/frontend`
- [ ] Environment Variables (leave empty for now, will add after backend)
- [ ] Deploy

### After First Deploy
- [ ] Vercel URL created: `https://_____.vercel.app`
- [ ] Save this URL for backend configuration
- [ ] Check deployment status
- [ ] Frontend loads without JavaScript errors

---

## 🔧 Backend Deployment (Railway)

### Create Railway Account
- [ ] Sign up at https://railway.app/
- [ ] Connect GitHub account

### Setup PostgreSQL Database
- [ ] Create new project
- [ ] Add PostgreSQL service
- [ ] Database created automatically
- [ ] Connection string available in env vars

### Deploy Backend Service
- [ ] Create new service from GitHub
- [ ] Select repository
- [ ] Set Root Directory: `phase4/backend`
- [ ] Railway detects Dockerfile
- [ ] Service builds and deploys
- [ ] Railway URL created: `https://_____.railway.app`

### Configure Backend Environment
- [ ] DATABASE_URL = Railway PostgreSQL (auto-set)
- [ ] Add: `CORS_ORIGIN=https://your-vercel-domain.vercel.app`
- [ ] Add: `DEBUG=false`
- [ ] Add: `PYTHONUNBUFFERED=1`
- [ ] Deployment completes

---

## 🔗 Connect Frontend to Backend

### Update Frontend Configuration
- [ ] Go to Vercel Project Settings
- [ ] Add Environment Variable:
   - Name: `VITE_API_URL`
   - Value: `https://your-railway-backend.railway.app/api/v1`
- [ ] Trigger new deployment
- [ ] Deployment completes

---

## ✅ Testing & Verification

### Frontend Testing
- [ ] Visit Vercel URL in browser
- [ ] Page loads without errors
- [ ] UI renders correctly
- [ ] No 404 errors in console
- [ ] Check DevTools for CORS errors

### Backend Testing
- [ ] Test endpoint: `curl https://backend-url.railway.app/api/v1/reserve/balance`
- [ ] Returns JSON response
- [ ] No database connection errors

### Integration Testing
- [ ] Visit frontend URL
- [ ] Dashboard loads
- [ ] Click "Refresh Analytics" button
- [ ] Data fetches from backend
- [ ] Cards populate with real data
- [ ] Charts render correctly
- [ ] No errors in browser console

### Full Feature Testing
- [ ] Quick Actions buttons work
- [ ] Modal popups open/close
- [ ] Scan QR camera requests permission
- [ ] Pay QR displays QR code
- [ ] Top Up form submits
- [ ] Notifications display
- [ ] Tab switching works
- [ ] All interactive elements functional

---

## 🐛 Common Issues & Fixes

### CORS Errors
- [ ] Check `CORS_ORIGIN` in Railway backend settings
- [ ] Ensure it matches Vercel domain exactly
- [ ] Redeploy backend
- [ ] Clear browser cache
- [ ] Test again

### API Not Responding
- [ ] Check Railway backend status
- [ ] Verify DATABASE_URL is set
- [ ] Check Railway logs for errors
- [ ] Verify backend URL is correct in Vercel env vars
- [ ] Test API directly with curl

### Database Errors
- [ ] Verify PostgreSQL is running on Railway
- [ ] Check DATABASE_URL format
- [ ] Run seed script: `python app/cli/seed_database.py`
- [ ] Check Railway Postgres logs

### Frontend Won't Load
- [ ] Check Vercel build logs
- [ ] Verify npm dependencies installed
- [ ] Check JavaScript errors in console
- [ ] Verify VITE_API_URL is set correctly
- [ ] Try hard refresh (Ctrl+Shift+R)

---

## 📊 Monitoring

### Vercel Dashboard
- [ ] Check deployment history
- [ ] View build logs
- [ ] Monitor function calls
- [ ] Track bandwidth usage
- [ ] View error logs

### Railway Dashboard
- [ ] Check backend service status
- [ ] Monitor database connections
- [ ] View service logs
- [ ] Check resource usage
- [ ] Monitor deployments

### Local Testing
- [ ] Frontend build: `npm run build` ✅
- [ ] Backend startup: `uvicorn app.main:app` ✅
- [ ] API endpoints: `curl http://localhost:8000/...` ✅

---

## 🔄 Future Deployment Updates

### When Making Changes
- [ ] Test locally first
- [ ] Commit to GitHub
- [ ] Push to GitHub
- [ ] Vercel auto-deploys (Frontend)
- [ ] Railway auto-deploys (Backend)
- [ ] Monitor logs for errors
- [ ] Verify changes live

### For Database Changes
- [ ] Test schema locally
- [ ] Update `phase4/backend/app/db/init_db.py`
- [ ] Push to GitHub
- [ ] Railway auto-deploys
- [ ] Update environment variables if needed
- [ ] Test endpoints

---

## 📝 Important URLs & Credentials

Keep these safe:

```
Frontend: https://your-project.vercel.app
Backend: https://your-backend.railway.app
GitHub: https://github.com/your-username/your-repo

Vercel Dashboard: https://vercel.com/dashboard
Railway Dashboard: https://railway.app/dashboard

Environment Variables:
- VITE_API_URL = <backend-url>/api/v1
- DATABASE_URL = <railway-postgres-url>
- CORS_ORIGIN = <vercel-frontend-url>
```

---

## ✨ Post-Deployment

- [ ] Update README with deployment info
- [ ] Document any custom configurations
- [ ] Set up monitoring alerts
- [ ] Plan backup strategy
- [ ] Document scaling plan
- [ ] Create deployment runbook
- [ ] Share with team
- [ ] Get user feedback

---

## 🎉 Deployment Complete!

Your Smart Reserve AI payment application is now live and accessible globally!

### Next Steps:
1. Share the URL with users
2. Monitor logs for issues
3. Collect user feedback
4. Plan feature improvements
5. Scale as needed

---

**Congratulations! You've successfully deployed your application! 🚀**

For support, refer to:
- VERCEL_DEPLOYMENT.md
- QUICK_DEPLOY.md
- Vercel Docs: vercel.com/docs
- Railway Docs: docs.railway.app
