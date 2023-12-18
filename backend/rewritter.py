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

# combine resume and job posting to generating queries for rewriting resume
def ResumeQueryGenerator(resume, job):
    jobId = job["job_id"]
    print(jobId)
    jobContent = job["content"]
    query = {"job_id": jobId,
             "prompt": "Rewrite my resume tailored to the following specific job_posting. Try to repharase my experiences, projects and eductation that are most relevant to the job descriptions and responsibilities to make my resume look more competitive. Narrow down history to only list relevant roles or experiences. Format my resume so that it is easy to identify my qualifications for this specific job. \n === my resume: {} ====\n === job posting: {}\n === the rewritten resume :".format(
                 resume, jobContent)}
    return query

# combine resume and job posting to generating queries for writing cover letters
def LetterQueryGenerator(resume, job):
    jobId = job["job_id"]
    print(jobId)
    jobContent = job["content"]
    query = {"job_id": jobId,
             "prompt": "A cover letter is a one-page document you send with your resume that provides additional information about skills and experiences related to the job you're pursuing. It typically includes three to four short paragraphs. A cover letter is important because it serves as the first chance for the recruiter to see the qualifications that make you a good fit for the position. Write a cover cover for the following job, based on the following resume. === job posting : {}\n ==== my resume: {} =====\n the cover letter :".format(
                 jobContent, resume)}
    return query

def ResumeGenerator(resume_query):
    id = resume_query["job_id"]
    print("job ", id)
    resume_prompt = resume_query["prompt"]
    # print("=== resume prompty ===\n", resume_prompt)
    completion = client.completions.create(model="gpt-3.5-turbo-instruct", prompt=resume_prompt, max_tokens=1024)
    return completion.choices[0].text

def CoverLetterGenerator(letter_query):
    id = letter_query["job_id"]
    print("job ", id)
    letter_prompt = letter_query["prompt"]
    # print("=== letter prompt ===\n", letter_prompt)
    completion = client.completions.create(model="gpt-3.5-turbo-instruct", prompt=letter_prompt, max_tokens=1024)
    response = completion.choices[0].text
    return response


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

    # let llm complete response and save
    out_dir = "./output/"
    for job in jobs:
        jobId = job["job_id"]
        task = "resume"
        resume_query = ResumeQueryGenerator(resume, job)
        new_resume = ResumeGenerator(resume_query)

        filename = out_dir + task + "-" + str(jobId)
        print(filename)
        with open(filename, 'w') as outfile:
            outfile.write(new_resume)

        task = "letter"
        letter_query = LetterQueryGenerator(resume, job)
        cover_letter = CoverLetterGenerator(letter_query)
        filename = out_dir + task + "-" + str(jobId)
        print(filename)
        with open(filename, 'w') as outfile:
            outfile.write(cover_letter)