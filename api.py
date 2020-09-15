import flask
from flask import request, jsonify
import amazonscraper

app = flask.Flask(__name__)
app.config["DEBUG"] = False


@app.route('/', methods=['GET'])
def home():
    s = request.args.get('s')
    amazon_data = amazonscraper.scraper(s)
    return jsonify(amazon_data)
