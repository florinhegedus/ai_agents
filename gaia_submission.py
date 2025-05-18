import json
from datasets import load_dataset
from agents import BasicAgent


def main():
    # Please pick one among the available configs: ['2023_all', '2023_level1', '2023_level2', '2023_level3']
    gaia_dataset = load_dataset('gaia-benchmark/GAIA', '2023_level1')
    
    print(f"Validation: {len(gaia_dataset['validation'])}")
    print(f"Validation: {len(gaia_dataset['test'])}")

    print(f"Keys: {gaia_dataset['validation'].features.keys()}")

    try:
        agent = BasicAgent()
    except Exception as e:
        print(f"Error instantiating agent: {e}")
        return f"Error initializing agent: {e}", None

    # Expected answer format:
    # {"task_id": "task_id_1", "model_answer": "Answer 1 from your model", "reasoning_trace": "The different steps by which your model reached answer 1"}
    # {"task_id": "task_id_2", "model_answer": "Answer 2 from your model", "reasoning_trace": "The different steps by which your model reached answer 2"}
    answers_payload = []
    for entry in gaia_dataset['validation']:
        print(entry['task_id'])
        model_answer = agent(entry['Question'])
        answers_payload.append({'task_id': entry['task_id'],
                                'model_answer': model_answer})
        
    answers_json = json.dumps(answers_payload, indent=4)
    with open("answers_payload.json", "w") as outfile:
        outfile.write(answers_json)


if __name__ == '__main__':
    main()
