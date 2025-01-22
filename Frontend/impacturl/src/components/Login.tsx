import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../services/authService';

const Login = ({ setIsAuthenticated }: { setIsAuthenticated: (auth: boolean) => void }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await login(email, password);

      // Store tokens in localStorage and update authentication state
      localStorage.setItem('accessToken', response.access);
      localStorage.setItem('refreshToken', response.refresh);
      setIsAuthenticated(true);

      // Redirect to home page after successful login
      navigate('/home');
    } catch (error) {
      console.error('Login error:', error.response ? error.response.data : error.message);
      alert('Login failed. Please check your credentials.');
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <input type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
      <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleLogin}>Log In</button>
    </div>
  );
};

export default Login;
