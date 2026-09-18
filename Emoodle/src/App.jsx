import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/home/home';
import Login from './components/login/Login';
import { Navbar } from './components/navbar/Navbar';
import About from './components/about/about';
import Emotionrecognition from './components/services/Emotionrecognition';

import './App.css';

function App() {
  return (
    <Router>
      <Navbar/>
      <div style={{ paddingTop: '84px'}}>
      <Routes>
      <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/about" element={<About />} />
        <Route path="/services/emotion-recognition" element={<Emotionrecognition />}/>
      </Routes>
      </div>
    </Router>
  );
}

export default App;
