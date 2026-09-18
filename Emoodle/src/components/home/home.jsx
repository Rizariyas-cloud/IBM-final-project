import React from 'react';
import { Link } from 'react-router-dom';
import './home.css'
import VideoCard1 from '../videocard1/VideoCard1';

const HomePage = () => {
  return (
    <div className="home">
      <h1 className='welcome'>Welcome to Emoodle</h1>
      <h2 className='info'>A cutting-edge platform that bridges technology and human expression.</h2>
      <h2 className='info1'> Our mission is to create seamless, intuitive interactions between people and devices by leveraging advanced emotion recognition, hand gesture recognition, and sign language detection technologies.</h2>
      <VideoCard1></VideoCard1>
      <div className='EmptyBackground'>
      <h1 className='mainhomeh1' >What's Stopping You from Smiling?</h1>
      <p className='homepara'>Emoodle Helps You find Your Emotions and Support You!</p>
      <Link to="/login"><button className='btn'>Login</button></Link>
      <p>This is just a Prototype Website of our Emotion Recogniton Project.</p>
      </div>
    </div>
  );
};

export default HomePage;
