"use client";

import React, { useEffect, useRef, useState } from "react";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";

export default function ChatWindow({ apiUrl }) {
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const chatEndRef = useRef(null);

  // Create stable session id (client-only)
  useEffect(() => {
    let sid = localStorage.getItem("home_session_id");
    if (!sid) {
      sid = crypto.randomUUID();
      localStorage.setItem("home_session_id", sid);
    }
    setSessionId(sid);
  }, []);

  const sendMessage = async (text) => {
    if (!sessionId) return;

    const userMsg = {
      sender: "user",
      text,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMsg]);

    const res = await fetch(`${apiUrl}/ask_stream`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: text,
        session_id: sessionId,
      }),
    });

    if (!res.body) return;

    const reader = res.body.getReader();
    const decoder = new TextDecoder("utf-8");

    let aiText = "";

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      aiText += decoder.decode(value, { stream: true });

      setMessages((prev) => {
        const last = prev[prev.length - 1];
        if (last?.sender === "ai") {
          const updated = [...prev];
          updated[updated.length - 1] = {
            ...last,
            text: aiText,
          };
          return updated;
        }
        return [
          ...prev,
          { sender: "ai", text: aiText, timestamp: new Date().toISOString() },
        ];
      });
    }
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div>
      <div className="chat-window">
        {messages.map((m, i) => (
          <ChatMessage key={i} message={m} />
        ))}
        <div ref={chatEndRef} />
      </div>

      <ChatInput onSend={sendMessage} />
    </div>
  );
}
