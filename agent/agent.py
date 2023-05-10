import json
import os
import secrets
import subprocess

from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import load_prompt
from langchain.tools import ShellTool
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import BaseChatPromptTemplate
from langchain import SerpAPIWrapper, LLMChain
from langchain.chat_models import ChatOpenAI
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, HumanMessage
import re

load_dotenv()

tools = []
# llm = OpenAI(temperature=0, openai_api_key=os.environ["OPENAI_API_KEY"])
llm = ChatOpenAI(model_name="gpt-4", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

# Set up a prompt template
class CustomPromptTemplate(BaseChatPromptTemplate):
    # The template to use
    template: str
    # The list of tools available
    tools: List[Tool]
    
    def format_messages(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        formatted = self.template.format(**kwargs)
        return [HumanMessage(content=formatted)]

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

def replace_placeholder(command, value, cache):
    start = command.find("<")
    end = command.find(">")

    if start != -1 and end != -1:
        key = command[start+1:end]
        cache[key] = value
        return command[:start] + value + command[end+1:]
    else:
        return command

init = LLMChain(
    llm=llm,
    prompt=load_prompt("init_prompt.yaml"),
)

platform = init.run("I want to deploy a react app with Azure")

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
        cmd = replace_placeholder(cmd, prev_cmd_output)
    prev_cmd_output = run_command(cmd)

