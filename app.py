from flask import Flask, render_template, request, jsonify
import subprocess
import sys
import os
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-detection')
def run_detection():
    try:
        script_path = os.path.join(os.getcwd(), 'eye_blink_detector.py')
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            return jsonify({'output': [f"❌ Script error {result.returncode}:"] + result.stderr.split('\n')})

        output_lines = result.stdout.strip().split('\n')
        summary = output_lines[-6:] if len(output_lines) >= 6 else output_lines
        return jsonify({'output': summary})
    except subprocess.TimeoutExpired:
        return jsonify({'output': ['❌ Detection timed out.']})
    except Exception as e:
        return jsonify({'output': [f'❌ Error occurred: {str(e)}']})

# 🧠 Add this endpoint for logging keyboard data
@app.route('/log-keystrokes', methods=['POST'])
def log_keystrokes():
    try:
        data = request.json.get('log', [])
        if not data:
            return jsonify({'status': '❌ No keystroke data received'}), 400

        log_file = os.path.join(os.getcwd(), 'keyboard_logs.json')
        with open(log_file, 'a') as f:
            f.write(json.dumps(data) + '\n')

        print("✅ Keystroke log received:", data[-1])  # Print last entry
        return jsonify({'status': '✅ Keystrokes logged'})
    except Exception as e:
        print("❌ Failed to log keystrokes:", str(e))
        return jsonify({'status': '❌ Server error'}), 500

@app.route('/submit-form', methods=['POST'])
def submit_form():
    website = request.form.get('website')
    if website:
        return jsonify({'status': 'Bot detected'}), 403

    name = request.form.get('name')
    email = request.form.get('email')
    print(f"Form submission from {name} ({email})")
    return jsonify({'status': 'Form submitted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
