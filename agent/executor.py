import json
import platform
import secrets

import faiss
from langchain.chains import LLMChain, ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import (ConversationBufferMemory,
                              VectorStoreRetrieverMemory)
from langchain.prompts import load_prompt
from langchain.vectorstores import FAISS
from steps import Step, load_steps

class Executor:
    def __init__(self):
        embedding_size = 1536 # Dimensions of the OpenAIEmbeddings
        index = faiss.IndexFlatL2(embedding_size)
        embedding_fn = OpenAIEmbeddings().embed_query
        vectorstore = FAISS(embedding_fn, index, InMemoryDocstore({}), {})

        # In actual usage, you would set `k` to be a higher value, but we use k=1 to show that
        # the vector lookup still returns the semantically relevant information
        retriever = vectorstore.as_retriever(search_kwargs=dict(k=1))
        self.memory = VectorStoreRetrieverMemory(retriever=retriever)

        llm = ChatOpenAI(model_name="gpt-4", temperature=0)
        self.chain = LLMChain(
            llm=llm,
            prompt=load_prompt("prompts/platform_prompt.yaml"),
            memory=self.memory,
            verbose=True
        )

        # doing this because I am too lazy to copy and paste the code
        self.buffer = ConversationChain(
            llm=llm,
            prompt=load_prompt("prompts/platform_prompt.yaml"),
            memory=self.memory,
            verbose=True
        )

        self.cached_outputs = {}
        self.os = platform.system()

    def setup_vector_store(self):

        self.vector_store = FAISS(embeddings=OpenAIEmbeddings())
    
    def __call__(self, platform):
        # need to figure out how to get the memory
        output = self.chain.run({"platform": platform, "os": self.os, "build_folder": "../sample-app/dist", "nonce": secrets.token_hex(8), "history":  })
        json_steps = json.loads(output)# ["steps"]
        steps = load_steps(json_steps)
        
        with open("steps.json", "w") as f:
            json.dump(json_steps, f, indent=4)

        for step in steps:
            success, output = step.exe(platform)
            if success:
                self.memory.save_context({ "input": step.command } , { "output": output })
