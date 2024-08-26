import os
import json

def secondone():
    directory_path = "C:/python/test"

    all_data = []

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if filename.endswith('.json'):
            with open(file_path, encoding='utf-8') as file:
                data = json.load(file)
                all_data.extend(data)

    output_file_path = "C:/python/test/combined_data.json"

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(all_data, output_file)

secondone()
