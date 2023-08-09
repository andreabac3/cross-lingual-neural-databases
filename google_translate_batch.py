#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
from collections import defaultdict
from dataclasses import dataclass
from time import sleep


import numpy as np
from tqdm import tqdm
from googletrans import Translator


from utilities.circular_list import CircularList
from utilities.utilities import *


@dataclass
class DatasetRepresentation:
    sentence: str
    line_idx: int
    sentence_id: int

    def __str__(self):
        return self.sentence


def make_batch(bucket, desired_batch_size):
    batch_size: float = len(bucket) / (desired_batch_size - 1)
    batch = np.array_split(bucket, batch_size)
    return batch


def batch_translation(translation_api: Translator, lang: str, batch: List[DatasetRepresentation]) -> List[str]:
    preprocessed_batch = [b.sentence for b in batch if len(b.sentence) > 0]
    translations = [None] * len(preprocessed_batch)

    while None in translations:
        for idx, sent in enumerate(preprocessed_batch):

            # Skip successfully translated sentences
            if translations[idx] is not None:
                continue
            try:
                sleep(0.3)
                translation = translation_api.translate(sent, src="en", dest=lang)
                translations[idx] = translation.text
            except KeyboardInterrupt:
                print("Keyboard Interrupt = CTRL+C")
                exit(-1)
            except Exception as e:
                sleep(3)
                print(e, lang)
                continue
    return translations



def translate_wikinldb(exp_name: str, LANGUAGE_LIST, translate_query: bool, batch_size: int, file_list_to_translate: List[str]):
    translation_api: Translator = Translator()
    dataset_folder_path = "WikiNLDB/v2.4_25/"
    obtain_dataset(dataset_folder_path)
    cl: CircularList = CircularList(LANGUAGE_LIST)
    cl_query: CircularList = CircularList(LANGUAGE_LIST)
    for dataset_filename in file_list_to_translate:
        buckets_fact: Dict[str, List[DatasetRepresentation]] = defaultdict(list)
        buckets_query: Dict[str, List[DatasetRepresentation]] = defaultdict(list)
        dataset_filename_path = f"{dataset_folder_path}/{dataset_filename}"
        json_lines: List[dict] = read_jsonl(dataset_filename_path)

        # Bucket creation for query and facts
        for line_idx, line in tqdm(enumerate(json_lines), desc=f"{dataset_filename}", total=len(json_lines)):

            if translate_query:
                for query_id, query_list in enumerate(line["queries"]):
                    query = query_list["query"]
                    TARGET_LANG_QUERY = cl_query.get_next()

                    json_lines[query_id]["language"] = TARGET_LANG_QUERY
                    if TARGET_LANG_QUERY == "EN":
                        continue
                    buckets_query[TARGET_LANG_QUERY].append(DatasetRepresentation(query, line_idx, query_id))

            for fact_id, fact in enumerate(line["facts"]):
                TARGET_LANG = cl.get_next()
                if TARGET_LANG == "EN":
                    # we won't translate all the sentences.
                    # We will translate only the ones that are not assigned to the EN bucket
                    continue
                buckets_fact[TARGET_LANG].append(DatasetRepresentation(fact, line_idx, fact_id))

        # Query translation
        if translate_query:
            for lang, bucket in buckets_query.items():
                batches = make_batch(bucket, batch_size)
                for batch in tqdm(batches, desc=f"{dataset_filename} {lang} query"):
                    translations = batch_translation(translation_api, lang, batch)
                    for b, translation in zip(batch, translations):
                        json_lines[b.line_idx]["queries"][b.sentence_id]["query"] = translation

        # Fact translation
        for lang, bucket in buckets_fact.items():
            batches = make_batch(bucket, batch_size)
            for batch in tqdm(batches, desc=f"{dataset_filename} {lang} facts"):
                translations = batch_translation(translation_api, lang, batch)

                for b, translation in zip(batch, translations):
                    json_lines[b.line_idx]["facts"][b.sentence_id] = translation

        os.makedirs(f"out/{exp_name}/", exist_ok=True)
        write_jsonl(f"out/{exp_name}/{''.join(LANGUAGE_LIST)}_{dataset_filename}",
                    json_lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Batch Translation Script')
    parser.add_argument('--translate_query', action='store_true', help='Translate query')
    parser.add_argument('--batch_size', default=100, type=int, help='Choose a positive integer for batch size')
    parser.add_argument('--language_list', nargs='+', default=['DE', 'EN', 'ES', 'FR', 'IT', 'zh-cn'], help="Write a list of languages to translate to. Do not use square brackets. Example: --language_list DE EN ES FR IT zh-cn")
    parser.add_argument('--file_list_to_translate', nargs='+', default=["train.jsonl", "dev.jsonl", "test.jsonl"], help="Write a list of files to translate. Do not use square brackets. Example: --file_list_to_translate train.jsonl dev.jsonl test.jsonl")
    parser.add_argument('--exp_name', type=str, default="cross-lingual-FQ", help='Choose an exp name')

    args = parser.parse_args()

    translate_wikinldb(args.exp_name, args.language_list, translate_query=args.translate_query,
                       batch_size=args.batch_size, file_list_to_translate=args.file_list_to_translate)



