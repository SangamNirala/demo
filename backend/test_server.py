"""
Minimal Test Server - For Debugging
"""

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'Test server working'}), 200

if __name__ == '__main__':
    print("Test server starting on http://localhost:8000")
    app.run(host='0.0.0.0', port=8000, debug=True)
