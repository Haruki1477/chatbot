from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta

app = Flask(__name__)
API_KEY = "5d4a878b3185a1bc054f25c36a7cdd49"  # GNews APIキー

# ニュース取得関数
def get_news(query="", page=1, page_size=5):
    now = datetime.utcnow()
    from_date = (now - timedelta(days=7)).strftime("%Y-%m-%d")

    keyword_query = "ニュース" if not query.strip() else " OR ".join([q.strip() for q in query.split(",")])

    url = (
        f"https://gnews.io/api/v4/search?q={keyword_query}"
        f"&lang=ja&from={from_date}&sortby=publishedAt"
        f"&apikey={API_KEY}&max={page_size}&page={page}"
    )

    response = requests.get(url)
    data = response.json()
    
    if "errors" in data:
        return []

    return data.get("articles", [])

# Flaskルート
@app.route("/")
def index():
    query = request.args.get("q", "")
    category = request.args.get("category", "")
    page = int(request.args.get("page", 1))

    # カテゴリが指定されていればクエリに追加
    if category:
        query = category if not query else f"{query}, {category}"

    articles = get_news(query=query, page=page)
    return render_template("index.html", articles=articles, query=query, category=category, page=page)

if __name__ == "__main__":
    app.run(debug=True)
