import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { signup } from '../services/authService';

const Signup = () => {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSignup = async () => {
    try {
      await signup(email, name, password);

      alert('Signup successful! Redirecting to login page.');

      // Redirect to login page after successful signup
      navigate('/login');
    } catch (error: any) {
      console.error('Signup error:', error.response ? error.response.data : error.message);
      alert(error.response?.data?.detail || 'Signup failed. Please try again.');
    }
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h2>Signup</h2>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      /><br /><br />
      <input
        type="text"
        placeholder="Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      /><br /><br />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      /><br /><br />
      <button onClick={handleSignup}>Sign Up</button>
    </div>
  );
};

export default Signup;
