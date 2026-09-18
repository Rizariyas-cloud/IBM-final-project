// components/VideoCard.jsx

import React from 'react';
import './VideoCard1.css';

const VideoCard = () => {
    return (
        <div className="video-container">
          <video width="100%" height="auto"
          autoPlay
          muted
          loop
          playsInline>
            <source src="/Video1.mp4" type="video/mp4" />
          </video>
        </div>
      );
    };

export default VideoCard;