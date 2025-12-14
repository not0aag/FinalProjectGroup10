from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from CI/CD Project"

@app.route('/health')
def health():
    env = os.environ.get('APP_ENV', 'development')
    return jsonify({'status': 'healthy', 'env': env})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
