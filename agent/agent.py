import json
import os
import secrets

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import load_prompt
from executor import Executor

load_dotenv()

tools = []
llm = ChatOpenAI(model_name="gpt-4", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

init = LLMChain(
    llm=llm,
    prompt=load_prompt("prompts/init_prompt.yaml"),
)

platform = "AWS" # init.run("I want to deploy a react app with AWS")
print(f"Platform: {platform}\n")

e = Executor()
e(platform)