from discord_webhook import DiscordWebhook
import os

alert_channel_url = "https://discord.com/api/webhooks/968249751403384843/0Fqt4BUGtGBdAqgnCHD5RmVQzrXyV-fGy-6N3gdHUyS-kptuikFzGqDVDm63508D1Ng8"

def send_alert(message):
    webhook = DiscordWebhook(url=alert_channel_url, content=message + f" PID=[ {os.getpid()} ]")
    return webhook.execute()