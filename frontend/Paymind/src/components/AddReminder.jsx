import React, { useState } from "react";
import "../AddReminder.css"; // Import external CSS

export default function AddReminder() {
  const [formData, setFormData] = useState({
    name: "",
    amount: "",
    due_date: "",
    email: "",
    mobile:""
  });
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.id]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:5000/reminders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const result = await response.json();

      if (response.ok) {
        setMessage("✅ Reminder added successfully!");
        setMessageType("success");
        setFormData({ name: "", amount: "", due_date: "", email: "",mobile:"" });
      } else {
        setMessage("❌ " + (result.error || "Something went wrong"));
        setMessageType("error");
      }
    } catch (error) {
      setMessage("❌ Network error!");
      setMessageType(error);
    }
  };

  return (
    <div className="container">
      <h2>Add Reminder</h2>
      <form onSubmit={handleSubmit}>
        <label>Name</label>
        <input type="text" id="name" value={formData.name} onChange={handleChange} required />

        <label>Amount</label>
        <input type="number" id="amount" value={formData.amount} onChange={handleChange} required />

        <label>Due Date</label>
        <input type="date" id="due_date" value={formData.due_date} onChange={handleChange} required />

        <label>Email</label>
        <input type="email" id="email" value={formData.email} onChange={handleChange} required />

        <label>Mobile</label>
        <input type="text" id="mobile" value={formData.mobile} onChange={handleChange} required />
        <button type="submit">Add Reminder</button>
      </form>

      {message && <div className={`message ${messageType}`}>{message}</div>}
    </div>
  );
}
