import os
import requests
from dotenv import load_dotenv
from smolagents import CodeAgent, OpenAIServerModel
from openai import OpenAI
from typing import Dict

from tools import get_xlsx_summary


load_dotenv()

DEFAULT_API_URL = "https://agents-course-unit4-scoring.hf.space"


def fetch_file_content(task: Dict):
    api_url = DEFAULT_API_URL
    files_url = f"{api_url}/files/{task.get("task_id")}"

    # Fetch files
    print(f"Fetching files from: {files_url}")
    try:
        response = requests.get(files_url, timeout=60)
        response.raise_for_status()
        if response.status_code == 200:
            return response.content
    except Exception as e:
        print(f"An unexpected error occurred fetching file: {e}")
        return f"An unexpected error occurred fetching file: {e}", None


class BasicAgent:
    def __init__(self):
        print("BasicAgent initialized.")
        model = OpenAIServerModel(
            model_id="gpt-4o",
            api_base="https://api.openai.com/v1",
            api_key=os.environ["OPENAI_API_KEY"],
        )
        self.agent = CodeAgent(tools=[], model=model, add_base_tools=True)

    def __call__(self, task: Dict) -> str:
        task_id = task.get("task_id")
        question = task.get("question")
        file_name = task.get("file_name")

        if file_name is not None:
            file_content = fetch_file_content(task)
            if file_name[-4:] == ".mp3":
                print("Processing audio file")
            elif file_name[-5:] == ".xlsx":
                print("Processing excel file")
            elif file_name[-3:] == ".py":
                print("Processing python file")
            elif file_name[-4:] == ".png":
                print("Processing image file")

        response = self.agent.run(question)
    
        return response
    

if __name__ == '__main__':
    model = OpenAIServerModel(
        model_id="gpt-4o",
        api_base="https://api.openai.com/v1",
        api_key=os.environ["OPENAI_API_KEY"],
    )

    agent = CodeAgent(tools=[], model=model, add_base_tools=True)

    agent.run(
        "What is the weather like in Timisoara right now?",
    )
