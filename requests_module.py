from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/respond', methods=['GET'])
def respond():
    text = request.args.get('text', type=str)
    if text and text.lower() == 'hello':
        return jsonify({'response': "What's up"})
    else:
        return jsonify({'response': 'Unrecognized input'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)