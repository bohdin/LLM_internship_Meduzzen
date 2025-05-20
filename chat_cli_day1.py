from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    print("ERROR: API nor found")
else:
    print("CORRECT: API found")