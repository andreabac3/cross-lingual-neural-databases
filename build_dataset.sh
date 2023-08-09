#!/usr/bin/env bash


# Cross-lingual WikiNLDB F and FQ
python3 google_translate_batch.py --exp_name cross-lingual-FQ --translate_query --list_file_to_translate train.jsonl dev.jsonl test.jsonl
python3 google_translate_batch.py --exp_name cross-lingual-F --list_file_to_translate train.jsonl dev.jsonl test.jsonl


# monolingual FQ WikiNLDB
python3 google_translate_batch.py --exp_name monolingual-FQ-French --translate_query --list_file_to_translate test.jsonl --language_list FR
python3 google_translate_batch.py --exp_name monolingual-FQ-Italian --translate_query --list_file_to_translate test.jsonl --language_list IT
python3 google_translate_batch.py --exp_name monolingual-FQ-Spanish --translate_query --list_file_to_translate test.jsonl --language_list ES
python3 google_translate_batch.py --exp_name monolingual-FQ-German --translate_query --list_file_to_translate test.jsonl --language_list DE
python3 google_translate_batch.py --exp_name monolingual-FQ-Chinese --translate_query --list_file_to_translate test.jsonl --language_list zh-cn


# monolingual F WikiNLDB
python3 google_translate_batch.py --exp_name monolingual-F-French --list_file_to_translate test.jsonl --language_list FR
python3 google_translate_batch.py --exp_name monolingual-F-Italian --list_file_to_translate test.jsonl --language_list IT
python3 google_translate_batch.py --exp_name monolingual-F-Spanish --list_file_to_translate test.jsonl --language_list ES
python3 google_translate_batch.py --exp_name monolingual-F-German --list_file_to_translate test.jsonl --language_list DE
python3 google_translate_batch.py --exp_name monolingual-F-Chinese --list_file_to_translate test.jsonl --language_list zh-cn


# Unseen languages FQ WikiNLDB
python3 google_translate_batch.py --exp_name monolingual-FQ-Korean --translate_query --list_file_to_translate test.jsonl --language_list KO
python3 google_translate_batch.py --exp_name monolingual-FQ-Catalan --translate_query --list_file_to_translate test.jsonl --language_list CA
python3 google_translate_batch.py --exp_name monolingual-FQ-Japanese --translate_query --list_file_to_translate test.jsonl --language_list JA
python3 google_translate_batch.py --exp_name monolingual-FQ-Yoruba --translate_query --list_file_to_translate test.jsonl --language_list YO
python3 google_translate_batch.py --exp_name monolingual-FQ-Tagalog --translate_query --list_file_to_translate test.jsonl --language_list TL




