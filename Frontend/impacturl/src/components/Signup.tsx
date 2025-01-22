import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { signup } from '../services/authService';
import AuthLayout from './AuthLayout';

const Signup = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const navigate = useNavigate();
  const typingTexts = ["Join Our Platform.", "Track Your Progress.", "Achieve Your Goals."];

  const handleSignup = async () => {
    if (password !== confirmPassword) {
      alert("Passwords do not match");
      return;
    }
    try {
      await signup(email, password);
      navigate('/login');
    } catch (error) {
      alert('Signup failed. Please try again.');
    }
  };

  return (
    <AuthLayout title="Sign Up" typingTexts={typingTexts}>
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
      <input 
        type="password" 
        placeholder="Confirm Password" 
        value={confirmPassword} 
        onChange={(e) => setConfirmPassword(e.target.value)} 
        className="auth-input"
      />
      <button onClick={handleSignup} className="auth-button">Sign Up</button>
      <p className="register-link" style={{ color: 'white', fontWeight: 'bold' }}>Already Have an account? <a href="/login" style={{ color: '#ffcc00', textDecoration: 'underline' }}> Log in</a></p>
    </AuthLayout>
  );
};

export default Signup;
