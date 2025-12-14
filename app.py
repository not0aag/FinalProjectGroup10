"""
Flask CI/CD Project Application
A simple Flask API demonstrating CI/CD pipeline practices
"""

from flask import Flask, jsonify
import os

# Create Flask application instance
app = Flask(__name__)


@app.route('/')
def home():
    """
    Home endpoint
    Returns a simple welcome message
    """
    return "Hello from CI/CD Project"


@app.route('/health')
def health():
    """
    Health check endpoint
    Returns JSON with status and environment information
    Used by Docker healthcheck and monitoring tools
    """
    # Get environment from APP_ENV variable, default to 'development'
    environment = os.environ.get('APP_ENV', 'development')
    
    return jsonify({
        'status': 'healthy',
        'env': environment
    })


if __name__ == '__main__':
    # Run the Flask application
    # host='0.0.0.0' allows external connections (required for Docker)
    # port=5000 is the default Flask port
    # debug=False for production safety
    app.run(host='0.0.0.0', port=5000, debug=False)
