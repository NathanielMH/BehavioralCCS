import json
from tqdm import tqdm
import requests

def load_data(dataset_name):
    url = f"https://huggingface.co/datasets/Anthropic/model-written-evals/raw/main/sycophancy/{dataset_name}.jsonl"
    r = requests.get(url).text
    data = [json.loads(l) for l in r.split("\n") if l != '']
    return data

def main():
    ...

if __name__ == "__main__":
    main()