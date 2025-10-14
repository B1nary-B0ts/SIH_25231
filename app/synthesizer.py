# app/synthesizer.py
from typing import List, Dict
import subprocess
import shlex
import os

# def build_prompt(query: str, retrieved: List[Dict]) -> str:
#     ctx = []
#     for i, r in enumerate(retrieved, start=1):
#         payload = r.get("payload", {})
#         text = payload.get("text", "")
#         src = payload.get("filename", payload.get("doc_id", "unknown"))
#         ctx.append(f"[{i}] {text}\nSOURCE: {src}\n")
#     prompt = ("You are a helpful assistant. Use ONLY the provided context snippets and cite them by number. "
#               "If the answer is not contained in the snippets, reply 'I don't know.'\n\nContext:\n"
#               + "\n".join(ctx) + f"\nQuestion: {query}\n\nAnswer with citation numbers like [1].")
#     return prompt

def build_prompt(query: str, retrieved: List[Dict]) -> str:
    ctx = []
    for i, r in enumerate(retrieved, start=1):
        text = r.get("text", "")
        src = r.get("payload", {}).get("filename", r.get("id", "unknown"))
        ctx.append(f"[{i}] {text}\nSOURCE: {src}\n")
    prompt = (
        "You are a helpful assistant. Use ONLY the provided context snippets to answer the question. "
        "Cite your sources using numbers in brackets like [1], [2], etc. "
        "If the answer is not contained in the snippets, reply 'I don't know.'\n\nContext:\n"
        + "\n".join(ctx)
        + f"\nQuestion: {query}\n\nAnswer in full sentences and cite sources."
    )

    return prompt


#def generate_with_local_llm(prompt: str) -> str:
    """
    Placeholder for local LLM. Options to replace:
    - Call Ollama HTTP API if running locally
    - Call a local llama.cpp/ggml binary via subprocess (echo to input file / run)
    - Use text-generation-inference server HTTP
    For now: return a short summary placeholder.
    """
    # SAFETY: Do not call remote services by default. Replace below with an integration.
    return "LOCAL-LLM-PLACEHOLDER — replace generate_with_local_llm() with your LLM call."

import requests

def generate_with_local_llm(prompt: str) -> str:
    """
    Calls local Llama 3.2 3B model via Ollama HTTP API.
    """
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": prompt,
                "stream": False
            },
            timeout=90
        )
        response.raise_for_status()
        data = response.json()
        # Some Ollama versions return 'generations'
        if "response" in data:
            return data["response"].strip()
        elif "generations" in data and len(data["generations"]) > 0:
            return data["generations"][0].get("text", "").strip()
        else:
            return "LLM returned no text."
    except Exception as e:
        return f"LLM error: {e}"

# def synthesize(query: str, retrieved: List[Dict]) -> Dict:
#     prompt = build_prompt(query, retrieved)
#     answer = generate_with_local_llm(prompt)
#     citations = [r["id"] for r in retrieved]
#     return {"answer": answer, "citations": citations, "prompt": prompt}

def synthesize(query: str, retrieved: List[Dict]) -> Dict:
    prompt = build_prompt(query, retrieved)
    answer = generate_with_local_llm(prompt)

    citations = []
    for r in retrieved:
        payload = r.get("metadata") or r.get("payload", {})
        citations.append({
            "id": r["id"],
            "filename": payload.get("filename"),
            "page_range": payload.get("page_range"),
            "page_number": payload.get("page_number"),
            "line_range": payload.get("line_range"),
            "file_path": f"http://127.0.0.1:8000/storage/{payload.get('doc_id')}{os.path.splitext(payload.get('filename') or '')[1]}" 
            if payload.get("filename") and payload.get("doc_id") else None,
            "audio_start": payload.get("audio_start"),
            "audio_end": payload.get("audio_end")
        })

    return {
        "answer": answer,
        "citations": citations,
        "prompt": prompt
    }
