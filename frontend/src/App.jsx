import { useState } from "react";
import axios from "axios";
import "./App.css";
import MapView from "./MapView";
import AnalyticsDashboard from "./AnalyticsDashboard";

function App() {
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  // ==========================
  // ASK AI
  // ==========================

  const askAI = async () => {
    const userMessage = prompt;

    if (!userMessage.trim()) {
      alert("Please enter a disaster-related question");
      return;
    }

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        text: userMessage,
      },
    ]);

    setPrompt("");
    setLoading(true);

    try {
      // Dynamically use environment variable for production (Netlify) or fallback to local
      const backendUrl = import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:8000";

      const response = await axios.post(
        `${backendUrl}/chat`,
        {
          prompt: userMessage,
        },
        {
          headers:{
            "ngrok-skip-browser-warning": "true"
          }
        }
      );

      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: response.data.answer,
          disaster: response.data.disaster,
          severity: response.data.severity,
          weather: response.data.weather,
          news: response.data.news,
          sources: response.data.sources,
        },
      ]);
    } catch (error) {
      console.log(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: "❌ Unable to connect with AI server.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // Clear Chat
  const clearChat = () => {
    setMessages([]);
  };

  // Copy
  const copyText = (text) => {
    navigator.clipboard.writeText(text);
    alert("Response copied!");
  };

  // Disaster Icon
  const getDisasterIcon = (disaster) => {
    const type = disaster?.toLowerCase();

    if (type === "flood") return "🌊";
    if (type === "earthquake") return "🌎";
    if (type === "wildfire") return "🔥";
    if (type === "cyclone") return "🌪️";
    if (type === "tsunami") return "🌊";
    if (type === "landslide") return "⛰️";
    return "⚠️";
  };

  return (
    <div className="app">
      <header>
        <h1>🌍 AI Disaster Management System</h1>
        <p>AI-powered emergency analysis and disaster assistance</p>

        <button className="clear-btn" onClick={clearChat}>
          🧹 Clear Chat
        </button>
      </header>

      <div className="chat-container">
        
        {/* Disaster Analytics Dashboard */}
        <AnalyticsDashboard messages={messages} />

        <div className="chat-box">
          {messages.length === 0 ? (
            <p className="welcome">
              Ask me anything about earthquakes, floods, cyclones, wildfire,
              tsunami, landslides or disaster safety.
            </p>
          ) : (
            messages.map((msg, index) => (
              <div
                key={index}
                className={msg.role === "user" ? "user-message" : "ai-message"}
              >
                <strong>{msg.role === "user" ? "👤 You" : "🤖 DisasterAI"}</strong>

                {msg.role === "ai" && (
                  <div className="metadata">
                    <p className="disaster-type">
                      {getDisasterIcon(msg.disaster)} Disaster: {msg.disaster}
                    </p>

                    <p>
                      🚨 Severity:{" "}
                      <span className={`severity ${msg.severity?.toLowerCase()}`}>
                        {msg.severity}
                      </span>
                    </p>

                    {msg.weather && (
                      <>
                        <div className="weather-card">
                          <h4>🌦 Weather Information</h4>
                          <p>📍 City: {msg.weather.city}</p>
                          <p>🌡 Temperature: {msg.weather.temperature}°C</p>
                          <p>☁ Condition: {msg.weather.weather}</p>
                          <p>💧 Humidity: {msg.weather.humidity}%</p>
                          <p>💨 Wind Speed: {msg.weather.wind_speed} m/s</p>
                        </div>

                        <MapView
                          city={msg.weather.city}
                          lat={msg.weather.lat}
                          lon={msg.weather.lon}
                        />
                      </>
                    )}
                  </div>
                )}

                <p>{msg.text}</p>

                <button
                  className="copy-btn"
                  onClick={() => copyText(msg.text)}
                >
                  📋 Copy
                </button>

                <div className="emergency-card">
                  <h4>🚨 Emergency Contacts</h4>
                  <p>📞 Disaster Management: 1078</p>
                  <p>🚑 Ambulance: 108</p>
                  <p>🚓 Police: 100</p>
                  <p>🔥 Fire: 101</p>
                </div>

                {msg.news && msg.news.length > 0 && (
                  <div className="news-card">
                    <h4>📰 Latest Disaster News</h4>
                    {msg.news.map((article, i) => (
                      <div className="news-item" key={i}>
                        <p>📰 {article.title}</p>
                        <small>Source: {article.source}</small>
                        <br />
                        <a
                          href={article.url}
                          target="_blank"
                          rel="noreferrer"
                        >
                          Read Full Article →
                        </a>
                      </div>
                    ))}
                  </div>
                )}

                {msg.sources && msg.sources.length > 0 && (
                  <div className="sources">
                    <h4>📚 Sources Used</h4>
                    {msg.sources.map((source, i) => (
                      <p key={i}>📄 {source}</p>
                    ))}
                  </div>
                )}
              </div>
            ))
          )}

          {loading && (
            <div className="ai-message">
              <strong>🤖 DisasterAI</strong>
              <p>Analyzing disaster information...</p>
            </div>
          )}
        </div>

        <div className="input-area">
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Ask your disaster-related question..."
          />

          <button onClick={askAI} disabled={loading}>
            {loading ? "Processing..." : "Ask AI"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;