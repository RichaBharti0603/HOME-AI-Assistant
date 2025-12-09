# backend/models/local_llm.py
import subprocess

def run_llm(prompt: str) -> str:
    """
    Run the Ollama LLM locally using subprocess.
    Returns the LLM output as plain text.
    """
    try:
        cmd = ["ollama", "run", "llama3.2", prompt]
        # text=True ensures output is string (Python 3.7+)
        output = subprocess.check_output(cmd, text=True)
        return output.strip()
    except subprocess.CalledProcessError as e:
        return f"Error running LLM: {e}"
    except FileNotFoundError:
        return "Ollama CLI not found. Make sure Ollama is installed and in your PATH."
