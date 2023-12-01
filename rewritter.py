#  ******
#  Re-write resume based on different job postings
# *****
# resume in folder "./data/resume_jobs/"  (textfile, free format)
# job postings in folder "./data/resume_jobs/jobs/  (textfile, json schema:
# {"title":"", "company":"", "location":"", "Qualification":"", "Responsibilities":"", "Job description":""}
# job0 is intended to be left empty (Benchmark)

# responses are saved in folder "./data/output/"

import os
from dotenv import load_dotenv

from openai import OpenAI
from llama_index import VectorStoreIndex, SimpleDirectoryReader

load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
print("here")

file_path = "./data/resume_jobs/resume"
with open(file_path) as inf:
    resume = inf.read()

# print(resume)

jobs = []
dir_path_in = "./data/resume_jobs/jobs/"
for file in os.listdir(dir_path_in):
    file_path = dir_path_in + file
    with open(file_path) as inf:
        content = inf.read()
        # print("read from ", file_path)
        # print(job)
        jobs.append({"job_id":file,"content":content})

# print(jobs)

queries = []
for idx, job in enumerate(jobs):
    jobId = job["job_id"]
    jobContent = job["content"]
    query = {"job_id":jobId, "content":"Rewrite my resume tailored to the following specific job_posting. Try to repharase my experiences, projects and eductation that are most relevant to the job descriptions and responsibilities to make my resume look more competitive. Narrow down history to only list relevant roles or experiences. Format my resume so that it is easy to identify my qualifications for this specific job. \n === my resume: {} ====\n === job posting: {}\n === the rewritten resume :".format(resume, jobContent)}
    queries.append(query)


dir_path_out = "./output/"

for query in queries:
    id = query["job_id"]
    q = query["content"]
    print("*************")
    print(q)
    print("************")
    completion = client.completions.create(model="gpt-3.5-turbo-instruct", prompt=q, max_tokens=1024)
    response = completion.choices[0].text
    print(f'response: {response}')
    print("==== END OF RESPONSE ====")
    filename = dir_path_out + "response-" + str(id)
    with open(filename, 'w') as outfile:
        outfile.write(response)