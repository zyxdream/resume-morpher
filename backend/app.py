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
    
    # openAI call
    # pack up job with job_id and content
    job = {'job_id': 0, 'content': input2}
    resume_query = ResumeQueryGenerator(resume=input1, job=job)
    result = ResumeGenerator(resume_query)

    print(result)
    # print('sending back :', result)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)

