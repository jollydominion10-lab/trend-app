import random
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enables frontend dashboard requests

# Mock database of social mentions and sentiment scores
mentions_db = [
    {
        "id": 1,
        "source": "Twitter / X",
        "text": "TrendApp user interface is extremely clean and fast!",
        "sentiment": "positive",
        "score": 0.92,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": 2,
        "source": "Reddit r/webdev",
        "text": "Comparing chart libraries for real-time analytics dashboards.",
        "sentiment": "neutral",
        "score": 0.10,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": 3,
        "source": "News Feed",
        "text": "Cloud infrastructure providers report minor API latency in East region.",
        "sentiment": "negative",
        "score": -0.75,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
]

def analyze_sentiment(text):
    """
    Simulates a natural language processing (NLP) sentiment analyzer.
    Returns polarity tag and confidence score.
    """
    text_lower = text.lower()
    positive_words = ["great", "fast", "love", "awesome", "good", "reliable", "excellent"]
    negative_words = ["slow", "error", "bad", "latency", "bug", "issue", "failed"]

    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)

    if pos_count > neg_count:
        return "positive", 0.85
    elif neg_count > pos_count:
        return "negative", -0.80
    else:
        return "neutral", 0.05

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "service": "TrendApp Analytics Engine",
        "status": "online",
        "version": "1.0.0"
    })

@app.route("/api/mentions", methods=["GET"])
def get_mentions():
    """Endpoint returning all analyzed mentions and aggregate metrics."""
    total = len(mentions_db)
    positive = sum(1 for m in mentions_db if m["sentiment"] == "positive")
    neutral = sum(1 for m in mentions_db if m["sentiment"] == "neutral")
    negative = sum(1 for m in mentions_db if m["sentiment"] == "negative")

    sentiment_index = round((positive / total) * 100) if total > 0 else 0

    return jsonify({
        "metrics": {
            "total_mentions": total,
            "sentiment_index_pct": sentiment_index,
            "breakdown": {
                "positive": positive,
                "neutral": neutral,
                "negative": negative
            }
        },
        "mentions": mentions_db
    })

@app.route("/api/mentions", methods=["POST"])
def add_mention():
    """Endpoint to submit a new social mention for sentiment processing."""
    data = request.get_json() or {}
    text = data.get("text", "")
    source = data.get("source", "API Webhook")

    if not text:
        return jsonify({"error": "Text content is required"}), 400

    sentiment, score = analyze_sentiment(text)

    new_entry = {
        "id": len(mentions_db) + 1,
        "source": source,
        "text": text,
        "sentiment": sentiment,
        "score": score,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    mentions_db.insert(0, new_entry)
    return jsonify({"success": True, "data": new_entry}), 201

if __name__ == "__main__":
    print("⚡ TrendApp Analytics Backend running on http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)