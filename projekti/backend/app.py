from flask import Flask, request, jsonify
from analyzer import CVAnalyzer

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    analyzer = CVAnalyzer(data['cv'], data['job'])
    result = analyzer.analyze()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
