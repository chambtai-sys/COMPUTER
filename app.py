from flask import Flask, render_template, jsonify
from computer_engine import ComputerEngine
import os

app = Flask(__name__)
# Initialize engine on the parent directory to see the whole workspace
engine = ComputerEngine(root_dir="/root/workspace")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def stats():
    return jsonify({
        "ops": engine.get_operations(),
        "progress": engine.get_progress(),
        "tech": engine.get_tech_endeavors()
    })

@app.route('/api/report')
def report():
    return jsonify({"markdown": engine.generate_report()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
