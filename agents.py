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
    

# class CustomModel(Model):
#     def generate(messages, stop_sequences=["Task"]):
#         response = client.chat_completion(messages, stop=stop_sequences, max_tokens=1024)
#         answer = response.choices[0].message
#         return answer
    

if __name__ == '__main__':
    model = OpenAIServerModel(model_id='deepseek-chat', api_base='https://api.deepseek.com', api_key=os.environ['DEEPSEEK_API_KEY'])

    agent = CodeAgent(tools=[], model=model, add_base_tools=True)

    agent.run(
        "What is the weather like in Timisoara right now?",
    )

    client = OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"},
        ],
        stream=False
    )

    print(response.choices[0].message.content)

