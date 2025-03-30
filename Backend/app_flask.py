from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)

def processimage(teacherans, studentans):
    return 80

@app.route('/run_my_script', methods=['POST'])
def run_my_script():
    try:
        if request.content_type.startswith('multipart/form-data'):
            teacherans = request.files.get('teacherans')
            studentans = request.files.get('studentans')
            if not teacherans or not studentans:
                return jsonify({'error': 'Missing files'}), 400
            if teacherans.filename.rsplit('.', 1)[-1].lower() in ('jpg', 'jpeg', 'png'):
                result = processimage(teacherans, studentans)
                return jsonify({'result': result})
            else:
                return jsonify({'error': 'Invalid file type'}), 400
        elif request.content_type == 'application/json':
            data = request.get_json()
            if 'teacherans' not in data or 'studentans' not in data:
                return jsonify({'error': 'Missing input_data parameter'}), 400
            
            # Path to the virtual environment's Python executable
            venv_python = os.path.join('.venv', 'Scripts', 'python.exe')
            
            result = subprocess.run([venv_python, 'Evaluation_model.py', data['teacherans'], data['studentans']],
                                    capture_output=True, text=True)
            if result.returncode == 0:
                return jsonify({'result': result.stdout.strip()})
            else:
                print(result.stderr.strip())
                return jsonify({'error': result.stderr.strip()}), 500
        else:
            return jsonify({'error': 'Unsupported Content-Type'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
