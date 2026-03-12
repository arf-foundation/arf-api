#!/bin/bash

# Set paths
BACKEND_DIR="/workspaces/arf-api"
FRONTEND_DIR="/workspaces/arf-frontend"
VENV_ACTIVATE="$BACKEND_DIR/venv/bin/activate"
CLOUDFLARED=$(which cloudflared 2>/dev/null || echo "/usr/local/bin/cloudflared")

# Kill any existing processes
echo "🛑 Stopping existing uvicorn and cloudflared..."
pkill -f uvicorn
pkill -f cloudflared
sleep 2

# Start uvicorn
echo "🚀 Starting uvicorn..."
cd "$BACKEND_DIR"
source "$VENV_ACTIVATE"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
sleep 3

# Verify uvicorn is running
if ! curl -s http://localhost:8000/health >/dev/null; then
    echo "❌ uvicorn failed to start. Exiting."
    exit 1
fi
echo "✅ uvicorn is running."

# Start cloudflared and capture URL
echo "🌐 Starting cloudflared tunnel..."
TEMP_FILE=$(mktemp)
$CLOUDFLARED tunnel --url http://localhost:8000 2>&1 | tee "$TEMP_FILE" &

# Wait for URL to appear
echo "⏳ Waiting for tunnel URL..."
URL=""
for i in {1..30}; do
    URL=$(grep -oP 'https://[a-z0-9-]+\.trycloudflare\.com' "$TEMP_FILE" | head -1)
    if [ -n "$URL" ]; then
        break
    fi
    sleep 1
done

if [ -z "$URL" ]; then
    echo "❌ Failed to get tunnel URL."
    exit 1
fi
echo "✅ Tunnel URL: $URL"

# Save URL for monitoring (used by monitor.sh)
echo "$URL" > /workspaces/arf-api/current_url.txt

# Update Vercel environment variable
echo "🔧 Updating Vercel environment variable..."
cd "$FRONTEND_DIR"
if command -v vercel &>/dev/null; then
    vercel env rm NEXT_PUBLIC_API_URL production -y
    echo "$URL" | vercel env add NEXT_PUBLIC_API_URL production
    echo "🔄 Redeploying frontend..."
    vercel --prod
else
    echo "⚠️  Vercel CLI not installed. Please install it with: npm i -g vercel"
    echo "Then manually update the env var to: $URL"
fi

echo "🎉 All done! Your new URL is: $URL"
echo "Frontend will be updated shortly. Check https://arf-frontend-sandy.vercel.app"