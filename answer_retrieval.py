from transformers.pipelines import pipeline
from transformers import AutoModelForQuestionAnswering
from transformers import AutoTokenizer
from urllib.request import urlopen
from bs4 import BeautifulSoup

model_name = "deepset/xlm-roberta-base-squad2"

# a) Get predictions
nlp = pipeline("question-answering", model=model_name, tokenizer=model_name)

# b) Load model & tokenizer
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)


def get_answer(context, question):
    input = {"question": question, "context": context}
    res = nlp(input)
    return res


def retrieve_webpage_text(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = "\n".join(chunk for chunk in chunks if chunk)

    return text


def get_webpage_answer(url, question):
    context = retrieve_webpage_text(url)
    input = {"question": question, "context": context}
    res = nlp(input)
    return res
