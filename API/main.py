from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
from transformers import GPT2TokenizerFast
import uvicorn

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify Retell's domain for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from rapidfuzz import fuzz
import re

def normalize(text):
    return re.sub(r'\s+', ' ', text.strip().lower()) if text else ""

def filter_kb_chunks(chunks, city, query, location=None, threshold=65):
    normalized_city = normalize(city)
    normalized_query = normalize(query)
    normalized_location = normalize(location)

    best_match = None
    highest_score = 0

    for item in chunks:
        city_text = normalize(item.get("city", ""))
        location_text = normalize(item.get("location", ""))
        chunk_text = normalize(item.get("chunk", ""))

        # Match city or allow partial matches
        city_score = fuzz.partial_ratio(normalized_city, city_text)
        if city_score < threshold and normalized_city not in city_text:
            continue

        # Match location loosely (can be in city or location field)
        if normalized_location:
            location_score = max(
                fuzz.partial_ratio(normalized_location, location_text),
                fuzz.partial_ratio(normalized_location, city_text)
            )
            if location_score < threshold:
                continue

        # Match query within chunk
        query_score = fuzz.token_set_ratio(normalized_query, chunk_text)

        if query_score > highest_score:
            best_match = item["chunk"]
            highest_score = query_score

    return best_match if best_match else None


from transformers import GPT2TokenizerFast
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

def count_tokens(text):
    return len(tokenizer.encode(text))# Load chunked KB
with open("kb_store2.json", "r") as f:
    KB_CHUNKS = json.load(f)

class KBResponse(BaseModel):
    answer: str
    tokens_used: int
    has_more: bool

@app.get("/kb/query", response_model=KBResponse)
def query_kb(city: str = Query(...), query: str = Query(...), location: Optional[str] = None):
    result = filter_kb_chunks(KB_CHUNKS, city=city, query=query, location=location)
    
    if result:
        tokens = count_tokens(result)
        if tokens <= 800:
            return {"answer": result, "tokens_used": tokens, "has_more": False}
        else:
            truncated = result[:3000]  # fallback truncation by character
            return {"answer": truncated, "tokens_used": count_tokens(truncated), "has_more": True}
    
    raise HTTPException(status_code=404, detail="No relevant information found.")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)