import json
import os
import platform
import secrets

import faiss
# from CustomChain import MyCustomChain
from customvectorstore import CustomVectorStoreRetrieverMemory
from langchain.chains import ConversationChain, LLMChain
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
        # TODO: ideally k is 2. Wonder if we can use an SVM
        retriever = vectorstore.as_retriever(search_kwargs=dict(k=2), search_type="mmr")
        self.memory = VectorStoreRetrieverMemory(retriever=retriever, input_key="input")

        llm = ChatOpenAI(model_name="gpt-4", temperature=0)
        self.chain = LLMChain(
            llm=llm,
            prompt=load_prompt("prompts/platform_prompt.yaml"),
            verbose=True
        )

        self.cached_outputs = {}
        self.os = platform.system()
    
    def __call__(self, platform):
        # need to figure out how to get the memory
        output = self.chain.run({"platform": platform, "os": self.os, "build_folder": "../sample-app/dist", "nonce": secrets.token_hex(8)})
        json_steps = json.loads(output)
        steps = load_steps(json_steps)

        if os.getenv("DEBUG") == "True":
            with open("steps.json", "w") as f:
                json.dump(json_steps, f, indent=4)

        for step in steps:
            success, output = step.exe(platform, self.memory)

        print(f"Done you can visit here: {output}")
