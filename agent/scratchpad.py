import json
import os

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import load_prompt
from utils import log

# need this for API key
load_dotenv()

code_chain = LLMChain(
    llm=ChatOpenAI(temperature=0, model_name="gpt-4"), 
    prompt=load_prompt("prompts/code_prompt.yaml"),
    verbose=True
)

steps_chain = LLMChain(
    llm=ChatOpenAI(temperature=0, model_name="gpt-4"),
    prompt=load_prompt("prompts/build_prompt.yaml"),
)


output = code_chain.run("I want the app to output a smily face")
data = json.loads(output)
path = 'web'
os.makedirs(path, exist_ok=True)
log(output, "green")
for file_path, content in data.items():
    os.makedirs(os.path.join(path, os.path.dirname(file_path)), exist_ok=True)

    with open(os.path.join(path, file_path), 'w') as f:
        f.write(content)

log("Getting steps\n", "green")
steps = steps_chain.run({ "path": path, "json": output })
print(steps)