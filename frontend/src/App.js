import React, { useState, useEffect, useRef } from "react";
import "./App.css";

function App() {

  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const ws = useRef(null);
  const chatEndRef = useRef(null);
  const [showTests, setShowTests] = useState(true);

  
  const testQueries = [
    "I am getting a 500 error after deployment.",
    "Nothing is working and I am extremely frustrated.",
    "How will this impact ROI in the long term?",
    "It is working fine but I need some clarification.",
    "The logs show a memory leak in the service."
  ];

  useEffect(() => {
    ws.current = new WebSocket("ws://127.0.0.1:8000/ws");

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);

      setChat(prev => [
        ...prev,
        {
          sender: "Bot",
          text: data.reply,
          persona: data.persona,
          sentiment: data.sentiment,
          escalate: data.escalate,
          pdf: data.pdf_download || null
        }
      ]);
    };

    return () => ws.current.close();
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat]);

  const sendMessage = (customMessage = null) => {
    const finalMessage = customMessage || message;
    if (!finalMessage) return;

    setChat(prev => [...prev, { sender: "User", text: finalMessage }]);
    ws.current.send(finalMessage);
    setMessage("");
  };

  const getPersonaClass = (persona) => {
    switch (persona) {
      case "technical_expert":
        return "tech";
      case "frustrated_user":
        return "frustrated";
      case "business_executive":
        return "business";
      default:
        return "default";
    }
  };

  return (
    <div className="app-container">
      <div className="chat-card">
        <h2 className="title">🤖 AI Persona Support</h2>

        <div className="test-container">

  <div 
    className="test-header" 
    onClick={() => setShowTests(!showTests)}
  >
    <div>🚀 Quick Demo Queries</div>
    <span>{showTests ? "Hide" : "Show"}</span>
  </div>

  {showTests && (
    <div className="test-list">
      {testQueries.map((query, index) => (
        <button
          key={index}
          className="test-button"
          onClick={() => sendMessage(query)}
        >
          {query.length > 30 ? query.substring(0, 30) + "..." : query}
        </button>
      ))}
    </div>
  )}

</div>
        

        <div className="chat-window">
          {chat.map((c, index) => (
            <div
              key={index}
              className={`message-row ${c.sender === "User" ? "user" : "bot"}`}
            >
              <div
                className={`bubble ${
                  c.sender === "Bot" ? getPersonaClass(c.persona) : "user-bubble"
                }`}
              >
                {c.text}
              </div>

              {c.sender === "Bot" && (
                <div className="meta">
                  Persona: {c.persona} | Sentiment: {c.sentiment}
                </div>
              )}

              {c.escalate && (
                <div className="escalation">
                  ⚠ Escalation Triggered
                  {c.pdf && (
                    <div>
                      <a href={c.pdf} target="_blank" rel="noreferrer">
                        Download Chat PDF
                      </a>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
          <div ref={chatEndRef}></div>
        </div>

        <div className="input-area">
          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            placeholder="Type your message..."
          />
          <button onClick={() => sendMessage()}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;