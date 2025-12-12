"use client";

import React, { useEffect, useRef, useState } from "react";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput"; // <-- Add this import

export default function ChatWindow({ apiUrl }) {
  const [messages, setMessages] = useState([]);
  const chatEndRef = useRef(null);

  const sendMessage = async (text) => {
    const userMsg = { sender: "user", text, timestamp: Date.now() };
    setMessages((prev) => [...prev, userMsg]);

    const res = await fetch(`${apiUrl}/ask_stream`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: text, user_id: "user_1" }),
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
        const lastMsg = prev[prev.length - 1];
        if (lastMsg?.sender === "ai") {
          const updated = [...prev];
          updated[updated.length - 1] = { ...lastMsg, text: aiText, timestamp: lastMsg.timestamp };
          return updated;
        } else {
          return [...prev, { sender: "ai", text: aiText, timestamp: Date.now() }];
        }
      });
    }
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div>
      <div className="chat-window">
        {messages.map((m, idx) => (
          <ChatMessage key={idx} message={m} />
        ))}
        <div ref={chatEndRef}></div>
      </div>
      <ChatInput onSend={sendMessage} /> {/* Now this will work */}
    </div>
  );
}
