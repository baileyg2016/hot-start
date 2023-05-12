import json
import os
import secrets

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import load_prompt
from executor import Executor
from utils import log

load_dotenv()

tools = []
llm = ChatOpenAI(model_name="gpt-4", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

init = LLMChain(
    llm=llm,
    prompt=load_prompt("prompts/init_prompt.yaml"),
)

human = LLMChain(
    llm=llm,
    prompt=load_prompt("prompts/human_steps_prompt.yaml"),
)

code = LLMChain(
    llm=llm,
    prompt=load_prompt("prompts/permissions_prompt.yaml"),
)
steps = json.loads(open("steps.json", "r").read())
commands = [step['command'] for step in steps]
# log(human.run({"platform": "AWS", "commands": commands}), "yellow")

# steps to creating permissions, might not need
# output = code.run({"steps": commands, "username": "bspell20"})
# with open("permissions.py", "w") as f:
#     f.write(output)
# log(output, "yellow")

platform = "Azure" # init.run("I want to deploy a react app with AWS")
log(f"Platform: {platform}\n", "white")

e = Executor()
e(platform)