"""Main application entry point."""
import os
from backend.app import create_app

app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    # Run in HTTP mode (reverted from HTTPS)
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)



"""
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Mac/Linux

Install dependencies
pip install -r requirements.txt

Then Run
python run.py
"""