from flask import Flask, jsonify
from haiku_scrape import YoutubeScrape


app = Flask(__name__)
url = "https://old.reddit.com/r/youtubehaiku/top/?sort=top"


@app.route("/top/<time_range>/<int:amount>")
def get_top_by_range(time_range, amount):
    if amount < 25:
        amount = 25
    if amount > 500:
        amount = 500
    result = YoutubeScrape(url, time_range, amount).get_links_for_period()
    return jsonify(list(result))
