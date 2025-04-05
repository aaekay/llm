from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

import transformers
import torch
import time
import os
import logging
import argparse
from tqdm import tqdm

log = logging.getLogger()

logging.basicConfig(filename="server.log", encoding='utf-8', level=logging.DEBUG)

pipeline = transformers.pipeline(
    "text-generation",
    model="../models/gemma-2-27b-it/",
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
    )
app = FastAPI()


# The function used to generate outputs (client function logic)
def client(impression, token):
    try:
        # Dynamically execute based on the prompt
        messages = impression[1:]

        # Generate output using the pipeline
        outputs = pipeline(
            messages,
            max_new_tokens=token,
            do_sample=True,
            temperature=0.1,
            top_p=0.9,
        )

        # Return the generated text excluding the prompt
        return outputs[0]["generated_text"][-1]['content']
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

try:
    print(client([
        {"role": "system", "content": "you are a helpful AI assistant"},
        {"role": "user", "content": "Write a poem in 50 words about star" }, # gemma 2 only takes user role
    ], 250))
except Exception as e:
    print(e)
    print("test prompt failed")
class ImpressionRequest(BaseModel):
    impression: List
    token: int

# Define the FastAPI endpoint
@app.post("/generate/")
async def generate_text(impression_req: ImpressionRequest):
    """
    Endpoint to generate text based on an impression.
    The impression is passed in the request body.
    """
    try:
        # Call the client function with the impression
        generated_text = client(impression_req.impression, impression_req.token) # added so that it takes only the user role as input
        return {"generated_text": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing impression: {str(e)}")