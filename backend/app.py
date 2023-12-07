from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/morph', methods=['POST'])
def morph():
    data = request.json
    input1 = data.get('input1', '')
    input2 = data.get('input2', '')
    
    # TODO: add the openAI call here
    result = input1 + " " + input2
    # print('sending back :', result)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)