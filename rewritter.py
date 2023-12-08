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


load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
print("here")

def QueryGenerator(resume, jobs):
    queries = []
    for idx, job in enumerate(jobs):
        jobId = job["job_id"]
        print(jobId)
        jobContent = job["content"]
        query = {"job_id": jobId,
                 "resume_prompt": "Rewrite my resume tailored to the following specific job_posting. Try to repharase my experiences, projects and eductation that are most relevant to the job descriptions and responsibilities to make my resume look more competitive. Narrow down history to only list relevant roles or experiences. Format my resume so that it is easy to identify my qualifications for this specific job. \n === my resume: {} ====\n === job posting: {}\n === the rewritten resume :".format(
                     resume, jobContent),
                 "letter_prompt": "A cover letter is a one-page document you send with your resume that provides additional information about skills and experiences related to the job you're pursuing. It typically includes three to four short paragraphs. A cover letter is important because it serves as the first chance for the recruiter to see the qualifications that make you a good fit for the position. Write a cover cover for the following job, based on the following resume. === job posting : {}\n ==== my resume: {} =====\n the cover letter :".format(
                     jobContent, resume)}

        queries.append(query)
    return queries

def ResponseGenerator(query, out_dir):
    id = query["job_id"]
    print("job ", id)
    resume_prompt = query["resume_prompt"]
    # print("=== resume prompty ===\n", resume_prompt)
    letter_prompt = query["letter_prompt"]
    # print("=== letter prompt ===\n", letter_prompt)

    completion = client.completions.create(model="gpt-3.5-turbo-instruct", prompt=resume_prompt, max_tokens=1024)
    response = completion.choices[0].text
    print(f'resume-response: {response}')
    print("==== ====")
    filename = out_dir + "resume-" + str(id)
    print(filename)
    with open(filename, 'w') as outfile:
        outfile.write(response)

    completion = client.completions.create(model="gpt-3.5-turbo-instruct", prompt=letter_prompt, max_tokens=1024)
    response = completion.choices[0].text
    print(f'letter-response: {response}')
    print("==== END OF RESPONSE ====")
    filename = out_dir + "letter-" + str(id)
    print(filename)
    with open(filename, 'w') as outfile:
        outfile.write(response)


if __name__ == "__main__":
    # load resume and job postings
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

        jobs.append({"job_id":file,"content":content})
    print(len(jobs))

    # combine resume and job posting to generating queries for rewriting resume and writing cover letters
    queries = QueryGenerator(resume, jobs)
    print(len(queries))
    # let llm complete response and save
    out_dir = "./output/"
    for query in queries:
        print(query["job_id"])
        ResponseGenerator(query, out_dir)



