#!/usr/bin/env bash
# Install dependencies for frontend
cd phase4/frontend
npm install

# Build the frontend
npm run build

echo "✅ Build complete! Frontend is ready for Vercel deployment."
echo ""
echo "📋 Next steps:"
echo "1. Install Vercel CLI: npm i -g vercel"
echo "2. Run: vercel deploy"
echo "3. Configure environment variables in Vercel dashboard"
echo "4. For backend: Deploy to Vercel Functions or Railway/Render"
