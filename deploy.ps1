#!/usr/bin/env powershell
# Deployment Setup Script for Vercel

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Smart Reserve AI - Vercel Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Vercel CLI is installed
Write-Host "Checking Vercel CLI installation..." -ForegroundColor Yellow
$vercelInstalled = npm list -g vercel 2>$null
if (!$vercelInstalled) {
    Write-Host "Installing Vercel CLI..." -ForegroundColor Yellow
    npm install -g vercel
}

Write-Host "✅ Vercel CLI is ready" -ForegroundColor Green
Write-Host ""

# Build frontend
Write-Host "Building frontend application..." -ForegroundColor Yellow
Set-Location "F:\Paytm\phase4\frontend"
npm run build

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Frontend built successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Frontend build failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deployment Instructions:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1️⃣  Frontend Deployment (Vercel)" -ForegroundColor Cyan
Write-Host "   cd phase4/frontend" -ForegroundColor White
Write-Host "   vercel deploy --prod" -ForegroundColor White
Write-Host ""
Write-Host "2️⃣  Backend Deployment (Railway)" -ForegroundColor Cyan
Write-Host "   - Go to https://railway.app/" -ForegroundColor White
Write-Host "   - Create new project" -ForegroundColor White
Write-Host "   - Connect GitHub repo" -ForegroundColor White
Write-Host "   - Add PostgreSQL database" -ForegroundColor White
Write-Host "   - Deploy" -ForegroundColor White
Write-Host ""
Write-Host "3️⃣  Configure Environment Variables" -ForegroundColor Cyan
Write-Host "   Frontend (Vercel):" -ForegroundColor White
Write-Host "   VITE_API_URL=https://your-backend-url/api/v1" -ForegroundColor White
Write-Host ""
Write-Host "   Backend (Railway):" -ForegroundColor White
Write-Host "   DATABASE_URL=postgresql://..." -ForegroundColor White
Write-Host "   CORS_ORIGIN=https://your-vercel-app.vercel.app" -ForegroundColor White
Write-Host ""
Write-Host "4️⃣  Test Your Deployment" -ForegroundColor Cyan
Write-Host "   Frontend: https://your-domain.vercel.app" -ForegroundColor White
Write-Host "   Backend: https://your-api.railway.app/api/v1" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Ready to deploy! 🚀" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
