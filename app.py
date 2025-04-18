from flask import Flask, render_template, jsonify
import subprocess
import sys
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/run-detection')
def run_detection():
    try:
        # Get full path to eye_blink_detector.py
        script_path = os.path.join(os.getcwd(), 'eye_blink_detector.py')
        # Use sys.executable to ensure correct Python from virtualenv
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=30)

        print(f"Detection output (stdout): {result.stdout}")
        print(f"Detection output (stderr): {result.stderr}")

        if result.returncode != 0:
            return jsonify({'output': [f"❌ Script execution failed with error code {result.returncode}:"] + result.stderr.split('\n')})

        output_lines = result.stdout.strip().split('\n')
        summary = output_lines[-6:] if len(output_lines) >= 6 else output_lines

        return jsonify({'output': summary})
    except subprocess.TimeoutExpired:
        return jsonify({'output': ['❌ Detection timed out.']})
    except Exception as e:
        return jsonify({'output': [f'❌ Error occurred: {str(e)}']})

if __name__ == '__main__':
    app.run(debug=True)
