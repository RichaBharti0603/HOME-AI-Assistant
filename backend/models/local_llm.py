import subprocess
import json

def run_llm(prompt):
    cmd = [
        "llama.cpp/llama-cli",
        "-m", "models/phi3.gguf",
        "-p", prompt,
        "-n", "256"
    ]
    output = subprocess.check_output(cmd).decode()
    return output
