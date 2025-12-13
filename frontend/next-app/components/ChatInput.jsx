"use client";

import { useState } from "react";

export default function ChatInput({ onSend }) {
  const [value, setValue] = useState("");

  const handleSend = () => {
    onSend(value);
    setValue("");
  };

  return (
    <div className="chat-input">
      <input
        type="text"
        value={value}
        placeholder="Type your question..."
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSend()}
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}
