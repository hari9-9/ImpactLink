import { useState } from 'react';
import { login } from '../services/authService';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    try {
      const response = await login(email, password);
  
      // Destructure the response properly
      const { access, refresh } = response;
  
      if (access && refresh) {
        localStorage.setItem('accessToken', access);
        localStorage.setItem('refreshToken', refresh);
        alert('Login successful!');
      } else {
        throw new Error("Invalid response structure");
      }
    } catch (error: any) {
      console.error("Login error:", error.response ? error.response.data : error.message);
      alert(error.response?.data?.detail || "Login failed. Please check your credentials.");
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
