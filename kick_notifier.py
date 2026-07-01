import requests
import time
import os
from datetime import datetime

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def send_discord_notification(channel, title, viewers):
    if not DISCORD_WEBHOOK:
        return
    embed = {
        "title": f"🔴 {channel} is LIVE on Kick!",
        "description": title,
        "color": 0x00ff00,
        "fields": [
            {"name": "Viewers", "value": str(viewers), "inline": True}
        ],
        "timestamp": datetime.utcnow().isoformat()
    }
    requests.post(DISCORD_WEBHOOK, json={"embeds": [embed]})

def is_live(channel_slug):
    # Alternative endpoint
    urls = [
        f"https://kick.com/api/v2/channels/{channel_slug}/livestream",
        f"https://kick.com/api/v1/channels/{channel_slug}"
    ]
    for url in urls:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, dict):
                    if data.get('data') or data.get('is_live'):
                        title = data.get('data', data).get('session_title', 'Live Stream')
                        viewers = data.get('data', data).get('viewer_count', 0)
                        return {"title": title, "viewers": viewers}
        except:
            continue
    return None

def main():
    channels = ["maplesyrupy"]
    print("Kick Notifier started - Monitoring MapleSyrupy")
    notified = False

    while True:
        status = is_live("maplesyrupy")
        if status and not notified:
            print("LIVE detected! Sending notification...")
            send_discord_notification("maplesyrupy", status["title"], status["viewers"])
            notified = True
        elif not status and notified:
            print("MapleSyrupy went offline.")
            notified = False
        
        time.sleep(30)

if __name__ == "__main__":
    main()
