import requests
import feedparser
import os
import time

# Telegram bot token और channel id (Secrets में store करना बेहतर है)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Dainik Jagran की RSS categories
RSS_FEEDS = {
    "राष्ट्रीय": "https://www.jagran.com/rss/news/national.xml",
    "खेल": "https://www.jagran.com/rss/sports.xml",
    "व्यापार": "https://www.jagran.com/rss/business.xml",
    "अंतरराष्ट्रीय": "https://www.jagran.com/rss/international.xml",
    "राज्य": "https://www.jagran.com/rss/state.xml"
}

# पहले भेजी हुई news track करने के लिए
sent_news = set()

def get_latest_news():
    new_items = []
    for category, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            if entry.link not in sent_news:
                sent_news.add(entry.link)
                new_items.append(f"🔹 *{category}*\n{entry.title}\n{entry.link}")
    return new_items

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print("Error:", response.text)

if __name__ == "__main__":
    news_items = get_latest_news()
    if news_items:
        for item in news_items:
            send_to_telegram(item)
          
