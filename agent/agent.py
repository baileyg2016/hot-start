import json
import os
import re
import secrets
import subprocess
from typing import Dict, List, Optional, Tuple, Union

from dotenv import load_dotenv
from langchain.agents import Tool
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts import BaseChatPromptTemplate, load_prompt
from langchain.schema import AgentAction, AgentFinish, HumanMessage
from langchain.tools import ShellTool

load_dotenv()

tools = []
# llm = OpenAI(temperature=0, openai_api_key=os.environ["OPENAI_API_KEY"])
llm = ChatOpenAI(model_name="gpt-4", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"Error executing command: {command}")
        print(f"Error: {stderr.decode('utf-8')}")
        exit(0)
    else:
        print(f"Command executed successfully: {command}")
        print(f"Output: {stdout.decode('utf-8')}")

    return stdout.decode('utf-8')

def find_key(command):
    start = command.find("<")
    end = command.find(">")

    return command[start+1:end] if start != -1 and end != -1 else None

def replace_placeholder(command, value, cache=None):
    start = command.find("<")
    end = command.find(">")

    if start != -1 and end != -1:
        key = command[start+1:end]
        if cache is not None:
            cache[key] = value
        return command[:start] + value + command[end+1:]
    else:
        return command

init = LLMChain(
    llm=llm,
    prompt=load_prompt("init_prompt.yaml"),
)

platform = init.run("I want to deploy a react app with AWS")
print(f"Platform: {platform}\n")

chain = LLMChain(
    llm=llm,
    prompt=load_prompt("platform_prompt.yaml"),
)

output = chain.run({"platform": platform, "build_folder": "../sample-app/dist", "nonce": secrets.token_hex(8)})
print(f"Output: {output}\n")
steps = json.loads(output)

prev_cmd_output = None

cache_outputs = {}

for step in steps:
    print(step["description"])
    cmd = step["command"]

    if "<" in cmd and ">" in cmd:
        key = find_key(cmd)
        if key in cache_outputs:
            cmd = replace_placeholder(cmd, cache_outputs[key])
        else:
            cmd = replace_placeholder(cmd, prev_cmd_output, cache_outputs)
    prev_cmd_output = run_command(cmd)

