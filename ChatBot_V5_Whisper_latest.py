from flask import Flask, render_template, request, redirect, url_for
import os
import pyaudio
import wave
import openai

app = Flask(__name__)

# Your OpenAI API key and URL
OPENAI_API_KEY = "open_AI_API_Key"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# Set your OpenAI API key here
openai.api_key = "open_AI_API_Key"

def record_audio(filename):
    p = pyaudio.PyAudio()
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 5

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    print("Recording...")

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

def translate_audio_to_text_with_whisper(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        whisper_response = openai.Audio.translate("whisper-1", audio_file, api_key=OPENAI_API_KEY)
        return whisper_response["text"]

@app.route('/', methods=['GET', 'POST'])
def chat():
    user_input = None
    response_content = None

    if request.method == 'POST':
        if 'prompt' in request.form:
            user_input = request.form['prompt']
        elif 'record' in request.form:
            record_audio("user_input.wav")
            user_input = translate_audio_to_text_with_whisper("user_input.wav")

        if user_input:
            response_content = get_openai_response(user_input)

    return render_template('index.html', user_input=user_input, response=response_content)

def get_openai_response(input_text):
    message = [{"role": "user", "content": input_text}]

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

    response = openai.ChatCompletion.create(**payload)
    return response.choices[0].message.content

if __name__ == '__main__':
    app.run(debug=True)
