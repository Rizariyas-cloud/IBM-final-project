import React from 'react';
import './About.css';
import robot from '../photos/robot.jpg';
import Handrecognition from '../photos/handrecognition.png';
import Signlanguage from '../photos/signlanguage.png';
import facial from '../photos/facialrec.png';

export const About = () => {
  return (
    <div>
        <h1 className='Aboutus'>About Us</h1>
        <p className='Aboutpara1'><b>At Emoodle,</b> we are dedicated to creating a world where technology enhances human connection, especially for those who benefit most from personalized emotional support. Our platform harnesses the power of emotion recognition, hand gesture recognition, and sign language detection to empower individuals, particularly those on the autism spectrum or those needing additional emotional understanding, with tools that foster communication and emotional awareness.</p>
        <br></br>
        <br></br>
        <img src={robot} alt='Robot Picture' className='Robot-Picture'></img>
        <div className='Aboutpara2bg'>
        <p className='Aboutpara2'><b>Our emotion recognition technology</b> uses advanced facial recognition to interpret subtle expressions and emotions, enabling caregivers, educators, and support networks to gain insights into emotional well-being in real time. By identifying shifts in emotional states, this technology offers support tailored to each person's needs, encouraging positive interactions and emotional development.</p>
        <br></br>
        <img src={facial} alt='Facial Picture' className='Facial-Picture'></img>
        </div>
        <div className='Aboutpara3bg'>
        <p className='Aboutpara3'><b>Our Hand Gesture Recognition</b> create new ways to communicate through intuitive gestures, providing autistic individuals with a natural, nonverbal method to express themselves and interact with the world around them. This technology bridges communication gaps, creating a more inclusive environment for individuals who may struggle with traditional verbal communication.</p>
        <br></br>
        <img src={Handrecognition} alt='Hand Picture' className='Hand-Picture'></img>
        </div>
        <div className='Aboutpara4bg'>
        <p className='Aboutpara4'><b> Our Sign Language Detection </b>is designed to translate sign language into text or speech, promoting accessible communication and independence for the Deaf and hard-of-hearing communities, as well as those using sign language as part of their communication toolkit.</p>
        <br></br>
        <img src={Signlanguage} alt='Sign Language Picture' className='Sign-Language'></img>
        </div>
        <div className='Lastparabg'>
        <p className='Lastpara'><b>At Emoodle,</b> Our mission is to make emotional and social support accessible, responsive, and personalized. We envision a future where technology adapts to the diverse ways people communicate, express, and understand emotions, creating a world of deeper empathy and inclusion.</p>
        <br></br>
        </div>
    </div>
  )
}
export default About;
