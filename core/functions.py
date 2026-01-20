import json, os
from openai import OpenAI
from config.paths import MEMORY_PATH, PROMPTS_PATH

def export_json(file_path, file_name, content):
    path = file_path / file_name

    with open(path, "w", encoding="utf-8") as file:
        json.dump(content, file, ensure_ascii=False, indent=4)

def read_json(file_path, file_name):
    path = file_path / file_name

    with open(path, "r", encoding="utf-8") as file:
        result = json.load(file)
    
    return result

def personal_info_to_text():
    memory_files = os.listdir(MEMORY_PATH)
    personal_content = {}

    for file in memory_files:
        file_name = file.split("json")[0]
        content = read_json(MEMORY_PATH, file)
        personal_content[file_name] = content

    personal_content = json.dumps(personal_content, ensure_ascii=False)

    return personal_content

def get_response_ia(input:str, prompt_name:str):
    openai_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_key)

    prompts = read_json(PROMPTS_PATH, "prompts.json")
    for prompt_item in prompts:
        if prompt_item["prompt_name"] == prompt_name:
            prompt = prompt_item["prompt"]
            break

    response = client.responses.create(
        input=input,
        prompt=prompt)
    
    return response