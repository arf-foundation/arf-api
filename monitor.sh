#!/bin/bash

URL_FILE="/workspaces/arf-api/current_url.txt"
LOG_FILE="/workspaces/arf-api/monitor.log"

if [ ! -f "$URL_FILE" ]; then
    echo "$(date): No URL file found. Exiting." >> "$LOG_FILE"
    exit 1
fi

CURRENT_URL=$(cat "$URL_FILE")

if ! curl -s -f "$CURRENT_URL/health" > /dev/null; then
    echo "$(date): Tunnel down. Restarting..." >> "$LOG_FILE"
    /workspaces/arf-api/start.sh
else
    echo "$(date): Tunnel OK." >> "$LOG_FILE"
fi
