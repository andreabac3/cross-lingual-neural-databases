import os
from typing import *

import json


def obtain_dataset(dataset_folder_path: str):
    dataset_list = ["dev.jsonl", "test.jsonl", "train.jsonl"]
    list_of_dataset: List[str] = [filename for filename in os.listdir(dataset_folder_path) if filename in dataset_list]
    assert len(list_of_dataset) == 3, f"Missing some dataset {list_of_dataset}"


def read_json(filename: str) -> dict:
    with open(filename, "r") as file:
        return json.load(fp=file)


def write_json(filename: str, data: dict) -> None:
    with open(filename, "w") as file:
        json.dump(obj=data, fp=file, indent=2)


def write_jsonl(filename: str, data: List[dict]) -> None:
    with open(filename, "w") as file:
        for item in data:
            file.write(json.dumps(item) + "\n")


def read_jsonl(filename: str) -> List[dict]:
    with open(filename, "r") as file:
        return [json.loads(line) for line in file]
