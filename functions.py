import json
import os
from openai import OpenAI
from prompts import assistant_instructions

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

client = OpenAI(api_key=OPENAI_API_KEY)


# Create or load assistant
def create_assistant(client):
    assistant_file_path = 'assistant.json'

    # If there is an assistant.json file already, then load that assistant
    if os.path.exists(assistant_file_path):
        with open(assistant_file_path, 'rb') as file:
            assistant_data = json.load(file)
            assistant_id = assistant_data['assistant_id']
            print("Loaded existing assistant ID.")
    else:
        try:
            file_paths = ["knowledge.docx", "knowledge3.pdf","ISO168902016.docx"]
            # Create files and retrieve their IDs
            file_ids = []
            for file_path in file_paths:
                file = client.files.create(file=open(file_path, "rb"), purpose='assistants')
                file_ids.append(file.id)

            assistant = client.beta.assistants.create(
                # Getting assistant prompt from "prompts.py" file, edit on left panel if you want to change the prompt
                instructions=assistant_instructions,
                model="gpt-3.5-turbo-1106",
                # This adds the knowledge base as a tool
                tools=[{"type": "retrieval", "file_ids": file_ids}])

            # Create a new assistant.json file to load on future runs
            with open(assistant_file_path, 'w') as file:
                json.dump({'assistant_id': assistant.id}, file)
                print("Created a new assistant and saved the ID.")

            assistant_id = assistant.id
        except Exception as e:
            print(f"Error creating assistant: {e}")
            raise
    return assistant_id
