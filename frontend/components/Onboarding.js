"use client";

export default function Onboarding({ onComplete }) {
  const select = (type) => {
    localStorage.setItem("userType", type);
    onComplete(type);
  };

  return (
    <div style={{ textAlign: "center", marginTop: 60 }}>
      <h2>Welcome to HOME AI Assistant</h2>

      <button onClick={() => select("individual")}>
        Personal Use
      </button>

      <br /><br />

      <button onClick={() => select("organization")}>
        Organization
      </button>
    </div>
  );
}
