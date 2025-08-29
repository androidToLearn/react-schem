import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import OdotPage from "./pages/OdotPage";
import StatisticPage from "./pages/StatisticPage";
import LoginPage from "./pages/LoginPage";
import Home from './pages/Home';
import Page404 from './pages/Page404'

function App() {
  return (
    //הגדרת נתיבים
    <div>
      <Router>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/odot" element={<OdotPage />} />
          <Route path="/statistics" element={<StatisticPage />} />
          <Route path="/" element={<Home />} />
          <Route path='*' element={<Page404 />} />
        </Routes>
      </Router>
    </div>
  )
}

export default App
