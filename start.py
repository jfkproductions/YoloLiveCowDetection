from app import app  # Assuming your Flask app is in app.py
import sys
import os
import logging

sys.stdout = open('stdout.log', 'w')
sys.stderr = open('stderr.log', 'w')

logging.basicConfig(filename="app.log", level=logging.DEBUG)

from app import app

if __name__ == "__main__":
    logging.debug("Starting Flask application...")
    app.run(host="0.0.0.0", port=5000)
    logging.debug("Flask application has started.")
