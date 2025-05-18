# AI Agents Course
In this repository, I create a multi-agentic system to solve the Final Assignment of the AI Agents Course on Hugging Face and to submit responses for the GAIA dataset.

## GAIA Dataset
To download GAIA dataset:
```bash
pip install -U "huggingface_hub[cli]"
huggingface-cli login # you have to paste an access token
huggingface-cli download gaia-benchmark/GAIA --repo-type dataset 
```

Necessary libraries for loading the dataset:
```bash
pip install datasets 
```

## Final Assignment
Necessary libraries for querying the questions:
```bash
pip install requests
```