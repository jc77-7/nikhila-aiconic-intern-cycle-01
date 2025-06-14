import os
import json
from dotenv import load_dotenv
from faster_whisper import WhisperModel
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM 

# === Load environment variables ===
load_dotenv()
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
AUDIO_FILE = "sample.wav"
OUTPUT_FILE = "output.json"

# === 1. Transcribe Audio ===
def transcribe_audio(audio_path):
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_path, beam_size=5)
    transcript = " ".join([seg.text.strip() for seg in segments])
    return transcript.strip()

# === 2. Categorize Tasks with Ollama ===
def categorize_tasks(text):
    llm = OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)

    prompt = PromptTemplate(
        input_variables=["text"],
        template="""
You are a helpful assistant. The user gives you a sentence describing personal activities.

Split the sentence into individual tasks. Then assign each task a category from:
["Study", "Meals", "Play", "Chores", "Hygiene", "Exercise", "Other"]

Example input:
"I want to finish my homework, cook lunch, play soccer, and brush my teeth."

Expected output (JSON only):
[
  {{ "task": "finish my homework", "category": "Study" }},
  {{ "task": "cook lunch", "category": "Meals" }},
  {{ "task": "play soccer", "category": "Play" }},
  {{ "task": "brush my teeth", "category": "Hygiene" }}
]

Now process this:
{text}

Respond only with the JSON array. Do not explain anything.
"""
    )

    chain = prompt | llm
    result = chain.invoke({"text": text})

    try:
        parsed = json.loads(result)
    except json.JSONDecodeError:
        print("⚠️ Error: LLM did not return valid JSON.")
        parsed = []

    return parsed

# === 3. Main ===
def main():
    if not os.path.exists(AUDIO_FILE):
        print(f"❌ Audio file '{AUDIO_FILE}' not found.")
        return

    print("🎙️ Transcribing audio...")
    transcript = transcribe_audio(AUDIO_FILE)
    print("📝 Transcript:", transcript)

    print("\n🤖 Categorizing tasks...")
    categorized = categorize_tasks(transcript)

    print("\n📤 Final JSON Output:")
    print(json.dumps(categorized, indent=2))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(categorized, f, indent=2)

    print(f"\n✅ Output saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
