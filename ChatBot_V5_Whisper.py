from flask import Flask, render_template, request
import requests
import os
import pyaudio
import wave
import speech_recognition as sr
import openai

OPENAI_API_KEY = "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"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

app = Flask(__name__)

def record_audio():
    # Set up PyAudio
    p = pyaudio.PyAudio()
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 5  # Adjust the recording time as needed

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    return b''.join(frames)

def translate_audio_to_text_with_whisper(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        whisper_response = openai.Audio.translate("whisper-1", audio_file, api_key=OPENAI_API_KEY)
        return whisper_response["text"]

@app.route('/', methods=['GET', 'POST'])
def chat():
    user_input = None

    if request.method == 'POST':
        if 'prompt' in request.form:
            user_input = request.form['prompt']
        elif 'record' in request.form:
            audio_data = record_audio()
            # Save the recorded audio to a WAV file (create the file if it doesn't exist)
            if not os.path.exists("user_input.wav"):
                with open("user_input.wav", "wb") as audio_file:
                    audio_file.write(audio_data)
            user_input = translate_audio_to_text_with_whisper("user_input.wav")

        if user_input:
            message = [{"role": "user", "content": user_input}]

            payload = {
                "model": "gpt-3.5-turbo",
                "messages": message,
                "temperature": 0,
                "top_p": 1.0,
                "n": 1,
                "stream": False,
                "presence_penalty": 0,
                "frequency_penalty": 0,
            }

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENAI_API_KEY}"
            }

            response = requests.post(OPENAI_API_URL, headers=headers, json=payload, stream=False)
            response_data = response.json()
            content = response_data['choices'][0]['message']['content']

            return render_template('index.html', user_input=user_input, response=content)

    return render_template('index.html', user_input=user_input, response=None)

if __name__ == '__main__':
    app.run(debug=True)
