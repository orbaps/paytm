# Vercel Deployment Guide - Smart Reserve AI

## 🚀 Quick Deployment Steps

### **Option 1: Frontend Only on Vercel (Recommended)**

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Navigate to frontend directory**
   ```bash
   cd phase4/frontend
   ```

3. **Deploy to Vercel**
   ```bash
   vercel deploy --prod
   ```

4. **Configure environment variables in Vercel Dashboard:**
   - Go to Project Settings → Environment Variables
   - Add: `VITE_API_URL` = `https://your-backend-url.com/api/v1`

---

### **Option 2: Full Stack Deployment**

#### **A. Deploy Frontend to Vercel**
```bash
cd phase4/frontend
vercel deploy --prod
```

#### **B. Deploy Backend to Railway/Render (Free Alternatives)**

**Using Railway.app:**
1. Go to https://railway.app/
2. Click "New Project" → Select "Deploy from GitHub"
3. Connect your GitHub repo with Paytm project
4. Add PostgreSQL database
5. Configure environment: `DATABASE_URL` (auto-configured)
6. Deploy backend from `phase4/backend`

**Using Render.com:**
1. Go to https://render.com/
2. Create new "Web Service"
3. Connect GitHub repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
6. Add PostgreSQL database
7. Configure PORT environment variable

---

### **Environment Variables Setup**

**In Vercel Dashboard (Frontend):**
```
VITE_API_URL=https://your-backend-api.railway.app/api/v1
```

**In Railway/Render Dashboard (Backend):**
```
DATABASE_URL=postgresql://user:password@host:port/dbname
CORS_ORIGIN=https://your-vercel-frontend.vercel.app
```

---

### **Database Setup**

**Option 1: Railway Postgres** (Easiest)
- Automatically provided when you add PostgreSQL service
- Connection string auto-configured

**Option 2: External PostgreSQL** (Supabase)
1. Create account at https://supabase.com/
2. Create new project
3. Copy connection string to `DATABASE_URL`
4. Run database schema:
   ```bash
   python phase4/backend/app/db/init_db.py
   ```

---

### **Verify Deployment**

1. **Frontend**: Visit your Vercel URL (e.g., https://smart-reserve.vercel.app)
2. **Backend API**: Visit https://your-backend-api.railway.app/api/v1/reserve/balance
3. **Health Check**: Should return JSON response with balance data

---

### **Troubleshooting**

**CORS Errors:**
- Update `app/main.py` CORS settings:
  ```python
  app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-vercel-domain.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )
  ```

**Database Connection Fails:**
- Verify `DATABASE_URL` environment variable is set
- Check database credentials
- Ensure database is running and accessible

**Frontend Blank Page:**
- Check browser console for errors
- Verify `VITE_API_URL` is correct
- Run build locally: `npm run build`

---

### **Deployment Checklist**

- [ ] Frontend builds successfully: `npm run build`
- [ ] Backend starts locally: `uvicorn app.main:app`
- [ ] Database connection works
- [ ] Environment variables configured
- [ ] CORS enabled for frontend origin
- [ ] API endpoints tested
- [ ] Git repository created and pushed
- [ ] Vercel project linked to repository
- [ ] Environment variables added to Vercel
- [ ] Backend deployed to Railway/Render
- [ ] Frontend deployed to Vercel
- [ ] All services connected and working

---

### **Quick Links**

- [Vercel](https://vercel.com/)
- [Railway](https://railway.app/)
- [Render](https://render.com/)
- [Supabase](https://supabase.com/)

---

### **Commands Reference**

```bash
# Build frontend
cd phase4/frontend && npm run build

# Deploy to Vercel
vercel deploy --prod

# Test backend locally
cd phase4/backend
python -m uvicorn app.main:app --reload

# Check deployment status
vercel status

# View deployment logs
vercel logs
```

---

**Need Help?** Check the logs in your deployment platform's dashboard!
