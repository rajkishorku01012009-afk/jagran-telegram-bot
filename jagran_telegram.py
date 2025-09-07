import requests
import feedparser
import os

# Telegram bot token और channel id secrets से लेंगे
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Dainik Jagran का RSS Feed URL
RSS_FEED_URL = "https://www.jagran.com/rss/news/national.xml"

def get_latest_news():
    feed = feedparser.parse(RSS_FEED_URL)
    news_items = []
    for entry in feed.entries[:5]:  # सिर्फ 5 news भेजेंगे
        title = entry.title
        link = entry.link
        news_items.append(f"{title}\n{link}")
    return "\n\n".join(news_items)

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print("Error:", response.text)

if __name__ == "__main__":
    news = get_latest_news()
    if news:
        send_to_telegram("📰 आज की मुख्य खबरें:\n\n" + news)
      
