const chat = document.getElementById("chat");
const input = document.getElementById("input");

const SESSION_ID = localStorage.getItem("home_session")
  || crypto.randomUUID();

localStorage.setItem("home_session", SESSION_ID);

function addMessage(text, cls) {
  const div = document.createElement("div");
  div.className = `msg ${cls}`;
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

async function send() {
  const question = input.value.trim();
  if (!question) return;

  input.value = "";
  addMessage("You: " + question, "user");

  const aiDiv = addMessage("HOME: ", "ai");

  const response = await fetch("http://127.0.0.1:8000/ask_stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question,
      session_id: SESSION_ID
    })
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    const events = buffer.split("\n\n");
    buffer = events.pop();

    for (const event of events) {
      if (event.startsWith("data: ")) {
        const data = event.replace("data: ", "");
        if (data === "[DONE]") return;
        aiDiv.textContent += data;
      }
    }
  }
}
