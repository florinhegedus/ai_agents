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
