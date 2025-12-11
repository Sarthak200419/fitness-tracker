"""Main application entry point."""
import os
from backend.app import create_app

app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    # Run with generated SSL certs to enable HTTPS (required for Web Bluetooth)
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
