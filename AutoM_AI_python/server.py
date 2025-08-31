# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 12:44:08 2025

@author: elmou
"""

# server.py
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        result = subprocess.run(
            ["python", "main.py"],  # ou ["python3", "main.py"] selon ton système
            capture_output=True,
            text=True,
            check=True
        )
        return jsonify({"output": result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.stderr}), 500

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
