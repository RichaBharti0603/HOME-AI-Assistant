"use client"; // This ensures hydration runs on client

import React from "react";

export default function ChatMessage({ message }) {
  const { sender, text, timestamp } = message;

  return (
    <div className={`chat-message ${sender}`}>
      <div>{text}</div>
      <div className="timestamp">{new Date(timestamp).toLocaleTimeString()}</div>
    </div>
  );
}
