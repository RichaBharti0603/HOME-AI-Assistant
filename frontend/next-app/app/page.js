"use client";

import { useState, useRef } from "react";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const controllerRef = useRef(null);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  const send = async (stream = false) => {
    if (!question.trim()) return;

    const q = question;
    setMessages((m) => [...m, { role: "user", text: q }]);
    setQuestion("");
    setLoading(true);

    if (!stream) {
      try {
        const res = await fetch(`${API_URL}/ask`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question: q }),
        });

        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

        const data = await res.json();
        setMessages((m) => [...m, { role: "assistant", text: data.answer }]);
      } catch (err) {
        setMessages((m) => [...m, { role: "assistant", text: "Error: " + err.message }]);
      } finally {
        setLoading(false);
      }
    } else {
      try {
        controllerRef.current = new AbortController();
        const res = await fetch(`${API_URL}/ask_stream`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question: q }),
          signal: controllerRef.current.signal,
        });

        if (!res.body) throw new Error("ReadableStream not supported by backend");

        let assistantText = "";
        setMessages((m) => [...m, { role: "assistant", text: "" }]);

        const reader = res.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
          const { value, done } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          assistantText += chunk;

          setMessages((m) => {
            const copy = [...m];
            const idx = copy.findIndex((x) => x.role === "assistant" && x.text === "");
            if (idx !== -1) {
              copy[idx] = { role: "assistant", text: assistantText };
            } else {
              copy[copy.length - 1] = { role: "assistant", text: assistantText };
            }
            return copy;
          });
        }
      } catch (err) {
        setMessages((m) => [...m, { role: "assistant", text: "Error: " + err.message }]);
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div style={{ maxWidth: 800, margin: "2rem auto", fontFamily: "sans-serif" }}>
      <h1>HOME — Local AI Assistant</h1>

      <div style={{ marginBottom: 16 }}>
        {messages.map((m, idx) => (
          <div key={idx} style={{ padding: 8, marginBottom: 6, background: m.role === "user" ? "#cce6ff" : "#eeeeee" }}>
            <strong>{m.role === "user" ? "You" : "Home"}</strong>
            <div>{m.text}</div>
          </div>
        ))}
      </div>

      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        rows={3}
        style={{ width: "100%" }}
        placeholder="Type your question..."
      />

      <div style={{ marginTop: 8 }}>
        <button onClick={() => send(false)} disabled={loading}>
          Send
        </button>
        <button onClick={() => send(true)} disabled={loading} style={{ marginLeft: 8 }}>
          Stream
        </button>
      </div>
    </div>
  );
}
