import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI

from utils import (get_gpt_response, get_transcription,
                   transcripts_and_summaries_log)

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file!")

client = OpenAI(api_key=API_KEY)
parser = argparse.ArgumentParser()
parser.add_argument("--mode", type=str)
args = parser.parse_args()

def main():

    model_name = 'gpt-4o'

    dict_gpt_task = {
        "summary": "Write a short summary (1-2 sentences) of the following transcript",
        "extract_keywords": "Extract relevant five keywords or key phrases from the following transcript. Separate them with commas",
        "generate_title": "Generate a concise and informative title that contains the main idea of the following transcript"
    }

    mode = args.mode

    if mode is None:
        mode = "summary"

    if mode not in dict_gpt_task.keys() and mode != "custom":
        raise ValueError(f"Not correct --mode task: {mode}")
    
    if mode != "custom":
        instructions = dict_gpt_task[mode]

    while True:

        user_input = input("You uploaded: ")

        if user_input.lower() in ["quit", "exit"]:
                    print("Goodbye!")
                    break  

        audio_paths = [audio_path.strip() for audio_path in user_input.split(";")]

        for audio_path in audio_paths:

            if not audio_path:
                continue

            if not os.path.exists(audio_path):
                        print(f"\nFile doesn't exist {audio_path}")
                        continue
            
            print(f"\nFile: {audio_path}")

            transcription_input = get_transcription(client, audio_path)
            print(f"-> Transcript: {transcription_input}")

            if mode == "custom":
                while True:
                    new_prompt = input("Enter prompt for GPT (write 'default' for return default prompt): ")
                                
                    instructions = dict_gpt_task["summary"] if new_prompt == "default" else new_prompt

                    summary = get_gpt_response(client, model_name, instructions, transcription_input)

                    print(f"\n-> GPT Summary: {summary}", end="\n\n")

                    transcripts_and_summaries_log(mode, instructions, transcription_input, summary)

                    again = input("\nTry another summarization prompts? (yes/not): ")

                    if again != "yes":
                        break
            else:
                summary = get_gpt_response(client, model_name, instructions, transcription_input)
                 
                print(f"\n-> GPT Summary: {summary}", end="\n\n")

                transcripts_and_summaries_log(mode, instructions, transcription_input, summary)
                 

if __name__ == "__main__":
    main()
