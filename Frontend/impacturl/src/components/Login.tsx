import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../services/authService';
import AuthLayout from './AuthLayout';

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
      navigate('/dashboard');
    } catch (error) {
      alert('Login failed. Please check your credentials.');
    }
  };

  return (
    <AuthLayout title="Login" typingTexts={typingTexts}>
      <input 
        type="email" 
        placeholder="Email" 
        value={email} 
        onChange={(e) => setEmail(e.target.value)} 
        className="auth-input"
      />
      <input 
        type="password" 
        placeholder="Password" 
        value={password} 
        onChange={(e) => setPassword(e.target.value)} 
        className="auth-input"
      />
      <button onClick={handleLogin} className="auth-button">Login</button>
      <p className="forgot-password"><a href="/forgot-password">Forgot Password?</a></p>
      <p className="register-link" style={{ color: 'white', fontWeight: 'bold' }}>Need an account? <a href="/signup" style={{ color: '#ffcc00', textDecoration: 'underline' }}>Sign Up</a></p>
    </AuthLayout>
  );
};

export default Login;
