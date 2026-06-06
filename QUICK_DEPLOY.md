# 🚀 Quick Start - Deploy to Vercel in 5 Minutes

## Prerequisites Checklist
- [ ] Code pushed to GitHub
- [ ] Vercel account created (vercel.com)
- [ ] Railway account created (railway.app)
- [ ] Node.js installed
- [ ] npm installed

---

## ⚡ Quick Deploy (5 min)

### 1. Deploy Frontend (2 min)
```powershell
cd phase4\frontend
npm install
npm run build
vercel deploy --prod
```
✅ Note your Vercel URL: `https://your-project.vercel.app`

### 2. Deploy Backend (2 min)
1. Go to railway.app
2. "New Project" → Select GitHub → Choose your repo
3. Railway will auto-detect and build
4. Add PostgreSQL service
5. ✅ Note your Railway URL: `https://your-api.railway.app`

### 3. Connect (1 min)
1. Go to Vercel Dashboard → Project Settings
2. Add Environment Variable:
   ```
   VITE_API_URL = https://your-api.railway.app/api/v1
   ```
3. Redeploy: `vercel deploy --prod`

---

## ✅ Verify It Works

1. Visit: https://your-project.vercel.app
2. Click "Refresh Analytics"
3. Data should load from backend ✨

---

## 📊 Files Created for Deployment

| File | Purpose |
|------|---------|
| `vercel.json` | Vercel configuration |
| `.env.example` | Environment variables template |
| `VERCEL_DEPLOYMENT.md` | Detailed deployment guide |
| `DEPLOYMENT_GUIDE.md` | Alternative guide |
| `deploy.ps1` | PowerShell deployment script |

---

## 🐛 If Something Breaks

**Frontend not loading?**
- Check Vercel logs: `vercel logs`
- Verify VITE_API_URL is correct

**Backend not responding?**
- Check Railway logs in dashboard
- Verify DATABASE_URL is set
- Check CORS_ORIGIN matches frontend URL

**CORS Error?**
- Backend needs frontend origin added
- Update phase4/backend/app/main.py CORS settings
- Redeploy backend

---

## 🔄 After First Deploy

**Next time you want to deploy:**

```bash
# Frontend
git push  # Vercel auto-deploys
# OR manual: vercel deploy --prod

# Backend
git push  # Railway auto-deploys
```

---

**That's it! Your app is live! 🎉**

Need help? Check VERCEL_DEPLOYMENT.md for full details.
