import os

from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.tools import ShellTool
from langchain.llms import OpenAI
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(temperature=0, openai_api_key=os.environ["OPENAI_API_KEY"])

tools = load_tools(["serpapi", "llm-math"], llm=llm)

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

agent.run("Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?")