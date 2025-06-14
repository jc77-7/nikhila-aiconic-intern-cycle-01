import os
import json
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_ollama import OllamaLLM
from langchain_core.runnables import Runnable

# Load env vars
load_dotenv()
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

# Initialize local LLM via Ollama
llm = OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)


# Read transcript
with open("transcript.txt", "r", encoding="utf-8") as f:
    user_text = f.read()

# Prompt template for categorization
prompt = PromptTemplate(
    input_variables=["text"],
    template="""
You are a helpful assistant. The user will give you a sentence describing multiple personal activities. 

Your task is:
1. Identify each activity as a separate task.
2. Assign each one a category from this list (exactly as written): 
["Study", "Meals", "Play", "Chores", "Hygiene", "Exercise", "Other"]

Example input: 
"I want to finish my homework, cook lunch, play soccer, and brush my teeth."

Expected JSON output:
[
  {{ "task": "finish my homework", "category": "Study" }},
  {{ "task": "cook lunch", "category": "Meals" }},
  {{ "task": "play soccer", "category": "Play" }},
  {{ "task": "brush my teeth", "category": "Hygiene" }}
]

Now process this input:
{text}

Respond **only** with the JSON array. Do not explain anything.
"""
)


# Combine prompt and model
chain: Runnable = prompt | llm

# Run categorization
response = chain.invoke({"text": user_text})

# Print and optionally save
print("\n--- Categorized Output ---")
print(response)

with open("categorized_tasks.json", "w", encoding="utf-8") as f:
    f.write(response)
