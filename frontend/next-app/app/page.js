import ChatWindow from "../components/ChatWindow";

export default function Home() {
  return (
    <div style={{ maxWidth: 800, margin: "40px auto" }}>
      <h1>HOME — Local AI Assistant</h1>
      <ChatWindow apiUrl="http://127.0.0.1:8000" />
    </div>
  );
}
