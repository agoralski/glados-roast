import os
import psutil
import time
import mss
import cv2
import schedule
import base64
import yaml
import openai
import json
import argparse

import sounddevice as sd
import soundfile as sf

from PIL import Image
from pync import Notifier
from twilio.rest import Client
from glados import tts
from pathlib import Path
from datetime import datetime


def rescale_image(image, max_size):
    # Rescale the image to have the longest edge equal to max_size
    width, height = image.size
    if width > height:
        new_width = max_size
        new_height = int((max_size / width) * height)
    else:
        new_height = max_size
        new_width = int((max_size / height) * width)
    return image.resize((new_width, new_height), Image.LANCZOS)

# Function to take screenshots of all screens
def take_screenshots():
    with mss.mss() as sct:
        monitors = sct.monitors[1:]  # Get all monitors excluding the first (virtual monitor)
        screenshots = []
        for i, monitor in enumerate(monitors):
            filename = f'screenshot_{i}.png'
            sct_img = sct.grab(monitor)
            img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
            img = rescale_image(img, config_data['screenshot_rescale'])  
            img.save(filename)
            screenshots.append(filename)
        return screenshots

# Function to capture a photo from the webcam
def take_webcam_photo():
    cap = cv2.VideoCapture(0)
    time.sleep(2)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return None
    
    ret, frame = cap.read()
    if ret:
        filename = 'webcam_photo.png'
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = rescale_image(img, config_data['webcam_rescale']) 
        img.save(filename)
        cap.release()
        return filename
    else:
        print("Error: Could not read frame from webcam.")
        cap.release()
        return None

# Function to encode image to base64
def encode_image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_image

# Function to translate text to audio and save it as a wav file
def text_to_audio(text):
    now = datetime.now()
    audio = _tts.generate_speech_audio(text)

    if config_data['save_generated_audio']:
        date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
        audio_filename = f"{date_time}-glados-response.wav"
        sf.write(audio_filename, audio, tts.RATE)

    print(f"GLaDOS text: {text}")
    sd.play(audio, tts.RATE)
    sd.wait()  # Wait until the audio is finished playing
    return 

# Function to send images to OpenAI API with user-defined prompt
def send_images_to_openai(image_paths, system_prompt, user_prompt, model):
    try:
        contents = [
            {
                "type": "text",
                "text": user_prompt
            }
        ]

        for image_path in image_paths:
            base64_image = encode_image_to_base64(image_path)
            contents.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_image}",
                    "detail": "low"
                }
            })

        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": contents
                },
            ]
        }

        response = openai.ChatCompletion.create(model=model, messages=payload["messages"])
        response_text = response["choices"][0]["message"]["content"]
        response_json = json.loads(response_text)
        
        status = response_json.get('status')
        analysis = response_json.get('analysis')
        print(f"GPT-4o: classification: {status}, analysis: {analysis}")
        return {'status': status, 'analysis': analysis}
    
    except openai.error.InvalidRequestError as e:
        print(f"OpenAI API request failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def roast_user(status, analysis, roast_prompt):
    try:
        if status != 'meeting' and (status == 'distracted' or status == 'absent' or status == 'smartphone'):
            voice_payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": roast_prompt
                    },
                    {
                        "role": "user",
                        "content": analysis
                    },
                ]
            }

            voice_response = openai.ChatCompletion.create(model=model, messages=voice_payload["messages"])
            response_text = voice_response["choices"][0]["message"]["content"]

            Notifier.notify(response_text, title="GLaDOS Alert")
            text_to_audio(response_text)

        if status == 'smartphone' and config_data['twilio_enabled']:
            client = Client(config_data['twilio_account_sid'], config_data['twilio_auth_token'])

            twilio_message = client.messages.create(
                from_   = config_data['twilio_source_number'],
                to      = config_data['twilio_dest_number'],
                body    = response_text
            )

    except openai.error.InvalidRequestError as e:
        print(f"OpenAI API request failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Schedule the tasks to run every 1 minute (adjust back to 5 minutes if needed)
def job():
    screenshots = take_screenshots()
    webcam_photo = take_webcam_photo()
    
    if webcam_photo:
        screenshots.append(webcam_photo)
    
    # Step 1: Send screenshots and webcam to OpenAI for evaluation
    result = send_images_to_openai(screenshots, system_prompt, user_prompt, model)
    
    # Step 2: Roast the user if distracted using voice
    roast_user(result['status'], result['analysis'], core_data['system_prompt'].format(ram = system_memory))

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description="Check for --personality-core parameter.")

# Add the --personality_core argument with a default value
parser.add_argument('--personality-core', type=str, default='glados', help='Set the personality core value.')

# Parse the command-line arguments
args = parser.parse_args()

# Get the value of the --personality_core parameter
personality_core = args.personality_core

# Load main config
roast_config_path = os.path.join('config', 'config.yaml')
with open(roast_config_path, "r") as file:
    config_data = yaml.safe_load(file)

# Load personality core config
core_config_path = os.path.join('cores', f"{personality_core}.yaml")
with open(core_config_path, "r") as file:
    core_data = yaml.safe_load(file)

system_prompt   = config_data['roast_system_prompt'].format(user_role = config_data['roast_user_role'])
user_prompt     = config_data['roast_user_prompt']
model           = config_data['openai_model']

# Set up OpenAI API key
openai.api_key = config_data['openai_api_key']

# Voice object
_tts = tts.Synthesizer(model_path=os.path.join(Path.cwd(), "models", core_data['voice_model']), use_cuda=False)

# Schedule the job
schedule.every(config_data['roast_interval']).seconds.do(job)

# Print initial info
system_memory = str(round(psutil.virtual_memory().total / (1024.0 **3)))+" gigabytes"
print(f"GLaDOS Roast started. RAM: {system_memory}. Press Ctrl+C to stop.")

if core_data['announcement']:
    text_to_audio(core_data['announcement'].format(ram = system_memory))

# Run the scheduled tasks
while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except Exception as e:
        print(f"An error occurred during scheduled task execution: {e}")
