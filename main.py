import feedparser
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

RSS_FEED = "https://www.jagran.com/rss/news/national.xml"

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    print("Telegram Response:", response.text)

def fetch_and_send_news():
    feed = feedparser.parse(RSS_FEED)
    if not feed.entries:
        print("No news found in RSS feed.")
        return

    for entry in feed.entries[:5]:  # सिर्फ़ पहली 5 news भेजेंगे
        title = entry.title
        link = entry.link
        message = f"<b>{title}</b>\n{link}"
        send_to_telegram(message)

if __name__ == "__main__":
    fetch_and_send_news()
    
