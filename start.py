#!/usr/bin/env python
"""
Simple launcher script - run this from repo root.
cd into HealthFusion-_24X7 and run app.py
"""
import subprocess
import os
import sys

project_dir = os.path.join(os.path.dirname(__file__), 'HealthFusion-_24X7')
os.chdir(project_dir)
result = subprocess.run([sys.executable, 'app.py'])
sys.exit(result.returncode)
