import os
import pandas as pd
import requests
from typing import List, Dict

from agents import BasicAgent


DEFAULT_API_URL = "https://agents-course-unit4-scoring.hf.space"
FILES_DIR = "files_for_tasks"


def query_all_questions():
    api_url = DEFAULT_API_URL
    questions_url = f"{api_url}/questions"

    # Fetch questions
    print(f"Fetching questions from: {questions_url}")
    try:
        response = requests.get(questions_url, timeout=15)
        response.raise_for_status()
        questions_data = response.json()
        if not questions_data:
             print("Fetched questions list is empty.")
             return "Fetched questions list is empty or invalid format.", None
        print(f"Fetched {len(questions_data)} questions.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching questions: {e}")
        return f"Error fetching questions: {e}", None
    except requests.exceptions.JSONDecodeError as e:
         print(f"Error decoding JSON response from questions endpoint: {e}")
         print(f"Response text: {response.text[:500]}")
         return f"Error decoding server response for questions: {e}", None
    except Exception as e:
        print(f"An unexpected error occurred fetching questions: {e}")
        return f"An unexpected error occurred fetching questions: {e}", None
    
    return questions_data


def get_files_for_task(task: Dict):
    api_url = DEFAULT_API_URL
    files_url = f"{api_url}/files/{task.get("task_id")}"

    # Fetch files
    print(f"Fetching files from: {files_url}")
    try:
        response = requests.get(files_url, timeout=60)
        response.raise_for_status()
        if response.status_code == 200:
            file_path = FILES_DIR + "/" + task.get("file_name")
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"Succesfully saved file {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred fetching files: {e}")
        return f"An unexpected error occurred fetching files: {e}", None


def fetch_files(questions_data: List[Dict]):
    os.makedirs(FILES_DIR, exist_ok=True)
    for task in questions_data:
        if task.get("file_name", "") != "":
            get_files_for_task(task)


def run_agent(questions_data):
    try:
        agent = BasicAgent()
    except Exception as e:
        print(f"Error instantiating agent: {e}")
        return f"Error initializing agent: {e}", None

    results_log = []
    answers_payload = []
    print(f"Running agent on {len(questions_data)} questions...")
    for item in questions_data:
        task_id = item.get("task_id")
        question_text = item.get("question")
        if not task_id or question_text is None:
            print(f"Skipping item with missing task_id or question: {item}")
            continue
        try:
            submitted_answer = agent(question_text)
            answers_payload.append({"task_id": task_id, "submitted_answer": submitted_answer})
            results_log.append({"Task ID": task_id, "Question": question_text, "Submitted Answer": submitted_answer})
        except Exception as e:
             print(f"Error running agent on task {task_id}: {e}")
             results_log.append({"Task ID": task_id, "Question": question_text, "Submitted Answer": f"AGENT ERROR: {e}"})

    if not answers_payload:
        print("Agent did not produce any answers to submit.")
        return "Agent did not produce any answers to submit.", pd.DataFrame(results_log)
    
    return results_log, answers_payload


if __name__ == '__main__':
    questions_data = query_all_questions()
    fetch_files(questions_data)
    results_log, answers_payload = run_agent(questions_data)
    print(results_log)

