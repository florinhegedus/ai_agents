import os
import requests
from dotenv import load_dotenv
from smolagents import CodeAgent, OpenAIServerModel
from typing import Dict


load_dotenv()
DEFAULT_API_URL = "https://agents-course-unit4-scoring.hf.space"


def fetch_file_content(task_id: str):
    api_url = DEFAULT_API_URL
    files_url = f"{api_url}/files/{task_id}"

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
        with open("system_prompt.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read()
        model = OpenAIServerModel(
            model_id="gpt-4o",
            api_base="https://api.openai.com/v1",
            api_key=os.environ["OPENAI_API_KEY"],
        )
        self.agent = CodeAgent(tools=[], 
                               model=model, 
                               add_base_tools=True,
                               additional_authorized_imports=["requests", "markdownify"],
                            )
        self.agent.system_prompt += system_prompt
        print(self.agent.system_prompt)

    def __call__(self, task: Dict) -> str:
        task_id = task.get("task_id")
        question = task.get("question")
        file_name = task.get("file_name", "")

        if file_name != "":
            question += f"To resolve the task you are provided with an additional file: {file_name}."
            question += f"Data extracted from file: "

            # Save file content locally
            file_content= fetch_file_content(task_id)
            with open(file_name, "wb") as file:
                file.write(file_content)

            if file_name[-4:] == ".mp3":
                from openai import OpenAI

                client = OpenAI()
                audio_file = open(file_name, "rb")
                transcription = client.audio.transcriptions.create(
                    model="gpt-4o-transcribe", 
                    file=audio_file
                )
                question += "transcription from audio: "
                question += transcription.text
            elif file_name[-5:] == ".xlsx":
                import pandas as pd

                df = pd.read_excel(file_name)

                question += "Dataframe: "
                question += str(df)
            elif file_name[-3:] == ".py":
                python_file = open(file_name, "r")
                code = python_file.read()
                question += "Code: "
                question += code
            elif file_name[-4:] == ".png":
                import base64
                from openai import OpenAI

                client = OpenAI()

                # Function to encode the image
                def encode_image(image_path):
                    with open(image_path, "rb") as image_file:
                        return base64.b64encode(image_file.read()).decode("utf-8")

                # Getting the Base64 string
                base64_image = encode_image(file_name)

                response = client.responses.create(
                    model="gpt-4.1",
                    input=[
                        {
                            "role": "user",
                            "content": [
                                { "type": "input_text", "text": "what's in this image?" },
                                {
                                    "type": "input_image",
                                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                                },
                            ],
                        }
                    ],
                )

                question += "Image description: "
                question += response.output_text
                

        response = self.agent.run(question)
    
        return response
