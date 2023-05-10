from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import load_prompt
import json
import secrets
from steps import Step, load_steps

class Executor:
    def __init__(self):
        llm = ChatOpenAI(model_name="gpt-4", temperature=0)
        self.chain = LLMChain(
            llm=llm,
            prompt=load_prompt("prompts/platform_prompt.yaml"),
        )
        self.cached_outputs = {}
    
    def __call__(self, platform):
        output = self.chain.run({"platform": platform, "build_folder": "../sample-app/dist", "nonce": secrets.token_hex(8)})
        json_steps = json.loads(output)# ["steps"]
        steps = load_steps(json_steps)

        for step in steps:
            step.exe(platform)
