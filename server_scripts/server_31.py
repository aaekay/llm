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
    model="/home/aaekay/llm/3.1_8Bf/",
    model_kwargs={"torch_dtype": torch.bfloat16},
    device="cuda",
    )
app = FastAPI()
class Args:
 # Set your default or dynamic prompt
    tokens = 250  # Adjust based on your needs

args = Args()

# The function used to generate outputs (client function logic)
def client(impression):
    try:
        # Dynamically execute based on the prompt
        messages = impression
        
        # Tokenize and apply chat template
        prompt = pipeline.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        # Define terminators for output generation
        terminators = [
            pipeline.tokenizer.eos_token_id,
            pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]

        # Generate output using the pipeline
        outputs = pipeline(
            prompt,
            max_new_tokens=args.tokens,
            eos_token_id=terminators,
            do_sample=True,
            temperature=0.1,
            top_p=0.9,
        )

        # Return the generated text excluding the prompt
        return outputs[0]["generated_text"][len(prompt):]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

try:
    print(client([
        {"role": "system", "content": "You are an AI assistant whose role is to listen to the user"},
        {"role": "user", "content": "Write a poem in 50 words about star" },
    ]))
except:
    print("model load failed")
class ImpressionRequest(BaseModel):
    impression: List

# Define the FastAPI endpoint
@app.post("/generate/")
async def generate_text(impression_req: ImpressionRequest):
    """
    Endpoint to generate text based on an impression.
    The impression is passed in the request body.
    """
    try:
        # Call the client function with the impression
        generated_text = client(impression_req.impression)
        return {"generated_text": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing impression: {str(e)}")