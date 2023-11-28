# RAG intuition, without using llama-index
# original code:
# https://colab.research.google.com/github/DanielWarfield1/MLWritingAndResearch/blob/main/RAGFromScratch.ipynb#scrollTo=_cTk6k--hFjO

# download and save document
# >>> mkdir -p 'data/paul_graham/'
# >>> wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'


"""Downloading a word encoder.
I was going to use word2vect, but glove downloads way faster. For our purposes
they're conceptually identical
"""
import gensim.downloader
import numpy as np
from scipy.spatial.distance import cdist

from openai import OpenAI  # import openai is deprecated
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
print("here")

#doenloading encoder
word_encoder = gensim.downloader.load('glove-twitter-25')

#getting the embedding for a word
print(word_encoder['apple'])


def embed_sequence(sequence):
    vects = word_encoder[sequence.split(' ')]
    return np.mean(vects, axis=0)

embed_sequence('its a sunny day today')

def calc_distance(embedding1, embedding2):
    return cdist(np.expand_dims(embedding1, axis=0), np.expand_dims(embedding2, axis=0), metric='cityblock')[0][0]

print('similar phrases:')
print(calc_distance(embed_sequence('sunny day today')
                  , embed_sequence('rainy morning presently')))

print('different phrases:')
print(calc_distance(embed_sequence('sunny day today')
                  , embed_sequence('perhaps reality is painful')))

# similar phrases:
# 8.496297497302294
# different phrases:
# 11.832107525318861

"""Defining documents
for simplicities sake I only included words the embedder knows. You could just
parse out all the words the embedder doesn't know, though. After all, the retreival
is done on a mean of all embeddings, so a missing word or two is of little consequence
"""
documents = {"menu": "ratatouille is a stew thats twelve dollars and fifty cents also gazpacho is a salad thats thirteen dollars and ninety eight cents also hummus is a dip thats eight dollars and seventy five cents also meat sauce is a pasta dish thats twelve dollars also penne marinera is a pasta dish thats eleven dollars also shrimp and linguini is a pasta dish thats fifteen dollars",
             "events": "on thursday we have karaoke and on tuesdays we have trivia",
             "allergins": "the only item on the menu common allergen is hummus which contain pine nuts",
             "info": "the resteraunt was founded by two brothers in two thousand and three"}


"""defining a function that retreives the most relevent document
"""

def retreive_relevent(prompt, documents=documents):
    min_dist = 1000000000
    r_docname = ""
    r_doc = ""

    for docname, doc in documents.items():
        dist = calc_distance(embed_sequence(prompt)
                           , embed_sequence(doc))

        if dist < min_dist:
            min_dist = dist
            r_docname = docname
            r_doc = doc

    return r_docname, r_doc


prompt = 'what pasta dishes do you have'
print(f'finding relevent doc for "{prompt}"')
print(retreive_relevent(prompt))
print('----')
prompt = 'what events do you guys do'
print(f'finding relevent doc for "{prompt}"')
print(retreive_relevent(prompt))

"""Defining retreival and augmentation
creating a function that does retreival and augmentation,
this can be passed straight to the model
"""
def retreive_and_agument(prompt, documents=documents):
    docname, doc = retreive_relevent(prompt, documents)
    return f"Answer the customers prompt based on the folowing documents:\n==== document: {docname} ====\n{doc}\n====\n\nprompt: {prompt}\nresponse:"

prompt = 'what events do you guys do'
print(f'prompt for "{prompt}":\n')
print("*****")
print(retreive_and_agument(prompt))
print("*****")


prompts = ['what pasta dishes do you have', 'what events do you guys do', 'oh cool what is karaoke']

for prompt in prompts:
    print(f'original prompt: "{prompt}"')
    ra_prompt = retreive_and_agument(prompt)
    print(f'ra prompt: "{ra_prompt}"')
    completion = client.completions.create(model="gpt-3.5-turbo-instruct", prompt=ra_prompt, max_tokens=80)
    response = completion.choices[0].text
    print(f'response: {response}')


