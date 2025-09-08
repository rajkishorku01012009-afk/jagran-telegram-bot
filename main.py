import requests
import feedparser
import os
import json

# Telegram bot token और channel id (Secrets में store करें)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Dainik Jagran के RSS categories
RSS_FEEDS = {
    "राष्ट्रीय": "https://www.jagran.com/rss/news/national.xml",
    "खेल": "https://www.jagran.com/rss/sports.xml",
    "व्यापार": "https://www.jagran.com/rss/business.xml",
    "अंतर्राष्ट्रीय": "https://www.jagran.com/rss/international.xml",
    "राज्य": "https://www.jagran.com/rss/state.xml"
}

STATE_FILE = "state.json"

# पहले से भेजी गई news load करें
def load_sent_news():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

# नई भेजी गई news save करें
def save_sent_news(sent_news):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(list(sent_news), f, ensure_ascii=False, indent=2)

# Latest news निकालें
def get_latest_news(sent_news, limit=5):
    new_items = []
    for category, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:limit]:  # हर category से 5 news
            if entry.link not in sent_news:
                sent_news.add(entry.link)
                new_items.append(f"📰 *{category}*\n{entry.title}\n{entry.link}")
    return new_items, sent_news

# Telegram पर भेजें
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
    sent_news = load_sent_news()
    news_items, sent_news = get_latest_news(sent_news, limit=5)

    if news_items:
        for item in news_items:
            send_to_telegram(item)
        save_sent_news(sent_news)
    else:
        print("No new news.")
        
