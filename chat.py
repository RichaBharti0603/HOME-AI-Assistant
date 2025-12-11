# chat.py
import requests
import json

API_URL = "http://127.0.0.1:8000/ask"
USER_ID = "user_1"  # Change this for different users

def ask_question(question, top_k=3, stream=False):
    payload = {
        "question": question,
        "user_id": USER_ID,
        "top_k": top_k,
        "stream": stream
    }
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("answer", "No answer received.")
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def main():
    print("Welcome to Home AI Assistant!")
    print("Type 'exit' to quit.\n")
    
    while True:
        question = input("You: ")
        if question.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        answer = ask_question(question)
        print(f"Home: {answer}\n")

if __name__ == "__main__":
    main()
