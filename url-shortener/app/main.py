from flask import Flask, jsonify, request, redirect
from app.models import url_store
from app.utils import generate_short_code, is_valid_url
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')

    if not original_url or not is_valid_url(original_url):
        return jsonify({'error': 'Invalid URL'}), 400

    short_code = generate_short_code()
    while short_code in url_store:
        short_code = generate_short_code()

    url_store[short_code] = {
        'url': original_url,
        'created_at': datetime.utcnow().isoformat(),
        'clicks': 0
    }

    short_url = f"http://localhost:5000/{short_code}"
    return jsonify({'short_code': short_code, 'short_url': short_url}), 201

@app.route('/<short_code>', methods=['GET'])
def redirect_url(short_code):
    if short_code not in url_store:
        return jsonify({'error': 'Short URL not found'}), 404

    url_store[short_code]['clicks'] += 1
    return redirect(url_store[short_code]['url'])

@app.route('/api/stats/<short_code>', methods=['GET'])
def get_stats(short_code):
    if short_code not in url_store:
        return jsonify({'error': 'Short URL not found'}), 404

    data = url_store[short_code]
    return jsonify({
        'url': data['url'],
        'clicks': data['clicks'],
        'created_at': data['created_at']
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
