from faster_whisper import WhisperModel
import os


def transcribe_audio(audio_path):
    # Initialize the Whisper model
    model_size = "base" 
    print(f"Loading Whisper model: {model_size}...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    print("Model loaded. Transcribing...")

    # faster-whisper can directly process .wav files.
    segments, info = model.transcribe(audio_path, beam_size=5)

    transcript = ""
    print(f"Detected language: {info.language} with probability {info.language_probability}")
    for segment in segments:
        transcript += segment.text.strip() + " "

    return transcript.strip()

def main():
    output_transcript_file = "transcript.txt"
    audio_to_transcribe = "sample.wav"
    if not os.path.exists(audio_to_transcribe):
        print(f"Error: {audio_to_transcribe} not found. Please ensure 'sample.wav' is in the same directory.")
        return
    print(f"Using provided audio file: {audio_to_transcribe}")

    # Perform transcription
    transcribed_text = transcribe_audio(audio_to_transcribe)
    print("\n--- Transcription Result ---")
    print(transcribed_text)

    # Save to transcript.txt
    with open(output_transcript_file, "w", encoding="utf-8") as f:
        f.write(transcribed_text)
    print(f"\nTranscription saved to {output_transcript_file}")


if __name__ == "__main__":
    main()