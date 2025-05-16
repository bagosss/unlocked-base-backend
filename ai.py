import base64
from fastapi import UploadFile
from typing import List
from openai import Client
from dotenv import load_dotenv

client = Client()

def encode_image_to_base64(
    image: UploadFile
):
    return base64.b64encode(image.file.read()).decode("utf-8")

def openai_chat(
    input_text: str,
    input_images: UploadFile
):
    chat_content = [
        {
            "type": "input_text",
            "text": input_text,
        }
    ]

    input_image_base64 = encode_image_to_base64(input_images)

    chat_content.append({
        "type": "input_image",
        "image_url": f"data:image/jpeg;base64,{input_image_base64}",
    })

    input_messages = [
        {
            "role": "user",
            "content": chat_content,
        }
    ]

    response = client.responses.create(
        model="gpt-4o-mini",
        input=input_messages
    )

    return response.output_text