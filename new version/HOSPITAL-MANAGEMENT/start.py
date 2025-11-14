#!/usr/bin/env python
"""
Simple launcher script - run this from repo root.
Runs app.py directly from current directory
"""
import subprocess
import os
import sys

# Run app.py from current directory
result = subprocess.run([sys.executable, 'app.py'])
sys.exit(result.returncode)
