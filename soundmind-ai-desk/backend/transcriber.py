import whisper

model = whisper.load_model("base")

def transcribe_audio(audio_file):
    audio_path = "/tmp/audio.wav"
    audio_file.save(audio_path)
    result = model.transcribe(audio_path)
    return result["text"]
