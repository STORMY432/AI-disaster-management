import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("Loading...");

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/")
      .then((response) => {
        setMessage(response.data.message);
      })
      .catch(() => {
        setMessage("Backend not connected");
      });
  }, []);

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h1>AI Disaster Management</h1>
      <h2>{message}</h2>
    </div>
  );
}

export default App;