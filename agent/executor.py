import json
import platform
import secrets

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import load_prompt
from steps import Step, load_steps
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory

class Executor:
    def __init__(self):
        llm = ChatOpenAI(model_name="gpt-4", temperature=0)
        self.chain = LLMChain(
            llm=llm,
            prompt=load_prompt("prompts/platform_prompt.yaml"),
            memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True),
        )
        self.cached_outputs = {}
        self.os = platform.system()

    def setup_vector_store(self):

        self.vector_store = FAISS(embeddings=OpenAIEmbeddings())
    
    def __call__(self, platform):
        output = self.chain.run({"platform": platform, "os": self.os, "build_folder": "../sample-app/dist", "nonce": secrets.token_hex(8)})
        json_steps = json.loads(output)# ["steps"]
        steps = load_steps(json_steps)
        
        with open("steps.json", "w") as f:
            json.dump(json_steps, f, indent=4)

        for step in steps:
            step.exe(platform)
