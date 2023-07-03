"""
Python voice assistant experiment using ChatGPT API
"""
import os
import sys
import shlex
import requests
import subprocess
from gtts import gTTS
import speech_recognition as sr

API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
API_KEY = None
HAS_CABINET = True

try:
    from cabinet import Cabinet
    cab = Cabinet()
    API_KEY = cab.get("keys", "openai")
    PARSE_ENABLED = cab.get("voicegpt", "parse_enabled")
except ImportError:
    HAS_CABINET = False
    key_file_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "OPENAI_KEY.md")
    if os.path.isfile(key_file_path):
        with open(key_file_path, "r", encoding="utf-8") as key_file:
            API_KEY = key_file.read().strip()

if API_KEY is None or API_KEY.startswith("Replace"):
    print("Failed to retrieve OpenAI API key. Please see the README.")
    sys.exit(-1)


def listen():
    """
    Listen to user input using the microphone.
    """
    recognizer = sr.Recognizer()
    file_dir = os.path.dirname(os.path.abspath(__file__))
    listen_path = os.path.join(file_dir, "audio/listen.mp3")
    error_path = os.path.join(file_dir, "audio/error.mp3")

    with sr.Microphone() as source:
        print("Listening...")
        subprocess.run(["play", listen_path, "tempo", "1.5"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            return query
        except sr.UnknownValueError:
            subprocess.run(["play", error_path, "tempo", "1.5"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            print("Sorry, I couldn't understand you.")
        except sr.RequestError:
            print("Sorry, there was an error with the speech recognition service.")
        return None


def speak(text):
    """
    Convert text to speech and play it.
    """
    tts = gTTS(text=text, lang='en')
    tts.save('output.mp3')
    subprocess.run(["play", "output.mp3", "tempo", "1.5"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)


def query_gpt(query, gpt_conversation=None):
    """
    Send the user query and conversation history to the OpenAI ChatGPT API and get a response.
    """

    if gpt_conversation is None:
        gpt_conversation = []
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    # Read system messages from the PERSONALITY.md file
    personality_file_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "PERSONALITY.md")

    if os.path.isfile(personality_file_path):
        with open(personality_file_path, "r", encoding="utf-8") as personality_file:
            system_messages = [
                line.strip() for line in personality_file.readlines() if line.strip()]
    else:
        # Default system messages
        system_messages = [
            "You are a helpful assistant named Victoria.",
            "You are not an AI, but a helpful friend.",
            "In all responses, you will respond as Victoria.",
            "You are designed to give very brief, thoughtful responses.",
            "You may have an edgy tone at times, but you always want what's best for me."
        ]

    # Construct messages list
    messages = [{"role": "system", "content": msg} for msg in system_messages]

    messages.extend(gpt_conversation)
    messages.append({"role": "user", "content": query})

    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
    }

    try:
        response = requests.post(
            API_ENDPOINT, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            messages = response.json()["choices"][0]["message"]["content"]
            return messages
        else:
            print("Sorry, there was an error with the API request.")
            print(response.json())
            speak("Hey, I ran into an error.")
            if HAS_CABINET:
                cab.log("VoiceGPT:", response.json(), level="error")
            return None
    except TimeoutError as error:
        speak("Hey, I'm not online. Let's talk later.")
        print(error)


conversation = []

def parse(input_string: str):
    """
    Parse the user input and perform specific actions if certain conditions are met.

    MODIFY THIS TO MATCH YOUR OWN NEEDS.
    
    Args:
        input_string (str): The user input to parse.

    Returns:
        bool: True if the conditions are met, False otherwise.
    """

    query = input_string.lower()
    if query in ['cancel', 'thank you']:
        sys.exit(0)

    if query.startswith("remind"):
        command = shlex.split(f"{query} --noconfirm")
        command_output = subprocess.run(command, capture_output=True, text=True, check=False)
        speak(command_output.stdout)
        return True

    return False


while True:
    user_input = listen()
    if user_input:
        print("User:", user_input)
        if PARSE_ENABLED and parse(user_input):
            continue
        output = query_gpt(user_input, conversation)
        if output:
            print(f"Assistant: {output}\n")
            speak(output)
            conversation.append({"role": "user", "content": user_input})
            conversation.append({"role": "assistant", "content": output})
