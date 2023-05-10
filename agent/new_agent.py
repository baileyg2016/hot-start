from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(temperature=0, model_name="gpt-4")#, model_name="gpt-3.5-turbo")

tools = load_tools(["serpapi", "terminal"], llm=llm)
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
agent.run("How do i deploy my react app to Azure? The build output is here ../sample-app/dist")