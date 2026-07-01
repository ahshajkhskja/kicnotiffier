import requests
import time
import os
from datetime import datetime

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def send_discord_notification(channel, title, viewers, category):
    if not DISCORD_WEBHOOK:
        return
    embed = {
        "title": f"🔴 {channel} is LIVE!",
        "description": title,
        "color": 0x00ff00,
        "fields": [
            {"name": "Viewers", "value": str(viewers), "inline": True},
            {"name": "Category", "value": category, "inline": True}
        ],
        "timestamp": datetime.utcnow().isoformat()
    }
    requests.post(DISCORD_WEBHOOK, json={"embeds": [embed]})

def is_live(channel_slug):
    url = f"https://kick.com/api/v2/channels/{channel_slug}/livestream"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return None
        data = r.json().get('data')
        if data:
            return {
                "title": data.get("session_title", "No title"),
                "viewers": data.get("viewer_count", 0),
                "category": data.get("categories", [{}])[0].get("name", "Unknown")
            }
        return None
    except:
        return None

def main():
    channels = ["maplesyrupy"]
    
    print(f"Kick Notifier running! Monitoring {len(channels)} channels.")
    notified = set()

    # Immediate check
    print("Checking MapleSyrupy right now...")
    status = is_live("maplesyrupy")
    if status:
        print("LIVE detected!")
        send_discord_notification("maplesyrupy", status["title"], status["viewers"], status["category"])
    else:
        print("Not detected as live.")

    print("Done.")

if __name__ == "__main__":
    main()
