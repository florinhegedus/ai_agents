import os
from dotenv import load_dotenv
from smolagents import CodeAgent, OpenAIServerModel
from openai import OpenAI

from tools import get_xlsx_summary


load_dotenv()


class BasicAgent:
    def __init__(self):
        print("BasicAgent initialized.")
    def __call__(self, question: str, file_path: str) -> str:
        print(f"Agent received question (first 50 chars): {question[:50]}...")
        fixed_answer = "This is a default answer."
        print(f"Agent returning fixed answer: {fixed_answer}")

        # The decision what tool to use for each file will be taken by the agent
        if file_path is not None:
            if file_path[-4:] == ".mp3":
                print("Processing audio file")
            elif file_path[-5:] == ".xlsx":
                print("Processing excel file")
            elif file_path[-3:] == ".py":
                print("Processing python file")
            elif file_path[-4:] == ".png":
                print("Processing image file")
    
        return fixed_answer
    

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
