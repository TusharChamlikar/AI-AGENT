import React from "react";
import "./App.css";
import AddReminder from "./components/AddReminder";
function App() {
  return (
    <div className="app-container">
      <h1>💰 Paymind - Payment Reminder</h1>
      <p>Send payment reminders via Email, SMS, and Voice</p>
      <AddReminder></AddReminder>
    </div>
  );
}

export default App;
