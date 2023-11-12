import os
from dotenv import load_dotenv

from openai import OpenAI

client = OpenAI()

# Load environment variables
load_dotenv()

# Set API key
OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4-1106-preview",
  messages=[
    {"role": "system", "content": "generate JSON response"},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ], 
  response_format = {"type": "json_object"}
)


message = response.choices[0].message.content

print(message)

response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages = [
        {
            "role" : "user",
            "content" :
            [
                {"type" : "text", "text" : "What's in this image?"},
                {
                    "type" : "image_url",
                    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
                }
            ]
        }
    ],
    max_tokens = 300
)

print(response.choices[0].message.content)
description = response.choices[0].message.content

response = client.images.generate(
    model= "dall-e-3",
    prompt= description,
    size="1024x1024",
    quality="standard",
    n=1
)
image_url = response.data[0].url
print(image_url)


speech_file_path = "speech.mp3"
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=description
)
response.stream_to_file(speech_file_path)

speech_file_path = "speech.mp3"
audio_file= open(speech_file_path, "rb")
transcript = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)

print(transcript)