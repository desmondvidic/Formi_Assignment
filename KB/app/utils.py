from tqdm import tqdm
from transformers import GPT2TokenizerFast

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

def chunk_text(text, max_tokens=700, overlap=50):
    tokens = tokenizer.encode(text)
    chunks = []
    length = len(tokens)
    start = 0
    start_prev = -1  # To keep track of previous start

    estimated_chunks = max(1, (length + max_tokens - 1) // max_tokens)

    with tqdm(total=estimated_chunks, desc="Chunking text", leave=False) as pbar:
        while start < length:
            end = min(start + max_tokens, length)
            chunk_tokens = tokens[start:end]
            chunk_text = tokenizer.decode(chunk_tokens, clean_up_tokenization_spaces=True)
            chunks.append(chunk_text)

            if start_prev == start:
                # no progress, break to avoid infinite loop
                break

            start_prev = start
            start = end - overlap

            # Make sure start moves forward at least by 1 token
            if start <= start_prev:
                start = start_prev + 1

            pbar.update(1)

    return chunks
