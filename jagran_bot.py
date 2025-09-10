import os
import json
import feedparser
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]

RSS_FEEDS = {
    "राष्ट्रीय": "https://www.jagran.com/rss/hindi-news/national-news.xml",
    "अंतर्राष्ट्रीय": "https://www.jagran.com/rss/hindi-news/international-news.xml",
    "राजनीति": "https://www.jagran.com/rss/hindi-news/politics-news.xml",
    "व्यापार": "https://www.jagran.com/rss/hindi-news/business-news.xml",
    "मनोरंजन": "https://www.jagran.com/rss/hindi-news/entertainment-news.xml",
    "खेल": "https://www.jagran.com/rss/hindi-news/sports-news.xml",
    "शिक्षा": "https://www.jagran.com/rss/hindi-news/education-news.xml",
    "टेक्नोलॉजी": "https://www.jagran.com/rss/hindi-news/technology-news.xml",
    "लाइफ़स्टाइल": "https://www.jagran.com/rss/hindi-news/lifestyle-news.xml",
    "धर्म": "https://www.jagran.com/rss/hindi-news/religion-news.xml"
}

CATEGORY_LOGOS = {
    "राष्ट्रीय": "logos/national.png",
    "अंतर्राष्ट्रीय": "logos/international.png",
    "राजनीति": "logos/politics.png",
    "व्यापार": "logos/business.png",
    "मनोरंजन": "logos/entertainment.png",
    "खेल": "logos/sports.png",
    "शिक्षा": "logos/education.png",
    "टेक्नोलॉजी": "logos/technology.png",
    "लाइफ़स्टाइल": "logos/lifestyle.png",
    "धर्म": "logos/religion.png"
}

SENT_FILE = "sent.json"

def load_sent():
    if os.path.exists(SENT_FILE):
        with open(SENT_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_sent(sent_ids):
    with open(SENT_FILE, "w", encoding="utf-8") as f:
        json.dump(list(sent_ids), f, ensure_ascii=False, indent=2)

def send_to_telegram(category, title, link):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    caption = f"📰 <b>{category}</b>\n\n{title}\n\n🔗 {link}"

    logo_path = CATEGORY_LOGOS.get(category)
    if logo_path and os.path.exists(logo_path):
        with open(logo_path, "rb") as photo:
            files = {"photo": photo}
            data = {"chat_id": CHANNEL_ID, "caption": caption, "parse_mode": "HTML"}
            requests.post(url, data=data, files=files)
    else:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHANNEL_ID, "text": caption, "parse_mode": "HTML"}
        requests.post(url, data=data)

def check_news():
    sent_ids = load_sent()
    new_sent = set(sent_ids)

    for category, feed_url in RSS_FEEDS.items():
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:5]:  # latest 5 check करें
            news_id = entry.id if "id" in entry else entry.link
            if news_id not in sent_ids:   # केवल नई news भेजें
                send_to_telegram(category, entry.title, entry.link)
                new_sent.add(news_id)

    save_sent(new_sent)

if __name__ == "__main__":
    check_news()
    
