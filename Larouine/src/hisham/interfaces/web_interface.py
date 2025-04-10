from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/status')
def get_status():
    return jsonify({
        'status': 'active',
        'version': '1.2.3',
        'pending_updates': 2
    })

def start_web_server():
    app.run(port=5000)