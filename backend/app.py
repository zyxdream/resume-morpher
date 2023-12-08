from flask import Flask, request, jsonify
from flask_cors import CORS
from rewritter import ResumeQueryGenerator, ResumeGenerator
import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
print("here")

app = Flask(__name__)
CORS(app)

@app.route('/morph', methods=['POST'])
def morph():
    data = request.json
    input1 = data.get('input1', '')
    input2 = data.get('input2', '')
    print("hi, type of input2 is ", type(input2))

    # TODO: add the openAI call here

    resume_query = ResumeQueryGenerator(resume=input1, job=input2)
    result = ResumeGenerator(resume_query)
    # print('sending back :', result)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)