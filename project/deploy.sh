#!/bin/bash

# Deployment script for Citizen AI

echo "🚀 Starting Citizen AI deployment..."

# Build frontend
echo "📦 Building frontend..."
npm install
npm run build

# Choose deployment method
echo "Choose deployment method:"
echo "1. Flask (app.py)"
echo "2. FastAPI (fastapi_app.py)"
echo "3. Docker Compose"
echo "4. Heroku"
echo "5. Vercel"

read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo "🐍 Starting Flask deployment..."
        pip install -r requirements.txt
        python app.py
        ;;
    2)
        echo "⚡ Starting FastAPI deployment..."
        pip install -r requirements.txt
        uvicorn fastapi_app:app --host 0.0.0.0 --port 8000 --reload
        ;;
    3)
        echo "🐳 Starting Docker deployment..."
        docker-compose up --build
        ;;
    4)
        echo "☁️ Deploying to Heroku..."
        git add .
        git commit -m "Deploy to Heroku"
        heroku create citizen-ai-app
        git push heroku main
        ;;
    5)
        echo "▲ Deploying to Vercel..."
        npm install -g vercel
        vercel --prod
        ;;
    *)
        echo "Invalid choice. Exiting..."
        exit 1
        ;;
esac

echo "✅ Deployment complete!"