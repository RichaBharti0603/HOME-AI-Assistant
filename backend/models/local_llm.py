# backend/models/local_llm.py
import subprocess
import requests
import os
import json
import time

OLLAMA_API = os.getenv("OLLAMA_API", "http://localhost:11434")  # if using Ollama HTTP api
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

def run_llm(prompt: str) -> str:
    """
    Simple synchronous call — try HTTP API first; fallback to CLI.
    """
    # Try HTTP POST to Ollama /api/generate if available
    try:
        resp = requests.post(
            f"{OLLAMA_API}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "max_tokens": 256},
            timeout=30,
        )
        data = resp.json()
        # Ollama returns structure; extract response
        return data.get("response") or json.dumps(data)
    except Exception:
        # Fallback: call ollama CLI
        try:
            cmd = ["ollama", "run", OLLAMA_MODEL, prompt]
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
            return out.strip()
        except Exception as e:
            return f"Error running local LLM: {e}"

def run_llm_stream(prompt: str):
    """
    Generator that yields text chunks from the CLI streaming mode if available.
    If not available, returns single chunk at the end.
    """
    # Prefer CLI streaming (ollama run prints progressively)
    try:
        cmd = ["ollama", "run", OLLAMA_MODEL, prompt]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    except FileNotFoundError:
        # Ollama not installed: fallback to single response
        yield run_llm(prompt)
        return

    with proc.stdout:
        for line in iter(proc.stdout.readline, ""):
            if not line:
                continue
            yield line.encode("utf-8")
    proc.wait()
