import requests
import feedparser
import os
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
RSS_FEED_URL = "https://www.jagran.com/rss/news/national.xml"

STATE_FILE = "last_sent.json"

def load_last_sent():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"last_links": []}

def save_last_sent(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f)

def get_latest_news():
    feed = feedparser.parse(RSS_FEED_URL)
    return [(entry.title, entry.link) for entry in feed.entries]

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHANNEL_ID, "text": message}
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print("Error:", response.text)

if __name__ == "__main__":
    state = load_last_sent()
    already_sent = set(state["last_links"])

    news_items = get_latest_news()
    new_items = [(title, link) for title, link in news_items if link not in already_sent]

    if new_items:
        for title, link in new_items:
            send_to_telegram(f"📰 {title}\n{link}")
            already_sent.add(link)

        state["last_links"] = list(already_sent)[-50:]  # सिर्फ़ recent 50 link याद रखेगा
        save_last_sent(state)
    else:
        print("कोई नई खबर नहीं मिली।")
        
