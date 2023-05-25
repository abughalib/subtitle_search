import os
import subtitle_search.settings as setting
from django.core.files.uploadedfile import UploadedFile
from . import dynamo
from typing import *
from pathlib import Path
from . import amazons3
import meilisearch
import json
import random

AWS_BUCKET_NAME = 'subtitle-search'
MEILISEARCH_URL = 'http://localhost:7700'

def generate_random_word():
    # Generate a random string of letters and numbers
    return ''.join([chr(random.randint(65, 90)) for _ in range(10)])[1:]


def write_file(file: UploadedFile) -> (str, str, Path):
    # Create media folder if not exists
    if not os.path.exists("media"):
        try:
            os.mkdir("media")
        except OSError:
            print("Creation of the directory failed")
            return {"error": "Creation of the directory failed"}
    file_extension = file.name.split('.')[-1]
    file_name = f"{generate_random_word()}"
    file_location = setting.MEDIA_DIR
    with open(file_location / (f'{file_name}.{file_extension}'), "wb+") as file_obj:
        for chunk in file.chunks():
            file_obj.write(chunk)

    return file_name, file_extension, file_location


def extract_subtitle(file_location: Path, file_name: str, file_extension: str):
    subtitle_path = setting.MEDIA_DIR.joinpath(file_name + '.srt')
    # For windows
    if os.name == 'nt':
        cc_extractor_path = 'C:\\"Program Files (x86)"\\CCExtractor\\ccextractorwinfull.exe'
        os.system(f'{cc_extractor_path} {file_location}/{file_name}.{file_extension} -o {subtitle_path}')
    else:
        os.system(f'/home/ubuntu/ccextractor/linux/ccextractor {file_location}/{file_name}.{file_extension} -o {subtitle_path}')

    return subtitle_path


def convert_to_json(file_location: Path, folder_location) -> Path:
    # Read the file
    with open(file_location, 'r') as f:
        text = f.read()

    # Split the text by empty lines
    text = text.split('\n\n')

    # Create a list of dictionaries
    data = []
    for item in text:
        item = item.split('\n')
        if len(item) < 3:
            continue
        # Convert this list of string to string

        try:
            data.append({
                'id': item[0],
                'time': item[1],
                'text': ' '.join([s.strip() for s in item[2:]])
            })
        except IndexError:
            print('IndexError at: ', item)

    # Write the json file
    with open(folder_location / 'subs.json', 'w') as f:
        json.dump(data, f, indent=2)

    return folder_location.joinpath('subs.json')


def upload_video(file):
    # Save the file first
    file_name, file_extension, file_location = write_file(file)
    subtitle_location = extract_subtitle(file_location, file_name, file_extension)
    subtitle_json = convert_to_json(subtitle_location, file_location)
    upload_subtitle(subtitle_json)
    # Upload file to S3
    # amazons3.upload_file(file_location / (file_name + file_extension), AWS_BUCKET_NAME)
    return subtitle_location


def upload_subtitle(subtitle_json_location: Path):
    # Remove the previous index
    remove_index()
    # Save subtitle to DynamoDB
    # dynamo.save_subtitle(subtitle_json_location)
    # Upload it to meilisearch
    client = meilisearch.Client(MEILISEARCH_URL)
    json_file = open(subtitle_json_location, encoding='utf-8')
    subtitles = json.load(json_file)
    try:
        client.index('subtitles').add_documents(subtitles)
    except meilisearch.errors.MeilisearchApiError:
        print('Error uploading to meilisearch')

def search_text(phrase: str) -> dict[str, Any]:
    client = meilisearch.Client(MEILISEARCH_URL)
    try:
        res = client.index('subtitles').search(phrase)
    except meilisearch.errors.MeilisearchApiError:
        print('Error searching in meilisearch')
        return {}
    return res

def remove_index():
    client = meilisearch.Client(MEILISEARCH_URL)
    client.index('subtitles').delete()