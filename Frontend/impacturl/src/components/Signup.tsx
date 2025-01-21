import { useState } from 'react';
import { signup } from '../services/authService';

const Signup = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSignup = async () => {
    try {
      await signup(email, password);
      alert('Signup successful! You can now log in.');
    } catch (error) {
      console.error('Signup error', error);
      alert('Signup failed');
    }
  };

  return (
    <div>
      <h2>Signup</h2>
      <input type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
      <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleSignup}>Sign Up</button>
    </div>
  );
};

export default Signup;
