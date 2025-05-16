from typing import List
from fastapi import FastAPI, UploadFile, Form, File
from fastapi.responses import JSONResponse
from openai import Client
from ai import openai_chat

client = Client()

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/task-verification")
async def verify_task(
    task: str = Form(...),
    description: str = Form(...),
    images: UploadFile = File(...)
):
    try:
        # Compose the prompt for the agent
        user_prompt = (
            f"You are a verification AI.\n\n"
            f"Task: {task}\n"
            f"Description: {description}\n\n"
            f"The user has submitted image(s) as evidence of completing the task.\n"
            f"Your job is to analyze the image(s) and determine whether they accurately reflect the task described.\n\n"
            f"Respond with 'Corresponding' if the image(s) align with the task and description, or 'Not Corresponding' if they do not.\n"
            f"Provide a brief explanation for your decision."
        )

        # Send message to the agent
        response = openai_chat(
            input_text=user_prompt,
            input_images=images
        )

        # Return structured response
        return JSONResponse({
            "result": response
        }, status_code=200)
    
    except Exception as e:
        import traceback

        traceback.print_exc()
        return JSONResponse({
            "error": str(e)
        }, status_code=500)