import React from "react";
import { Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import AddReminder from "./components/AddReminder";
import "./App.css";

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/add-reminder" element={<AddReminder />} />
    </Routes>
  );
}

export default App;