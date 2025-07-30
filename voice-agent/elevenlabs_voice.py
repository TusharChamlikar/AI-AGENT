import requests

def generate_tts(text, voice="Bella"):
    headers = {"xi-api-key": "<ELEVENLABS_API_KEY>"}
    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice}",
        json={"text": text},
        headers=headers
    )
    with open("reminder.mp3", "wb") as f:
        f.write(response.content)
