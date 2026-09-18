import React, { useState, useRef, useEffect } from 'react';
import './Emotionrecognition.css';

const Emotionr_ecognition = () => {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [preview, setPreview] = useState(null);
    
    // Real-time webcam states
    const [isStreaming, setIsStreaming] = useState(false);
    const [realtimeResult, setRealtimeResult] = useState(null);
    const [realtimeError, setRealtimeError] = useState(null);
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const streamRef = useRef(null);
    const intervalRef = useRef(null);
    
    const apiUrl = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

    const handleFileChange = (e) => {
        const selectedFile = e.target.files?.[0];
        if (selectedFile) {
            setFile(selectedFile);
            setError(null);
            setResult(null);
            
            // Create preview
            const reader = new FileReader();
            reader.onload = (e) => setPreview(e.target.result);
            reader.readAsDataURL(selectedFile);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) return;
        
        setLoading(true);
        setError(null);
        setResult(null);
        
        try {
            const formData = new FormData();
            formData.append('file', file);
            
            const response = await fetch(`${apiUrl}/predict`, {
                method: 'POST',
                body: formData,
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Prediction failed');
            }
            
            const data = await response.json();
            setResult(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleWebcamCapture = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            const video = document.createElement('video');
            video.srcObject = stream;
            video.play();
            
            // Create a canvas to capture frame
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            video.addEventListener('loadedmetadata', () => {
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                
                // Draw current frame
                ctx.drawImage(video, 0, 0);
                
                // Convert to blob
                canvas.toBlob(async (blob) => {
                    if (blob) {
                        const file = new File([blob], 'webcam-capture.jpg', { type: 'image/jpeg' });
                        setFile(file);
                        setPreview(URL.createObjectURL(blob));
                        
                        // Stop webcam
                        stream.getTracks().forEach(track => track.stop());
                        
                        // Auto-submit
                        const formData = new FormData();
                        formData.append('file', file);
                        
                        setLoading(true);
                        try {
                            const response = await fetch(`${apiUrl}/predict`, {
                                method: 'POST',
                                body: formData,
                            });
                            
                            if (!response.ok) {
                                const errorData = await response.json();
                                throw new Error(errorData.detail || 'Prediction failed');
                            }
                            
                            const data = await response.json();
                            setResult(data);
                        } catch (err) {
                            setError(err.message);
                        } finally {
                            setLoading(false);
                        }
                    }
                }, 'image/jpeg', 0.8);
            });
        } catch (err) {
            setError('Webcam access denied or not available');
        }
    };

    const startRealtimeStream = async () => {
        try {
            setRealtimeError(null);
            const stream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    width: 640, 
                    height: 480,
                    facingMode: 'user'
                } 
            });
            
            streamRef.current = stream;
            setIsStreaming(true);
            
            if (videoRef.current) {
                videoRef.current.srcObject = stream;
                videoRef.current.play();
            }
            
            // Start prediction loop
            intervalRef.current = setInterval(async () => {
                if (videoRef.current && canvasRef.current) {
                    const canvas = canvasRef.current;
                    const ctx = canvas.getContext('2d');
                    const video = videoRef.current;
                    
                    // Draw current frame
                    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                    
                    // Convert to blob and send for prediction
                    canvas.toBlob(async (blob) => {
                        if (blob) {
                            const formData = new FormData();
                            formData.append('file', blob, 'frame.jpg');
                            
                            try {
                                const response = await fetch(`${apiUrl}/predict`, {
                                    method: 'POST',
                                    body: formData,
                                });
                                
                                if (response.ok) {
                                    const data = await response.json();
                                    setRealtimeResult(data);
                                }
                            } catch (err) {
                                // Silent fail for real-time to avoid spam
                                console.warn('Prediction failed:', err);
                            }
                        }
                    }, 'image/jpeg', 0.7);
                }
            }, 1000); // Predict every 1 second
            
        } catch (err) {
            setRealtimeError('Webcam access denied or not available');
            setIsStreaming(false);
        }
    };

    const stopRealtimeStream = () => {
        if (streamRef.current) {
            streamRef.current.getTracks().forEach(track => track.stop());
            streamRef.current = null;
        }
        
        if (intervalRef.current) {
            clearInterval(intervalRef.current);
            intervalRef.current = null;
        }
        
        setIsStreaming(false);
        setRealtimeResult(null);
        
        if (videoRef.current) {
            videoRef.current.srcObject = null;
        }
    };

    // Cleanup on unmount
    useEffect(() => {
        return () => {
            stopRealtimeStream();
        };
    }, []);

    return (
        <div className="emotion-recognition-container">
            <h1 className='erhead'>Emotion Recognition</h1>
            
            <div className="upload-section">
                <div className="upload-options">
                    <div className="file-upload">
                        <label htmlFor="file-input" className="upload-label">
                            📁 Choose Image File
                        </label>
                        <input
                            id="file-input"
                            type="file"
                            accept="image/*"
                            onChange={handleFileChange}
                            style={{ display: 'none' }}
                        />
                    </div>
                    
                    <button 
                        type="button" 
                        onClick={handleWebcamCapture}
                        className="webcam-button"
                        disabled={loading || isStreaming}
                    >
                        📷 Capture Photo
                    </button>
                    
                    <button 
                        type="button" 
                        onClick={isStreaming ? stopRealtimeStream : startRealtimeStream}
                        className={`realtime-button ${isStreaming ? 'stop' : 'start'}`}
                        disabled={loading}
                    >
                        {isStreaming ? '⏹️ Stop Live' : '🎥 Start Live Recognition'}
                    </button>
                </div>
                
                {preview && (
                    <div className="preview-section">
                        <img src={preview} alt="Preview" className="preview-image" />
                        <button 
                            type="button" 
                            onClick={handleSubmit}
                            disabled={loading || !file}
                            className="analyze-button"
                        >
                            {loading ? '🔄 Analyzing...' : '🔍 Analyze Emotion'}
                        </button>
                    </div>
                )}
            </div>
            
            {/* Real-time video stream */}
            {isStreaming && (
                <div className="realtime-section">
                    <div className="video-container">
                        <video 
                            ref={videoRef}
                            className="live-video"
                            autoPlay
                            muted
                            playsInline
                        />
                        <canvas 
                            ref={canvasRef}
                            className="hidden-canvas"
                            width="640"
                            height="480"
                        />
                        
                        {realtimeResult && (
                            <div className="live-overlay">
                                <div className="live-emotion">
                                    {realtimeResult.predicted_emotion}
                                </div>
                                <div className="live-confidence">
                                    {(realtimeResult.confidence * 100).toFixed(1)}%
                                </div>
                            </div>
                        )}
                    </div>
                    
                    {realtimeError && (
                        <div className="error-message">
                            ❌ Live Error: {realtimeError}
                        </div>
                    )}
                </div>
            )}
            
            {error && (
                <div className="error-message">
                    ❌ Error: {error}
                </div>
            )}
            
            {result && (
                <div className="result-section">
                    <div className="main-result">
                        <h2>🎭 Predicted Emotion</h2>
                        <div className="emotion-result">
                            <span className="emotion-name">{result.predicted_emotion}</span>
                            <span className="confidence">
                                {(result.confidence * 100).toFixed(1)}% confidence
                            </span>
                        </div>
                    </div>
                    
                    <div className="all-predictions">
                        <h3>📊 All Predictions</h3>
                        <div className="predictions-list">
                            {Object.entries(result.all_predictions)
                                .sort(([,a], [,b]) => b - a)
                                .map(([emotion, confidence]) => (
                                <div key={emotion} className="prediction-item">
                                    <span className="emotion-label">{emotion}</span>
                                    <div className="confidence-bar">
                                        <div 
                                            className="confidence-fill"
                                            style={{ width: `${confidence * 100}%` }}
                                        ></div>
                                    </div>
                                    <span className="confidence-text">
                                        {(confidence * 100).toFixed(1)}%
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}
            
            <footer className='footer'>
                Live Footage is Captured and Recorded for Development Purposes
            </footer>
        </div>
    );
};

export default Emotionr_ecognition;