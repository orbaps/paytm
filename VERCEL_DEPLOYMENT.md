# 🚀 Smart Reserve AI - Complete Deployment Guide

This guide walks you through deploying your Smart Reserve AI payment application to Vercel (Frontend) and Railway (Backend).

## 📋 Prerequisites

- GitHub account with your code pushed
- Vercel account (free at vercel.com)
- Railway account (free at railway.app)
- Node.js and npm installed
- Vercel CLI installed: `npm install -g vercel`

---

## 🎯 Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        VERCEL (Frontend)                     │
│        Smart Reserve React App (Vite)                        │
│        https://smart-reserve.vercel.app                      │
└─────────────────────┬──────────────────────────────────────┘
                      │
                      │ API Calls
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    RAILWAY (Backend)                         │
│        FastAPI Python Server                                 │
│        https://smart-reserve-api.railway.app                │
│                      │                                       │
│                      ▼                                       │
│            ┌──────────────────┐                             │
│            │  PostgreSQL DB   │                             │
│            │  (Railway)       │                             │
│            └──────────────────┘                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Step 1: Prepare Local Build

### Build and test locally first

```bash
# Navigate to frontend
cd phase4/frontend

# Install dependencies
npm install

# Build for production
npm run build

# Test the build
npm run preview
```

Verify that everything works at `http://localhost:4173/`

---

## 🌐 Step 2: Deploy Frontend to Vercel

### Option A: Using Vercel CLI (Recommended)

```bash
# From project root
cd phase4/frontend

# Login to Vercel
vercel login

# Deploy to production
vercel deploy --prod
```

### Option B: GitHub Integration (Easier for future deploys)

1. Push your code to GitHub
2. Go to https://vercel.com/
3. Click "New Project"
4. Select your GitHub repo
5. Configure settings:
   - Framework: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Environment Variables:
     ```
     VITE_API_URL=https://your-backend-api.railway.app/api/v1
     ```
6. Click "Deploy"

✅ **Frontend is now live at:** `https://your-project-name.vercel.app`

---

## 🔧 Step 3: Deploy Backend to Railway

### 1. Create Railway Account
- Go to https://railway.app/
- Sign up with GitHub

### 2. Create New Project
- Click "New Project"
- Select "Deploy from GitHub"
- Choose your Paytm repository
- Select "Confirm"

### 3. Add PostgreSQL Database
- Click "Add Service"
- Select "PostgreSQL"
- Railway creates the database automatically

### 4. Configure Backend Service
- Click "New Service"
- Select "Docker" or "GitHub"
- Configure:
  - **Root Directory:** `phase4/backend`
  - **Dockerfile:** Located at `phase4/backend/Dockerfile`
  - **PORT:** 8000 (Railway auto-detects)

### 5. Add Environment Variables
In Railway dashboard, add to Backend service:

```
DATABASE_URL=${{Postgres.DATABASE_URL}}
CORS_ORIGIN=https://your-project.vercel.app
DEBUG=false
PYTHONUNBUFFERED=1
```

### 6. Deploy
- Click "Deploy"
- Wait for deployment to complete

✅ **Backend is now live at:** `https://your-backend-url.railway.app`

---

## 🔗 Step 4: Connect Frontend to Backend

### Update Environment Variables

**In Vercel Dashboard:**
1. Go to Settings → Environment Variables
2. Add/Update:
   ```
   VITE_API_URL=https://your-railway-backend.railway.app/api/v1
   ```
3. Trigger redeploy

---

## ✅ Step 5: Verify Deployment

### Test Frontend
```bash
# Visit your Vercel URL
https://your-project.vercel.app

# Should load without errors
# Check browser console for API errors
```

### Test Backend API
```bash
# Test endpoint
curl https://your-backend-url.railway.app/api/v1/reserve/balance

# Should return JSON with balance data
```

### Test Full Integration
1. Open frontend URL
2. Should load dashboard
3. Click "Refresh Analytics"
4. Should fetch data from backend
5. Dashboard should populate with data

---

## 🚨 Troubleshooting

### **Frontend shows "Cannot reach backend"**
- Check `VITE_API_URL` environment variable
- Verify backend is running on Railway
- Check browser console for CORS errors
- Ensure CORS_ORIGIN matches your Vercel URL

### **CORS Error in Console**
Update `phase4/backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-vercel-app.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **Database Connection Failed**
- Check `DATABASE_URL` is set correctly
- Railway Postgres should auto-configure it
- Verify database is running in Railway dashboard

### **Backend won't start**
- Check logs in Railway dashboard
- Verify Dockerfile is correct
- Check Python dependencies in `requirements.txt`
- Run locally: `uvicorn app.main:app --reload`

### **Out of Memory or Timeout**
- Railway free tier has resource limits
- Upgrade to paid plan or optimize code
- Check for infinite loops or memory leaks

---

## 📝 Monitoring & Logs

### Vercel Logs
```bash
vercel logs
```

### Railway Logs
1. Go to Railway Dashboard
2. Click your Backend service
3. Click "Logs" tab
4. View real-time logs

---

## 🔄 Future Deployments

After initial setup, deployments are automatic:

1. **Frontend:** Push to GitHub → Vercel auto-deploys
2. **Backend:** Push to GitHub → Railway auto-deploys

Or manually trigger:
```bash
# Frontend
vercel deploy --prod

# Backend: Push changes to GitHub, Railway auto-deploys
```

---

## 💾 Backup & Database Management

### Backup PostgreSQL Data
```bash
# From Railway CLI
railway shell
pg_dump > backup.sql
```

### Restore Database
```bash
psql -U postgres < backup.sql
```

---

## 🛡️ Security Checklist

- [ ] Environment variables are secrets (not in code)
- [ ] CORS configured for your domain only
- [ ] Database backups enabled
- [ ] SSL/HTTPS enabled (automatic on both platforms)
- [ ] Rate limiting configured
- [ ] Input validation on backend
- [ ] No API keys in frontend code

---

## 💰 Cost Estimation

- **Vercel Frontend:** Free tier (up to 100GB bandwidth/month)
- **Railway Backend:** Free tier ($5/month credit after trial)
- **PostgreSQL:** Included in Railway project

**Total Cost:** ~$0 (free tier) or ~$7-10/month (paid tier)

---

## 📞 Support Resources

- [Vercel Docs](https://vercel.com/docs)
- [Railway Docs](https://docs.railway.app/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React/Vite Docs](https://vitejs.dev/)

---

## ✨ Next Steps

1. ✅ Deploy frontend to Vercel
2. ✅ Deploy backend to Railway
3. ✅ Connect and test
4. ✅ Monitor logs and errors
5. ✅ Make improvements and redeploy
6. ✅ Share your app with the world!

🎉 **You're all set! Your Smart Reserve AI app is now live!**

---

For questions or issues, check the logs on Vercel and Railway dashboards!
