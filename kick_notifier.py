import requests
import os

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

print("Webhook URL length:", len(DISCORD_WEBHOOK) if DISCORD_WEBHOOK else 0)

if not DISCORD_WEBHOOK:
    print("ERROR: Webhook not found!")
else:
    data = {
        "content": "🧪 Test message from Kick Notifier - If you see this, webhook is working!"
    }
    response = requests.post(DISCORD_WEBHOOK, json=data)
    print("Status Code:", response.status_code)
    if response.status_code != 204:
        print("Response:", response.text)
    else:
        print("✅ Message sent successfully!")
