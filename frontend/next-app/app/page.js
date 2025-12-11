"use client";

import { useState, useRef, useEffect } from "react";

export default function Home() {
  const API = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]); // {role, text, time}
  const [loading, setLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const controllerRef = useRef(null);
  const listRef = useRef(null);

  useEffect(() => {
    listRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages]);

  const addMessage = (role, text) => {
    setMessages(m => [...m, { role, text, time: new Date().toLocaleTimeString() }]);
  };

  const askBackend = async (q, stream = false) => {
    addMessage("user", q);
    setQuestion("");
    setLoading(true);

    if (!stream) {
      try {
        const res = await fetch(`${API}/ask`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question: q, user_id: "user_1" }),
        });

        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

        const data = await res.json();
        addMessage("assistant", data.answer);

        speakText(data.answer);
      } catch (err) {
        addMessage("assistant", "Error: " + err.message);
      } finally {
        setLoading(false);
      }
    } else {
      controllerRef.current = new AbortController();

      try {
        const res = await fetch(`${API}/ask_stream`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question: q, user_id: "user_1" }),
          signal: controllerRef.current.signal,
        });

        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

        const reader = res.body.getReader();
        const decoder = new TextDecoder();

        let assistantText = "";

        addMessage("assistant", "");

        while (true) {
          const { value, done } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          assistantText += chunk;

          setMessages(m => {
            const copy = [...m];
            for (let i = copy.length - 1; i >= 0; i--) {
              if (copy[i].role === "assistant") {
                copy[i] = {
                  ...copy[i],
                  text: assistantText,
                  time: new Date().toLocaleTimeString()
                };
                break;
              }
            }
            return copy;
          });
        }

        speakText(assistantText);
      } catch (err) {
        addMessage("assistant", "Error streaming: " + err.message);
      } finally {
        setLoading(false);
      }
    }
  };

  const speakText = (text) => {
    try {
      const utter = new SpeechSynthesisUtterance(text);
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(utter);
    } catch (e) {}
  };

  const startRecording = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("SpeechRecognition not supported in this browser.");
      return;
    }

    const rec = new SpeechRecognition();
    rec.lang = "en-US";
    rec.interimResults = true;

    rec.onresult = (e) => {
      const last = e.results[e.results.length - 1];
      setQuestion(last[0].transcript);
    };

    rec.onend = () => setIsRecording(false);

    rec.start();
    setIsRecording(true);
  };

  return (
    <div style={{ maxWidth: 760, margin: "1.5rem auto", fontFamily: "Inter, sans-serif" }}>
      <h1>HOME — Local AI Assistant</h1>

      <div style={{ minHeight: 300, border: "1px solid #eee", padding: 12, borderRadius: 8 }}>
        {messages.map((m, i) => (
          <div
            key={i}
            style={{ marginBottom: 8, textAlign: m.role === "user" ? "right" : "left" }}
          >
            <div
              style={{
                display: "inline-block",
                padding: "8px 12px",
                borderRadius: 12,
                background: m.role === "user" ? "#cce6ff" : "#f1f1f1",
                maxWidth: "85%",
                whiteSpace: "pre-wrap",
              }}
            >
              <div style={{ fontSize: 12, color: "#333", marginBottom: 4 }}>
                <strong>{m.role === "user" ? "You" : "Home"}</strong> •{" "}
                <span style={{ color: "#666" }}>{m.time}</span>
              </div>
              <div>{m.text}</div>
            </div>
          </div>
        ))}

        <div ref={listRef} />
      </div>

      <div style={{ marginTop: 12 }}>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          rows={3}
          style={{ width: "100%" }}
          placeholder="Type your question..."
        />

        <div style={{ marginTop: 8, display: "flex", alignItems: "center", gap: 8 }}>
          <button onClick={() => askBackend(question, false)} disabled={loading}>Send</button>
          <button onClick={() => askBackend(question, true)} disabled={loading}>Stream</button>
          <button onClick={() => controllerRef.current?.abort()} disabled={!loading}>Abort</button>

          <button
            onClick={() => startRecording()}
            style={{ marginLeft: "auto", background: isRecording ? "red" : "" }}
          >
            {isRecording ? "Recording..." : "Record"}
          </button>
        </div>
      </div>
    </div>
  );
}
