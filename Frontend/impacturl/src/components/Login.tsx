import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../services/authService';
import './Login.css'; // Add CSS for styling

const Login = ({ setIsAuthenticated }: { setIsAuthenticated: (auth: boolean) => void }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const typingTexts = ["Shorten Your URLs.", "Track Your Links.", "Grow Your Influence."];

  const handleLogin = async () => {
    try {
      const response = await login(email, password);
      localStorage.setItem('accessToken', response.access);
      localStorage.setItem('refreshToken', response.refresh);
      setIsAuthenticated(true);
      navigate('/home');
    } catch (error) {
      console.error('Login error:', error.response ? error.response.data : error.message);
      alert('Login failed. Please check your credentials.');
    }
  };

  // Typing animation logic
  const [currentText, setCurrentText] = useState('');
  const [index, setIndex] = useState(0);
  const [subIndex, setSubIndex] = useState(0);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    if (subIndex === typingTexts[index].length + 1 && !isDeleting) {
      setIsDeleting(true);
      setTimeout(() => {}, 1000);
    } else if (subIndex === 0 && isDeleting) {
      setIsDeleting(false);
      setIndex((prev) => (prev + 1) % typingTexts.length);
    }

    const timeout = setTimeout(() => {
      setSubIndex((prev) => (isDeleting ? prev - 1 : prev + 1));
    }, isDeleting ? 50 : 100);

    return () => clearTimeout(timeout);
  }, [subIndex, index, isDeleting]);

  useEffect(() => {
    setCurrentText(typingTexts[index].substring(0, subIndex));
  }, [subIndex, index]);

  return (
    <div className="login-container">
      <div className="login-animated-text">
        <h1>{currentText}</h1>
      </div>
      <div className="login-form">
        <h2>Login</h2>
        <input 
          type="email" 
          placeholder="Email" 
          value={email} 
          onChange={(e) => setEmail(e.target.value)} 
          className="login-input"
        />
        <input 
          type="password" 
          placeholder="Password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
          className="login-input"
        />
        <button onClick={handleLogin} className="login-button">Login</button>
        <p className="forgot-password"><a href="/forgot-password">Forgot Password?</a></p>
        <p className="register-link">Need an account? <a href="/register">Sign Up</a></p>
      </div>
    </div>
  );
};

export default Login;
