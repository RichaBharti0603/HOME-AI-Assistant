import React from "react";
import dynamic from "next/dynamic";
import "../globals.css";

const ChatWindow = dynamic(() => import("../components/ChatWindow"), { ssr: false });

export default function Home() {
  return (
    <main className="chat-container">
      <h1>HOME — Local AI Assistant</h1>
      <ChatWindow apiUrl="http://127.0.0.1:8000" />
    </main>
  );
}
