import os
from collections import deque
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from langchain import LLMChain, OpenAI, PromptTemplate
from langchain.chains.base import Chain
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
from langchain.experimental import BabyAGI
from langchain.llms import BaseLLM
from langchain.vectorstores import FAISS
from langchain.vectorstores.base import VectorStore
from pydantic import BaseModel, Field

load_dotenv()

# Define your embedding model
embeddings_model = OpenAIEmbeddings()
# Initialize the vectorstore as empty
import faiss

embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})

OBJECTIVE = "What is the weather going to be like next week in SF? Specifically, Tuesday through Sunday."
llm = OpenAI(temperature=0, openai_api_key=os.environ["OPENAI_API_KEY"])
# Logging of LLMChains
verbose = False
# If None, will keep on going forever
max_iterations: Optional[int] = 7
baby_agi = BabyAGI.from_llm(
    llm=llm, vectorstore=vectorstore, verbose=verbose, max_iterations=max_iterations
)

baby_agi({"objective": OBJECTIVE})