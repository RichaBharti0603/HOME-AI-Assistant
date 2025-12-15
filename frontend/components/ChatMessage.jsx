"use client";

import { useEffect, useState } from "react";

export default function ChatMessage({ message }) {
  const [time, setTime] = useState("");

  useEffect(() => {
    const date = new Date(message.createdAt);
    setTime(
      date.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      })
    );
  }, [message.createdAt]);

  return (
    <div className={`chat-message ${message.sender}`}>
      <div className="chat-meta">
        <strong>{message.sender === "user" ? "You" : "HOME"}</strong>
        <span>{time}</span>
      </div>
      <div className="chat-text">{message.text}</div>
    </div>
  );
}
