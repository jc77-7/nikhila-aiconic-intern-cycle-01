## Project Overview
The AI Daily Activity Organizer is a Python-based application that leverages speech-to-text and large language models (LLMs) to automatically transcribe spoken daily activities and categorize them into predefined types. This allows for effortless logging and organization of your daily routine without the need for manual typing.

## Features
- Speech Transcription: Converts audio input (e.g., a .wav file) into text using the efficient faster-whisper library.

- LLM-Powered Categorization: Utilizes a local Large Language Model (LLM) via Ollama and LangChain to intelligently parse the transcribed text and assign each identified activity to a specific category.

- Predefined Categories: Tasks are categorized into: "Study", "Meals", "Play", "Chores", "Hygiene", "Exercise", and "Other".

- Structured Output: Generates a JSON file containing the categorized tasks, making it easy to integrate with other systems or for further analysis.

- Privacy-Focused: Designed to work with local LLMs, ensuring your data remains on your machine.

## Prerequisites
Before you begin, ensure you have the following installed:
 - Python 3.8+: Download Python
 - Ollama: A platform to run large language models locally.
 - After installation, download the mistral/ tinyllama model (or your preferred LLM):
 - ollama run mistral
 - sample.wav file: An audio file containing spoken activities to be transcribed and categorized. Place this file in the root directory of the project.