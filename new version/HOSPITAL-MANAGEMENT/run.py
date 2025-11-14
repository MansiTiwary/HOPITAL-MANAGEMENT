#!/usr/bin/env python
"""
Entry point to run HealthFusion app from repo root.
Usage: python run.py
"""
import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import and run the app
from app import app

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
