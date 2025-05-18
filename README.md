# 📚 Knowledge Base API with DOCX Chunking and Retell.ai Integration

This project extracts structured content from `.docx` files, chunks it based on token count, serves it via a FastAPI backend, and integrates it with [Retell.ai](https://www.retellai.com) using a custom webhook.

---

## 🔧 Features

- ✅ Extract text from `.docx` files
- 🧩 Chunk text using token-aware logic (e.g., 800 token limit with overlap)
- 🚀 Serve the knowledge base via FastAPI endpoint `/kb/query`
- 🔍 Robust fuzzy search using `fuzzywuzzy` for accurate matching
- 🌐 Integration with Retell.ai using a custom webhook
- 📝 Preprocessing includes filtering out invalid or empty chunks
- 🗂 Supports flexible KB queries based on city, location, and query intent

---

## Working
![Working](https://github.com/user-attachments/assets/165844f5-4d1c-44a4-99e0-8eba4fd99732)


# Knowledge Base to Retell Webhook Integration

## 1. Extracting Chunks from DOCX

The DOCX file contains structured and semi-structured information such as daily schedules, menus, and other general instructions. To integrate this with an AI-driven assistant, we first parse the DOCX content into manageable 'chunks' of text. Each chunk is restricted to a token limit (e.g., 800 tokens) to be suitable for prompt input. Overlap between chunks ensures continuity.

**Key Steps:**

* Read DOCX content
* Tokenize using an efficient tokenizer (e.g., from Hugging Face)
* Create overlapping chunks
* Save as a JSON for quick access

## 2. JSON Knowledge Base

The extracted chunks are stored in a JSON file (`kb_store.json`). Each item contains:

* `city`
* `location`
* `category`
* `chunk`

This allows fast lookup and filtering based on API requests.

## 3. Query Endpoint with FastAPI

A FastAPI server is created to serve queries to the knowledge base. The `/kb/query` endpoint accepts parameters like:

* `city`
* `query`
* `location` (optional)

It searches for the best matching chunk using both exact and fuzzy string matching to handle variations in input.

## 4. Fuzzy Matching for Robust Queries

To enhance query reliability, fuzzy string matching (e.g., using `fuzzywuzzy`) is used to compare user input with the knowledge base content. This improves handling of typos and variations in phrasing.

## 5. Webhook Integration with Retell.ai

Retell.ai supports integration with external knowledge bases through webhooks.

**Setup involves:**

* Hosting the FastAPI service (e.g., on Render or Replit)
* Creating a public URL
* Pointing Retell webhook configuration to `/kb/query`

When the assistant needs to fetch knowledge, it triggers the webhook with parameters like city, location, and question. The FastAPI responds with a relevant chunk from the JSON knowledge base.

## 6. Deployment

To deploy the FastAPI server:

* Use Render with the start command: `uvicorn retell_webhook:app --host 0.0.0.0 --port $PORT`
* Or run locally using: `uvicorn retell_webhook:app --host 0.0.0.0 --port 8000`

Ensure the API is publicly accessible so that Retell can reach it.

---


## ⚙️ Setup Instructions

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/your-repo/kb-retell-integration.git
cd kb-retell-integration
pip install -r requirements.txt
```

2. Extract & Chunk DOCX

Modify and run the script:

Always show details

python extract_and_chunk.py

This script will:

    Load .docx files

    Chunk text by token count

    Save the chunks into kb_store.json

3. Run FastAPI Server

Always show details

uvicorn app.main:app --reload

API Endpoint: http://localhost:8000/kb/query?city=Delhi&query=menu
4. Test on Postman

    Method: GET

    URL: http://localhost:8000/kb/query

    Query Params:

        city: Your city (e.g., Bangalore)

        location: (Optional)

        query: Your query (e.g., menu)

🔗 Retell.ai Webhook Integration
Step-by-Step

    Go to Retell.ai Console

    Set up a Custom Webhook under Integrations

    Point the webhook to your FastAPI endpoint (/webhook from retell_webhook.py)

    Ensure Render/Replit exposes public URL (use 0.0.0.0 and correct port)

Always show details

uvicorn app.retell_webhook:app --host 0.0.0.0 --port 10000

🔍 Sample Query Response

Always show details

{
  "answer": "Menu: Veg Starter - Paneer Tikka, Non-Veg - Chicken Tangdi...",
  "tokens_used": 376,
  "has_more": false
}

✅ Improvements

    Fuzzy matching for resilient query recognition

    Handles structured day-wise data, menus, addresses

    Eliminates invalid _Barbeque Nation suffixes in data

    Ensures fallback if over-token limit (>800 tokens)

🛠 Requirements

    Python 3.8+

    fastapi, uvicorn, fuzzywuzzy, transformers, python-docx, tqdm, pydantic
