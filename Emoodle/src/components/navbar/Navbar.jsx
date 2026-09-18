// components/navbar/Navbar.jsx

import React, { useState, useEffect } from 'react';
import { Link, NavLink } from 'react-router-dom';
import './Navbar.css';

export const Navbar = () => {
  const [showNavbar, setShowNavbar] = useState(true);
  const [lastScrollY, setLastScrollY] = useState(0);
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const handleScroll =() => {
    if (window.scrollY > lastScrollY) {
      setShowNavbar(false);
    } else {
      setShowNavbar(true);
    }
    setLastScrollY(window.scrollY);
  };

  const toggleDropdown = () => {
    setDropdownOpen(!dropdownOpen);
  };

  useEffect(() => {
    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, [lastScrollY]);
  
  return (
    <nav className={`navbar ${showNavbar ? 'visible' : 'hidden'}`}>
      <h1 className="navbar-logo">EMOODLE</h1>
      <ul className="navbar-links">
        <li>
            <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/about">About</Link>
        </li>
        <li 
          className="navbar-dropdown"
          onMouseEnter={() => setDropdownOpen(true)}
          onMouseLeave={() => setDropdownOpen(false)}>

            <Link onClick={toggleDropdown}>Services</Link>
            {dropdownOpen && (
              <ul className="dropdown-menu">
                <li>
                  <Link to="/services/emotion-recognition">Emotion Recognition</Link>
                </li>
                <li>
                  <Link to="/services/hand-gesture">Hand Gesture Recognition</Link>
                </li>
                <li>
                  <Link to="/services/sign-language">Sign Language Detection</Link>
                </li>
              </ul>
            )}
          </li>
        <li>
          <Link to="/login">Login</Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
