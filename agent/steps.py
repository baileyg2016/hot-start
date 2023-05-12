import subprocess

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import load_prompt
from utils import log
import json

class Step:
    def __init__(self, description, command):
        self.description = description
        self.command = command.replace("\'", "\"")
        self.key = self.find_key()

    def find_key(self):
        self.start = self.command.find("<")
        self.end = self.command.find(">")

        return self.command[self.start+1:self.end] if self.start != -1 and self.end != -1 else None
    
    def replace_placeholder(self, command, value, cache=None):
        if self.key is not None:
            # key = command[start+1:end]
            if cache is not None:
                cache[self.key] = value
            return command[:self.start] + value + command[self.end+1:]
        else:
            return command
        

    def exe(self, platform, memory):
        process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        output = stdout.decode('utf-8')

        if process.returncode != 0:
            info = f"Error executing command: {self.command}"
            error = f"Error: {stderr.decode('utf-8')}"
            log(info, "red")
            log(error, "red")
            self.retry(error, platform, memory)
            self.exe(platform, memory)
            
        else:
            log(f"Command executed successfully: {self.command}")
            log(f"Output: {output}\n")
            memory.save_context({ "command": self.command } , { "command output": output })

        return True, output
    
    def retry(self, error, platform, memory):
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        chain = LLMChain(
            llm=llm,
            prompt=load_prompt("prompts/retry_failed_prompt.yaml"),
            memory=memory
        )
        log("\nFinding a fix for the error...", "yellow")

        output = chain.run({"input": self.command, "platform": platform, "error_message": error})
        output = json.loads(output)
        self.command = output["command"]
        self.description = output["description"]
        log(f"Fixing with: {self.description}", "yellow")
        log(f"Found a new command: {output}\n", "yellow")

def load_steps(steps):
    return [Step(step["description"], step["command"]) for step in steps]