import { logout } from '../services/authService';

const Logout = () => {
  const handleLogout = () => {
    logout();
    alert('You have been logged out');
  };

  return <button onClick={handleLogout}>Logout</button>;
};

export default Logout;
